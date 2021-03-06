import logging
import json

from flask import request, jsonify;

from codeitsuisse import app;

logger = logging.getLogger(__name__)

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
    logging.info("My profit :{}".format(profit_res))
    logging.info("My result :{}".format(output_res))
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
    length = (energy//2) *2
    prices_go = stock['price'][-length//2:]
    prices_back = stock['price'][-length//2::-1]
    qtys = stock['qty'][-length:]
    prices = prices_go +  prices_back
    result = {}
    # inital 
    for i in range(min(qtys[0],int(capital/prices_go[0]))+1):
        result = { i:[-i*prices[0] for _ in range(length)],'qty'+str(i): [ j for j in qtys]}
        result['qty'+str(i)][0] -= i
    
    # dp 
    for i in range(1,length): # for every year
        for j in range(len(result)): # for diferent result 
            money = result[j][i-1] # money you have 
            price = prices[i]
            buy_amount = min( money // price, result['qty'+str(i)][i%(length//2)])
            temp_list = [result[k][i-1] + (j-k) * price[i] for k in range(len(result)) ]
            result[j][i] =  max(temp_list) # this year 
            result['qty'+str(j)][i%(length//2)] -= (j-temp_list.index(result[j][i])) if  (j-temp_list.index(result[j][i])) > 0 else 0
            if j + buy_amount > len(result) :
                for k in range(j + buy_amount - len(result)):
                    result[j+k] = [ _ for _ in result[j] ]
                    result[j+k][i] = result[j+k][i] - (k+1)*price
                    result['qty'+str(j)] = [_ for _ in result[j]]
                    result['qty'+str(j)] -= k+1
        if len(result) == 0:
            for i in range(min(qtys[0],int(capital/prices_go[0]))+1):
                result = { i:[-i*prices[0] for _ in range(length)],'qty'+str(i): [ j for j in qtys]}
                result['qty'+str(i)][0] -= i
    
    return result[0][length-1],result['qty0']



    


