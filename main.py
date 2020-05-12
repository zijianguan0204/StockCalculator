from flask import Flask, render_template, flash
from forms import CalculateForm, realTimeInfoForm, invsForm
from alpha_vantage.timeseries import TimeSeries
import datetime
import yfinance as yf
import requests

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
    input_amount = 0
    invs_method = ''
    result = ""
    form = invsForm()
    if form.validate_on_submit():
        input_amount = form.input_amount.data
        invs_method = form.invs_method.data
        if (invs_method == "Ethical Investing"):
            result = "You can chose Tesla (TSLA)\n Sunrun (RUN) \n General Electric (GE)"
            result = getApiResult("IBM")
        elif (invs_method == 'Growth Investing'):
            result = "You can chose Amazon (AMZN)\n Veera System (VEEV) \n Shopify (SHOP)"
        elif (invs_method == "Index Investing"):
            result = "You can chose Fidelity ZERO Large Cap Index(FNILX)\n Vanguard S&P 500 ETF(VOO) \n SPDR S&P 500 ETF Trust(SPY)"
        elif (invs_method == "Quality Investing"):
            result = "You can spend " +str(0.3* input_amount) + " on Apple (APPL) and " +str(0.5* input_amount)+ "on Amazon (AMZN) and " +str(0.1* input_amount) + "on Zoom (ZM)"
            result += "The current value is "
            result += "The weekly trend of the portfolio value"
        elif (invs_method == "Value Investing"):
            result = "You can chose Apple (APPL)\n Adobe (ADBE) \nNestle (NSRGY)"
        else:
            result = "Plese enter a valid strategy method"

        #calculations and algorithm down here.............
        #result = "Here is the result..."

    else:
        flash('calculator failed')
    return render_template('invs.html', title='Invs', form=form, result=result)

def getApiResult(symbol):
    url = "https://www.alphavantage.co/query"
    #Taylor's
    #apikey = "AQBRXZ79TA0OFHR3"
    #Zijian's
    apikey = "7NQ5H1FQHLLH7JFC"
    function = "TIME_SERIES_DAILY"
    params = {'function': function, 'symbol':symbol, 'apikey': apikey}
    r = requests.request('GET', url, params=params).json()
    data = r["Time Series (Daily)"]["2020-05-11"]
    return data

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
