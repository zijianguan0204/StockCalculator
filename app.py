from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, CalculateForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/calculate", methods=['GET', 'POST'])
def calculate():
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

        proceeds = allotment*final_sell_price
        cost = allotment*initial_sell_price+buy_commission+sell_commission+tax*proceeds
        net_profit = proceeds - cost
        return_on_inv = net_profit/cost
        break_piece = net_profit/allotment
        print(tax)
    else:
        flash('calculator failed')
    return render_template('calculator.html', title='Calculator', form=form, proceeds=proceeds, cost=cost, net_profit=net_profit, return_on_inv=return_on_inv, break_piece=break_piece)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
