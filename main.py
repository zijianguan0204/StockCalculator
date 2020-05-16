from flask import Flask, render_template, flash,url_for
from forms import CalculateForm, realTimeInfoForm, invsForm
from alpha_vantage.timeseries import TimeSeries
import datetime
import yfinance as yf
import requests
from datetime import date, timedelta
import os
import json
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/", methods=['GET', 'POST'])
def calculator():
    proceeds = 0
    cost = 0
    net_profit = 0
    return_on_inv = 0
    break_piece = 0
    form = CalculateForm()
    if form.validate_on_submit():
        symbol = form.symbol.data
        allotment = form.allotment.data
        final_sell_price = form.final_share_price.data
        sell_commission = form.sell_commission.data
        initial_sell_price = form.initial_share_price.data
        buy_commission = form.buy_commission.data
        tax = form.tax.data

        proceeds = allotment * final_sell_price
        cost = (proceeds - allotment * initial_sell_price - buy_commission - sell_commission) * tax + allotment * initial_sell_price + buy_commission + sell_commission
        net_profit = proceeds - cost
        return_on_inv = net_profit / cost
        break_piece = (allotment * initial_sell_price + buy_commission + sell_commission) / allotment
    else:
        flash('calculator failed')
    return render_template('calculator.html', title='Calculator', form=form, proceeds=proceeds, cost=cost,
                           net_profit=net_profit, return_on_inv=return_on_inv, break_piece=break_piece)

@app.route("/realTimeInfo", methods=['GET', 'POST'])
def realTimeInfo():

    api_key = '7NQ5H1FQHLLH7JFC'

    symbol = 'MSFT'
    date_time = 'No date...'
    output = 'No output here...'
    company_name = 'No Company...'
    form = realTimeInfoForm()
    if form.validate_on_submit():
        symbol = form.symbol.data
        ts = TimeSeries(key=api_key, output_format='pandas')
        try:
            data, meta_data = ts.get_intraday(symbol=symbol, interval = '60min', outputsize = 'full')
            close_data = data['4. close']
            open_data = data['1. open']
            date_time = datetime.datetime.now()
            initial_price = open_data[-1]
            final_price = close_data[-1]
            value_changes = final_price - initial_price
            percent_change = (final_price - initial_price)/initial_price*100

            tickerdata = yf.Ticker(symbol)
            tickerinfo = tickerdata.info
            company_name = tickerinfo['shortName']

            if value_changes > 0:
                output = str(initial_price) +' +'+ str(value_changes) + ' +' + str(percent_change) + '%'
            if value_changes < 0:
                output = str(initial_price) +' '+ str(value_changes) + ' ' + str(percent_change) + '%'
            print(company_name)
            print(date_time)
            print(output)

        except:
            print("No such symbol..")
    else:
        flash('Getting real info failed')
    return render_template('realTimeInfo.html', title='realTimeInfo', form=form, symbol=symbol, date_time=date_time, output=output, company_name = company_name)


def checkSecondmethod(method):
    if (method == "Ethical Investing" or method == 'Growth Investing' or  method == "Index Investing" or method == "Value Investing"):
        return True
    else:
        return False


def getValueList(invs_method,input_amount,portion,company,symbolList):
    m = invs_method.split()[0]
    companyList = company[m]
    portionList= portion[m]
    symol_1 = getJsonResult(symbolList[m][0])
    symol_2 = getJsonResult(symbolList[m][1])
    symol_3 = getJsonResult(symbolList[m][2])
    valueList = profileValue(input_amount,symol_1, symol_2, symol_3, portionList)
    return valueList, companyList, portionList
    
    

#This is the function we should work on
@app.route("/invs", methods=['GET', 'POST'])
def invs():
    companyList = []
    portionList = []
    companyList2 = []
    portionList2 = []
    valueList = []
    valueList2 = []
    company = {"Ethical":["Tesla (TSLA)","Sunrun (RUN)","General Electric (GE)"],"Growth":["Amazon (AMZN)","Veera System (VEEV)","Shopify (SHOP)"],"Quality":
               ["Apple (AAPL)","Amazon (AMZN)","Zoom (ZM)"],"Index":["iShares Core S&P 500 ETF (IVV)","Vanguard S&P 500 ETF(VOO)","SPDR S&P 500 ETF Trust(SPY)"],"Value":["Google (GOOG)","Netflix (NFLX)","NVIDIA(NVDA)"]}
    symbolList = {"Ethical":["TSLA","RUN","GE"],"Growth":["AMZN","VEEV","SHOP"],"Quality":
                 ["AAPL","AMZN","ZM"],"Index":["IVV","VOO","SPY"],
                 "Value":["GOOG","NFLX","NVDA"]}

    portion = {"Ethical":np.random.multinomial(100, np.ones(3)/3, size=1)[0],"Growth":np.random.multinomial(100, np.ones(3)/3, size=1)[0],"Quality":
               [30,40,30],"Index":[60,30,10],"Value":[60,30,10]}
    profit=0
    input_amount = 0
    invs_method = ''
    invs_method_opt = ''
    result = ""
    form = invsForm()
    
    if form.validate_on_submit():
        input_amount = form.input_amount.data
        invs_method = form.invs_method.data
        invs_method_opt = form.invs_method_opt.data
        
        if (checkSecondmethod(invs_method_opt)):
            input_amount = input_amount/2
            valueList2, companyList2,portionList2 = getValueList(invs_method_opt,input_amount,portion,company,symbolList)            
            
        if (invs_method == "Ethical Investing"):
            companyList = company["Ethical"]
            portionList= portion["Ethical"]
            tsla = getJsonResult("TSLA")
            run = getJsonResult("RUN")
            ge = getJsonResult("GE")
            valueList = profileValue(input_amount, tsla, run, ge, portionList)    
        elif (invs_method == 'Growth Investing'):
            companyList = company["Growth"]
            portionList= portion["Growth"]
            amzn = getJsonResult("AMZN")
            veev = getJsonResult("VEEV")
            shop = getJsonResult("SHOP")
            valueList = profileValue(input_amount, amzn, veev, shop, portionList) 
        elif (invs_method == "Index Investing"):
            companyList = company["Index"]
            portionList= portion["Index"]
            amzn = getJsonResult("AMZN")
            veev = getJsonResult("VEEV")
            shop = getJsonResult("SHOP")
            valueList = profileValue(input_amount, amzn, veev, shop, portionList)
        elif (invs_method == "Quality Investing"):
            companyList = company["Quality"]
            portionList= portion["Quality"]
            appl = getJsonResult("AAPL")
            amzn = getJsonResult("AMZN")
            zm = getJsonResult("ZM")
            valueList = profileValue(input_amount, appl, amzn, zm, portionList)
        elif (invs_method == "Value Investing"):
            companyList = company["Value"]
            portionList= portion["Value"]
            goog = getJsonResult("GOOG")
            nflx = getJsonResult("NFLX")
            nvda = getJsonResult("NVDA")
            valueList = profileValue(input_amount, goog, nflx, nvda, portionList)
        else:
            result = "Plese enter a valid strategy method"
            method1 = ""
            method2 = ""
                     
        profit = getProfit(input_amount, valueList, valueList2)
        days = [1,2,3,4,5]
        #plt.plot(days, valueList)
        #plt.xlabel('days')
        #plt.ylabel('Prices')
        #plt.title('Price vs. Days')
        #plt.savefig('static/graph.png')


        #calculations and algorithm down here.............
        #result = "Here is the result..."

    else:
        flash('calculator failed')
    return render_template('invs.html', title='Invs', form=form, method1 = invs_method, method2 = invs_method_opt, result=result,
                           companyList=companyList,portionList=portionList,companyList2=companyList2,portionList2=portionList2,
                           valueList = valueList,valueList2 = valueList2, profit = profit)

def getJsonResult(symbol):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, symbol+".json")
    r = json.load(open(json_url))
    data=[]
    #dt = date.today()
    date_time_str = '2020-05-13'   #write todays date
    date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
    dt = date_time_obj.date()
    for i in range(5):
        dt = getMostRecentBusinessDay(dt)
        data.append( r["Time Series (Daily)"][str(dt)]["4. close"] )
    return list(reversed(data))

def getApiResult(symbol):
    url = "https://www.alphavantage.co/query"
    #Taylor's
    #apikey = "AQBRXZ79TA0OFHR3"
    #Zijian's
    apikey = "7NQ5H1FQHLLH7JFC"
    function = "TIME_SERIES_DAILY"
    params = {'function': function, 'symbol':symbol, 'apikey': apikey}
    r = requests.request('GET', url, params=params).json()
    
    data=[]
    dt = date.today()
    for i in range(5):
        dt = getMostRecentBusinessDay(dt)
        data.append( r["Time Series (Daily)"][str(dt)]["4. close"] )
    return list(reversed(data))

def getMostRecentBusinessDay(today):
    offset = max(1, (today.weekday() + 6) % 7 - 3)
    most_recent = today - timedelta(offset)
    return most_recent

def profileValue(money, list1, list2, list3, portionList):
    portion1 = portionList[0] * money * 0.01
    portion2 = portionList[1] * money * 0.01
    portion3 = portionList[2] * money * 0.01
    result = []
    result.append(money)
    for i in range(1, len(list1)):
        value = portion1 * float(list1[i]) / float(list1[0]) + portion2 * float(list2[i]) / float(list2[0])+ portion3 * float(list3[i]) / float(list3[0])
        result.append(round(value,2))
    return result

def getProfit(input_amount, valueList1, valueList2):
    profit = 0
    if(len(valueList1) > 1):
        profit = valueList1[4] - input_amount 
    if(len(valueList2) > 1):
        profit += valueList2[4] - input_amount 
    return round(profit, 2)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
