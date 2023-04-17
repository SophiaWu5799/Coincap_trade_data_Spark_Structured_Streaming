# Real-time Cryptocurrency Analytics with Spark Structured Streaming 
## Project Original Thoughts:
  
## Project Overview
For this data engineering project, I will be working with a live streaming dataset obtained from the CoinCap API using websockets. The goal of this project is to build a real-time data pipeline using Apache Spark's Structured Streaming module, which will process and analyze the incoming data, and store the results in a MySQL database. Additionally, we will be using Tableau to create a dashboard that displays the processed data in an easily digestible format.

## Technical Overview
The project can be broken down into the following components:

1. Data Source: The CoinCap API provides live cryptocurrency trade data through websockets. We will use this API to stream data into our pipeline.

2. Apache Kafka: We will use Apache Kafka as a message broker to receive and distribute the data stream from the CoinCap API. The incoming data will be formatted in JSON, which will be used to feed the Spark Structured Streaming application.

3. Spark Structured Streaming: Using Spark Structured Streaming, we will process and analyze the incoming data from Kafka in real-time. Specifically, we will use the Structured Streaming module to create a streaming application that processes the incoming data, aggregates it in 1-minute tumbling windows, and generates a set of aggregated metrics (e.g., total trade volume, average trade price, etc.) for each 1-minute window. The resulting data will be stored in a MySQL database.

4. MySQL: We will store the processed data in a MySQL database. This will allow us to persist the data and perform ad-hoc queries later on.

5. Tableau: Finally, we will create a dashboard in Tableau that visualizes the processed data. The dashboard will provide an overview of the key metrics that were calculated in the Spark Structured Streaming application.

## Project Approach

1. Data Ingestion: We will use the CoinCap API to stream live cryptocurrency trade data into our pipeline. Specifically, we will use websockets to receive data in real-time.

2. Data Distribution: We will use Apache Kafka to receive and distribute the data stream from the CoinCap API. We will configure Kafka to consume the incoming data as a JSON message, which will be used to feed the Spark Structured Streaming application.

3. Data Processing: We will use Spark Structured Streaming to process and analyze the incoming data in real-time. Specifically, we will create a streaming application that processes the incoming data, aggregates it in 1-minute tumbling windows, and generates a set of aggregated metrics for each window. We will use the Spark SQL module to calculate these metrics, and we will store the results in a MySQL database.

4. Data Visualization: Finally, we will use Tableau to create a dashboard that visualizes the processed data. The dashboard will display key metrics such as total trade volume, average trade price, and price trend over time.

## Project Benefits:

This project will demonstrate a real-world data engineering pipeline for processing and analyzing live streaming data. By working with the CoinCap API, we will be able to build a pipeline that can handle large volumes of data in real-time. Additionally, by using Spark Structured Streaming, we can leverage the power of Apache Spark to perform complex calculations on the incoming data, and store the results in a MySQL database. Finally, by using Tableau to visualize the processed data, we can gain insights into the trends and patterns in the data, which can be used to inform trading decisions.





