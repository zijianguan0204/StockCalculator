from flask import Flask, render_template, flash
from forms import CalculateForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


@app.route("/", methods=['GET', 'POST'])
def home():
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
