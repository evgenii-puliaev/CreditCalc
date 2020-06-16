from application.models import CreditInfo, MonthlyPaymentInfo, BankOffer


def count_ann_credit(credit_amount: int, time: int, rate: float):
    credit_amount = int(credit_amount)
    time = int(time)
    rate = float(rate)

    month_rate = rate / 12 / 100.
    ann_coeff = (month_rate * ((1 + month_rate) ** time)) / (((1 + month_rate) ** time) - 1)

    monthly_payment = float(format(credit_amount * ann_coeff, '.2f'))
    total_payout = float(format(monthly_payment * time, '.2f'))
    overpayment = float(format(total_payout - credit_amount, '.2f'))

    table = []
    left_to_pay = total_payout
    for i in range(time):
        left_to_pay -= monthly_payment
        interest_payment = float(format(left_to_pay * month_rate, '.2f'))
        table.append(MonthlyPaymentInfo(
            monthly_payment,
            float(format(monthly_payment - interest_payment, '.2f')),
            interest_payment,
            float(format(left_to_pay, '.2f'))
        ))

    return CreditInfo(credit_amount, rate, time, overpayment, total_payout), table


def count_dif_credit(credit_amount: int, time: int, rate: float):
    credit_amount = int(credit_amount)
    time = int(time)
    rate = float(rate)

    repayment_of_principal = credit_amount / time
    left_to_pay = credit_amount
    total_payout = 0
    table = []

    for i in range(time):
        interest_payment = left_to_pay * (rate / 100) * (30 / 365)
        payment = repayment_of_principal + interest_payment
        total_payout += payment
        left_to_pay -= repayment_of_principal
        table.append(MonthlyPaymentInfo(
            float(format(payment, '.2f')),
            float(format(repayment_of_principal, '.2f')),
            float(format(interest_payment, '.2f')),
            float(format(left_to_pay, '.2f'))
        ))

    return CreditInfo(
        credit_amount,
        rate,
        time,
        float(format(total_payout - credit_amount, '.2f')),
        float(format(total_payout, '.2f'))
    ), table


def find_bank_offers(credit_amount, time, rate, credit_type):
    result = []
    all_banks = [
        BankOffer('Закрытие', 'Льготный', range(350_000, 850_001), range(12, 19), 9),
        BankOffer('Закрытие', 'Основной', range(500_000, 1_500_001), range(6, 36), 12),
        BankOffer('Тинькон', 'Льготный', range(500000, 2000001), range(12, 37), 8.7),
        BankOffer('Тинькон', 'Стандарт', range(350000, 2500001), range(6, 37), 15),
        BankOffer('Бета-банк', 'Молодежный', range(250000, 1000001), range(6, 25), 9.2),
        BankOffer('Бета-банк', 'Бизнес', range(1500000, 3500001), range(18, 37), 16),
        BankOffer('Растратбанк', 'Для семьи', range(500000, 2500001), range(12, 49), 12)
    ]
    # можно прикрутить бд (например sqlalchemy) и залить туда все банки с тарифами и не только их (пока сделал через массив)

    for bank in all_banks:
        if int(credit_amount) in bank.credit_amount_range and int(time) in bank.time_range:
            if credit_type == 'ann':
                result.append({'bank': bank, 'info': count_ann_credit(credit_amount, time, rate)[0]})
            elif credit_type == 'dif':
                result.append({'bank': bank, 'info': count_dif_credit(credit_amount, time, rate)[0]})

    def by_rate_key(this_bank_offer):
        return abs(float(this_bank_offer['bank'].rate) - float(rate))

    result.sort(key=by_rate_key)

    return result
