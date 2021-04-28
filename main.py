from flask import Flask, request, Response, render_template, redirect, url_for
from datetime import datetime, timezone
import json
import time
import os

app = Flask(__name__)

#Route which receives the webhook response from the unplugg API
@app.route('/webhook', methods=['POST'])
def respond():
    result = request.json
    final_stock_predictions = {"data": []}
    for prediction in result["forecast"]:
        stock_predictions = {}
        future_date = datetime.utcfromtimestamp(prediction["timestamp"]).strftime("%Y-%m-%d")
        stock_predictions[future_date] = prediction["value"]
        final_stock_predictions["data"].append(stock_predictions)
        #print(final_stock_predictions)
        with open('data.txt', 'w') as outfile:
            json.dump(final_stock_predictions, outfile)   
    f = open("semaphore.txt", "w")
    f.write("1")
    f.close()
    print("Webhook data received")
    return Response(status=200)

#Landing page route
@app.route('/')
def home():
    with open('data.txt') as json_file:
        data = json.load(json_file)
    f = open("company_name.txt", "r")
    company_name = f.read()
    f.close()
    return render_template('home.html', data=data, company_name=company_name)

#Route for the fetch button which uses the stock API wrapper and gets the historic stock data for the company and then calls the Unplugg API
@app.route('/button', methods = ["POST", "GET"])
def use_stock_wrapper():
    from stock_wrapper import StockAPI
    import requests
    UNPLUGG_API_KEY = os.getenv("UNPLUGG_API_KEY")

    #Receiving company name from the drop-down from HTML
    req = request.form
    company_name = req.get("Company")

    #Using the custom stock API Wrapper to receive the stock data for the requested company
    StockInstance = StockAPI(company_name)
    result = StockInstance.info()

    date_list = list(result["Time Series (Daily)"].keys())

    payload = {}
    all_date_list = []

    for each_date in date_list:
        each_date_dict = {}
        each_date_dict["timestamp"] = int(datetime.strptime(each_date, '%Y-%m-%d').replace(tzinfo=timezone.utc).timestamp())
        each_date_dict["value"] = float(result["Time Series (Daily)"][each_date]["1. open"])
        all_date_list.append(each_date_dict)

    #Payload has been made and has to be sent as a POST request to the Unplugg API
    payload["data"]= all_date_list

    #URL where the response is received and has to be a public URL {Using ngrok for testing}
    payload["callback"]= os.getenv("CALLBACK_URL")

    #Sending out the POST request to Unplugg API
    payload = json.dumps(payload)
    url="https://api.unplu.gg/forecast"
    unplugg_response = requests.post(url, data = payload, headers = {"x-access-token": UNPLUGG_API_KEY, "content-type": "application/json"})

    #Waiting until the webhook receives the response from the API
    f = open("semaphore.txt", "r")
    sem_value = f.read()
    f.close()
    while (int(sem_value) !=1):
        f = open("semaphore.txt", "r")
        sem_value = f.read()
        print("Waiting for the webhook to receive the response from Unplugg API")
        time.sleep(0.1)
        f.close()
    f = open("semaphore.txt", "w")
    f.write("0")
    f.close()
    f = open("company_name.txt", "w")
    f.write(company_name)
    f.close()

    #Sending the Unplugg API response to the html file 
    with open('data.txt') as json_file:
        data = json.load(json_file)
    return redirect(url_for('home', data=data, company_name=company_name))
