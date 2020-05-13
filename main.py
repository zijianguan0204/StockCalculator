from flask import Flask, render_template, flash,url_for
from forms import CalculateForm, realTimeInfoForm, invsForm
from alpha_vantage.timeseries import TimeSeries
import datetime
import yfinance as yf
import requests
from datetime import date, timedelta
import os
import json

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


#This is the function we should work on
@app.route("/invs", methods=['GET', 'POST'])
def invs():
    companyList = []
    portionList = []
    valueList = []
    resultDict = {1:"haha",2:"xixi"}
    company = {"Ethical":["Tesla (TSLA)","Sunrun (RUN)","General Electric (GE)"],"Growth":["Amazon (AMZN)","Veera System (VEEV)","Shopify (SHOP)"],"Quality":
               ["Apple (APPL)","Amazon (AMZN)","Zoom (ZM)"],"Index":["iShares Core S&P 500 ETF (IVV)","Vanguard S&P 500 ETF(VOO)","SPDR S&P 500 ETF Trust(SPY)"],"Value":["Google (GOOG)","Netflix (NFLX)","NVIDIA(NVDA)"]}
    portion = {"Ethical":[30,40,30],"Growth":[30,40,30],"Quality":
               [30,40,30],"Index":[60,30,10],"Value":[60,30,10]}
    input_amount = 0
    invs_method = ''
    result = ""
    form = invsForm()
    if form.validate_on_submit():
        input_amount = form.input_amount.data
        invs_method = form.invs_method.data
        if (invs_method == "Ethical Investing"):
            companyList = company["Ethical"]
            portionList= portion["Ethical"]
            tsla = getJsonResult("TSLA")
            run = getJsonResult("RUN")
            ge = getJsonResult("GE")
            valueList = profileValue(100, tsla, run, ge, portionList)
        elif (invs_method == 'Growth Investing'):
            companyList = company["Growth"]
            portionList= portion["Growth"]
            amzn = getJsonResult("AMZN")
            veev = getJsonResult("VEEV")
            shop = getJsonResult("SHOP")
            valueList = profileValue(100, amzn, veev, shop, portionList) 
        elif (invs_method == "Index Investing"):
            companyList = company["Index"]
            portionList= portion["Index"]
            amzn = getJsonResult("AMZN")
            veev = getJsonResult("VEEV")
            shop = getJsonResult("SHOP")
            valueList = profileValue(100, amzn, veev, shop, portionList)
        elif (invs_method == "Quality Investing"):
            companyList = company["Quality"]
            portionList= portion["Quality"]
            appl = getJsonResult("APPL")
            amzn = getJsonResult("AMZN")
            zm = getJsonResult("ZM")
            valueList = profileValue(100, appl, amzn, zm, portionList)
        elif (invs_method == "Value Investing"):
            companyList = company["Value"]
            portionList= portion["Value"]
            goog = getJsonResult("GOOG")
            nflx = getJsonResult("NFLX")
            nvda = getJsonResult("NVDA")
            valueList = profileValue(100, goog, nflx, nvda, portionList)
        else:
            result = "Plese enter a valid strategy method"

        #calculations and algorithm down here.............
        #result = "Here is the result..."

    else:
        flash('calculator failed')
    return render_template('invs.html', title='Invs', form=form, result=result,
                           resultDict = resultDict,companyList=companyList,portionList=portionList,valueList = valueList)

def getJsonResult(symbol):
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, symbol+".json")
    r = json.load(open(json_url))
    data=[]
    dt = date.today()
    dt = getMostRecentBusinessDay(dt)
#     date_time_str = '2020-05-12'
#     dt = datetime.datetime.strptime(date_time_str, '%Y-%m-%d')
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
