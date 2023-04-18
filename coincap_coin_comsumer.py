# Databricks notebook source
# Define Kafka configurations
kafka_brokers = "b-1.detrainingmsk.66lq6h.c10.kafka.us-east-1.amazonaws.com:9092"
kafka_topic = 'coin_data'

# Read data from Kafka
df = (spark.readStream.format("kafka")
    .option('inferSchema', True)
    .option("kafka.bootstrap.servers", kafka_brokers) 
    .option("subscribe", kafka_topic) 
    .option("startingOffsets", "latest") 
    .load()
     )

display(df)

# COMMAND ----------

df.printSchema()

# COMMAND ----------

from pyspark.sql.functions import *
df1 = df.select(col('value').cast('string'))
display(df1)
df1.printSchema()

# COMMAND ----------

#define Schema methord 1

from pyspark.sql.functions import window, from_json, col, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, LongType

# Define the schema of the Kafka messages
schema = StructType([
    StructField("exchange", StringType()),
    StructField("base", StringType()),
    StructField("quote", StringType()),
    StructField("direction", StringType()),
    StructField("price", DoubleType()),
    StructField("volume", DoubleType()),
    StructField("timestamp", LongType()),
    StructField("priceUsd", DoubleType())
  ])


# COMMAND ----------

#define Schema methord 2: save the streaming data as a static file, and use inferschema to obtain schema

path = '/users/sophiawu/coincap'

query =(df1.writeStream
  .format("csv") 
  .option("path", path) 
  .option('header', True)
  .option("checkpointLocation", "/users/sophiawu/checkpoint/coincap") 
  .start()
       )


# save it as a static data to obtain schema


static_df = spark.read.format("csv") \
  .option("inferSchema", "true") \
  .option("header", "true") \
  .load("/users/sophiawu/coincap")
static_df.printSchema()
display(static_df)

# COMMAND ----------

# Parse JSON message Since the message value is in JSON format. Use from_json() function takes two arguments: the first argument is the column to parse, and the second argument is the schema to use for parsing. 
# * is a wildcard character that represents all columns in the data dataframe. 

parsed_df = (df
    .select(from_json(col("value").cast("string"), schema).alias("data"))
    .select('data.*')
            )

display(parsed_df)

# COMMAND ----------

parsed_df.printSchema()

# COMMAND ----------

#change the timestamp from long data type to timestamp data type
    
from pyspark.sql.functions import from_utc_timestamp, to_utc_timestamp, lit

 # Convert the Unix timestamp to a string timestamp. if it is 13 digitals, divide by 1000 to convert milliseconds to seconds
timestamp_df =(parsed_df.withColumn("timestamp", from_unixtime(parsed_df.timestamp/1000, "yyyy-MM-dd HH:mm:ss"))
#             #use the from_utc_timestamp function to convert the timestamp from UTC format to local time zone
              .withColumn("timestamp", from_utc_timestamp("timestamp", "UTC")) 
 
        )
display(timestamp_df)
timestamp_df.printSchema()

  

# COMMAND ----------

# Tumbling window. Show the last 5 minutes trading information in 1- minutes tumbling window, the output must include at least 5 columns

from pyspark.sql.functions import *

tumbling_window = (timestamp_df
#     .filter((col('base') =='bitcoin') | (col('base') == 'ethereum'))
    .withWatermark('timestamp','5 minutes')
    .withColumn('amount', col('priceUsd')*col('volume'))
    .groupBy('base', window('timestamp', '1 minutes').alias('window'))
    .agg(sum('volume').alias('total_volume'), sum('amount').alias('total_amount'))
    .withColumn('actual_avg', col('total_amount')/col('total_volume') )
    .select('window','base','total_volume','actual_avg')
    .orderBy(desc('actual_avg'))
)
display(tumbling_window)

# COMMAND ----------

# Write streaming DataFrame to Delta Lake format

static = (tumbling_window.writeStream
    .queryName('change') 
    .format('memory')
    .trigger(processingTime='10 seconds')
    .outputMode("complete")
    .start()
    )

# import time
# for i in range(10):
#     print(f"Run index {i}:")
#     spark.sql("SELECT * FROM change").show(truncate=False)
#     time.sleep(60)


# COMMAND ----------

table_df = spark.sql("SELECT * FROM change")
table_df.printSchema()

# COMMAND ----------

table_df.count()

# COMMAND ----------

#Q6
from pyspark.sql.window import Window
windowSpec  = Window.partitionBy("base").orderBy("window")
rowNum = Window.partitionBy("base").orderBy(desc("window"))

price_trend = (table_df.withColumn('price_trend', when(col('actual_avg') > lag('actual_avg',1).over(windowSpec), "up")
                                                       .when(col('actual_avg') < lag('actual_avg',1).over(windowSpec), "down")
                                                       .otherwise('null'))
                       .withColumn('rowNum', row_number().over(rowNum))
                       .where(col('rowNum')<=5)
                       .orderBy('base','window')
              )

display(price_trend)

# COMMAND ----------

price_trend.printSchema()

# COMMAND ----------

from pyspark.sql.functions import regexp_replace, concat_ws, col, lit

change_window = price_trend.withColumn('window', 
                    concat(lit('{'), 
                          regexp_replace(concat_ws(',', col('window.start'), col('window.end')), 
                                         '[{|}]|start:|end:', ''), 
                          lit('}'))
                  )
display(change_window)

# COMMAND ----------

change_window.printSchema()

# COMMAND ----------

import time
for i in range(10):
    print(f"Run index {i}:")
    table_df = spark.sql("SELECT * FROM change")
    windowSpec  = Window.partitionBy("base").orderBy("window")
    rowNum = Window.partitionBy("base").orderBy(desc("window"))
    price_trend = (table_df.withColumn('price_trend', when(col('actual_avg') > lag('actual_avg',1).over(windowSpec), "up")
                                                       .when(col('actual_avg') < lag('actual_avg',1).over(windowSpec), "down")
                                                       .otherwise('null'))
                       .withColumn('rowNum', row_number().over(rowNum))
                       .where(col('rowNum')<=5)
                       .orderBy('base','window')
              )
    price_trend.show(truncate = False)
    time.sleep(60)

# COMMAND ----------

price_trend.printSchema()

# COMMAND ----------

# save the streaming table to mysql database. However,  a struct or a nested data type that cannot be mapped directly to a JDBC data type.
# so we should flatten the DataFrame to remove the struct column and replace it with its nested fields.

from pyspark.sql.functions import col

jdbc_url = 'jdbc:mysql://database.ascendingdc.com:3306/de_001'
user = 'sophiawu'
password = 'welcome'
jdbc_driver = "com.mysql.jdbc.Driver"


properties = {
    "driver": jdbc_driver,
    "user": user,
    "password": password
}


# Flatten the struct column
flattened_df = price_trend.select(
    col("window.start").alias("window_start"),
    col("window.end").alias("window_end"),
    col("base"),
    col("total_volume"),
    col("actual_avg"),
    col("price_trend"),
    col("rowNum")
)

# Write the flattened DataFrame to MySQL
flattened_df.write.jdbc(
    url=jdbc_url,
    table="coincap_analysis",
    mode="append",
    properties=properties
)


# COMMAND ----------

# List tables in mysql database

db_name = 'de_001'
table_list = (
    spark.read.format("jdbc")
    .option("driver", jdbc_driver)
    .option("url", jdbc_url)
    .option("dbtable", "information_schema.tables")
    .option("user", user)
    .option("password", password)
    .load()
    .filter(f"table_schema = '{db_name}'")
    .select("table_name")
)

table_list.show()


# COMMAND ----------

#Read table from mysql database through jdbc

df_coincap = (
    spark.read.format("jdbc")
    .option("driver", jdbc_driver)
    .option("url", jdbc_url)
    .option("dbtable", "coincap_analysis")
    .option("user", user)
    .option("password", password)
    .load()
)

df_coincap.show(truncate=False)
print(df_coincap.count())

# COMMAND ----------

df_coincap.count()
