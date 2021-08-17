from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = "abc"


SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="YashValod",
    password="toor12345",
    hostname="YashValod.mysql.pythonanywhere-services.com",
    databasename="YashValod$default",
)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://YashValod:toor12345@YashValod.mysql.pythonanywhere-services.com/YashValod$default'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Grocery(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    shopname = db.Column(db.String(100), nullable=False)

    def __init__(self, name, company, quantity, shopname):
        self.name = name
        self.company = company
        self.quantity = quantity
        self.shopname = shopname


@app.route('/')
def index():
    data_grocery = db.session.query(Grocery)
    return render_template('index.html', data=data_grocery)


@app.route('/input', methods=['GET', 'POST'])
def input_data():
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        quantity = request.form['quantity']
        shopname = request.form['shopname']

        add_data = Grocery(name, company, quantity, shopname)

        db.session.add(add_data)
        db.session.commit()

        flash("Input Data Success")

        return redirect(url_for('index'))

    return render_template('input.html')


@app.route('/edit/<int:id>')
def edit_data(id):
    data_grocery = Grocery.query.get(id)
    return render_template('edit.html', data=data_grocery)


@app.route('/proses_edit', methods=['POST', 'GET'])
def proses_edit():
    data_grocery = Grocery.query.get(request.form.get('id'))

    data_grocery.name = request.form['name']
    data_grocery.company = request.form['company']
    data_grocery.quantity = request.form['quantity']
    data_grocery.shopname = request.form['shopname']

    db.session.commit()

    flash('Edit Data Success')

    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    data_grocery = Grocery.query.get(id)
    db.session.delete(data_grocery)
    db.session.commit()

    flash('Delete Data Success')

    return redirect(url_for('index'))