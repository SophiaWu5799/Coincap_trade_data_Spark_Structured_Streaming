# Real-time Cryptocurrency Analytics with Spark Structured Streaming 
## Project Original Thoughts:
Have you been confused by the volatility of the cryptocurrency market and struggled to make sense of its rapid price fluctuations? With the increasing popularity of Bitcoin and Ethereum, more people are becoming interested in trading these digital assets, but it can be difficult to know when to buy or sell.

This is where our project, Spark Structured Streaming for Coincrpty, comes in. By using real-time data from CoinCap API via websockets, we are able to stream the latest trading information for a large amount of cryptocurrency and process it using Spark structured streaming in order to create a dashboard that visualizes the data in an easily digestible format. This project aims to help traders and investors make informed decisions by providing them with up-to-date information on market trends and price movements.
  
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

## Conclusion:

In conclusion, the Spark Structured Streaming for CoinCrpty project is a great example of a data engineering project that uses real-time data to provide insights and analysis for cryptocurrency trading. By utilizing the CoinCap API and Apache Spark's Structured Streaming, we were able to process and analyze large volumes of streaming data, and store the results in MySQL for further analysis and visualization using Tableau.

This project has the potential to benefit both individual traders and businesses involved in cryptocurrency trading by providing them with real-time insights into market trends and fluctuations. Furthermore, this project can serve as a starting point for those interested in exploring data engineering and real-time data processing using Spark and other related tools.

Overall, this project showcases the power and potential of data engineering and real-time data processing in the cryptocurrency market, and serves as a valuable resource for anyone looking to gain insights and make informed decisions in this rapidly evolving industry.





