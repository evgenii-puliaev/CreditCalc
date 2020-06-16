from collections import namedtuple

from flask import render_template, redirect, url_for, request

from application import app
from application.services import count_ann_credit, find_bank_offers, count_dif_credit

CountResult = namedtuple('CountResult', 'total_payout overpayment table')
Offer = namedtuple('Offer', 'bank_name tariff_name rate overpayment total_payout')

count_result = None
offers = []
credit_types = [
    {'name': 'Аннуитентный', 'val': 'ann'},
    {'name': 'Дифференцированный', 'val': 'dif'}
]
times = [
    {'name': '1 месяц', 'val': '1'},
    {'name': '3 месяца', 'val': '3'},
    {'name': '6 месяцев', 'val': '6'},
    {'name': '9 месяцев', 'val': '9'},
    {'name': '1 год', 'val': '12'},
    {'name': '1.5 года', 'val': '18'},
    {'name': '2 года', 'val': '24'},
    {'name': '3 года', 'val': '36'},
    {'name': '4 года', 'val': '48'},
    {'name': '5 лет', 'val': '60'},
]


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/calculator', methods=['GET'])
def calculator():
    return render_template(
        'calculator.html',
        count_result=count_result,
        offers=offers,
        credit_types=credit_types,
        times=times
    )


@app.route('/count', methods=['POST'])
def count():
    credit_amount = request.form['credit_amount']
    time = request.form['time']
    rate = request.form['rate']
    credit_type = request.form['credit_type']

    info, table = None, None
    if credit_type == 'ann':
        info, table = count_ann_credit(credit_amount, time, rate)
    elif credit_type == 'dif':
        info, table = count_dif_credit(credit_amount, time, rate)
    global count_result
    count_result = CountResult(info.total_payout, info.overpayment, table)

    return redirect(url_for('calculator'))


@app.route('/find_banks', methods=['POST'])
def find_banks():
    credit_amount = request.form['credit_amount']
    time = request.form['time']
    rate = request.form['rate']
    credit_type = request.form['credit_type']

    found_offers = find_bank_offers(credit_amount, time, rate, credit_type)

    global offers
    offers = []
    for found_offer in found_offers:
        info = found_offer['info']
        offer = found_offer['bank']
        offers.append(Offer(
            offer.bank_name,
            offer.tariff_name,
            offer.rate,
            info.overpayment,
            info.total_payout
        ))

    return redirect(url_for('calculator'))
