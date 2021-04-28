# Using API Wrapper to fetch and predict Stock Opening prices for Companies.

A custom API wrapper is built for Alphavantage API to query for historic day-wise stock market opening prices for each company. The wrapper fetches the data which is then formatted and sent as the body to the /forecast method of Unplugg API which performs time-series prediction on the formatted stock opening price data and provides the response on the public callback URL. The response which are the predictions are then read and displayed on a HTML page. The HTML page provides options to select a company and view the stock market opening prices prediction for that company.

## Setup

Populate the .env file:

1. CALLBACK_URL -  Should be a public URL to be used as a Webhook where the response from the Unplugg API will be obtained. ngrok can be used for testing. 

2. STOCK_API_KEY - Alphavantage API is being used to obtain the historic stock data. You can register to Alphavantage API to obtain an api_key

3. UNPLUGG_API_KEY - Unplugg is being used to forecast the stock market opening price when the historic time-series data is provided. Unplugg api_key can be obtained by registering at the website. 

### Running the code

The code can be run by running the flask server by using the below command:

```flask run --host=0.0.0.0```

### HTML Page

![Alt text](/homepage.png?raw=true "HTML Page")

