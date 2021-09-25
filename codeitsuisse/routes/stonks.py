import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)
""""2037":{
     "Apple":{
       "price":100,
       "qty":10
     }
   },
   "2036":{
     "Apple":{
       "price":10,
       "qty":50"""

@app.route('/stonks', methods=['POST'])
def evaluate():
    data = request.get_json();
    logging.info("data sent for evaluation {}".format(data))
    energy = data.get("energy");
    capital = data.get("capital");
    timeline = data.get("timeline");
    stocks_dic = getprice(timeline)
    profit_res,output_res = 0,None
    for stock in stocks_dic.keys():
        profit,output = maxprofit(energy,capital,stocks_dic[stock])
        if profit > profit_res:
            profit_res,output_res = profit,output
    

    logging.info("My profit :{}".format(profit))
    logging.info("My result :{}".format(output))
    return json.dumps(output);
def getprice(timeline):
    stocks_dic = {}
    for i in timeline['2037'].keys():
        stocks_dic[i] = {'price':[],'qty':[]}
    for year,stocks in timeline.items():
        for stock in stocks.keys():
            stocks_dic[stock]['price'].append(stocks[stock]['price'])
            stocks_dic[stock]['qty'].append(stocks[stock]['qty'])
    return  stocks_dic

def maxprofit(energy,capital,stock):
    # TODO pretend only one stock
    len = energy // 2
    prices_go = stock['price'][-len:]
    prices_back = stock['price'][-len::-1]
    qtys_go = stock['qty'][-len:]

    result = {}
    # inital 
    amount = min(qtys[0],int(capital/prices[0]))
    result = { 0:[-i*prices[0] for _ in range(len)]}
    
    # dp 
    for i in range(len):
        for j in range(len(result)):
        result[]
    for(int i = 1; i < n; i++){             
        dp0[i] = max(dp0[i-1], dp1[i-1] + prices[i]);
        dp1[i] = max(dp1[i-1], dp0[i-1] - prices[i]);
    }


    


