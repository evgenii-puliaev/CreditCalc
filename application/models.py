class BankOffer(object):
    def __init__(self, bank_name, tariff_name, credit_amount_range, time_range, rate):
        self.bank_name = bank_name
        self.tariff_name = tariff_name
        self.credit_amount_range = credit_amount_range
        self.time_range = time_range
        self.rate = rate


class CreditInfo(object):
    def __init__(self, credit_amount, rate, time, overpayment, total_payout):
        self.credit_amount = credit_amount
        self.rate = rate
        self.time = time
        self.overpayment = overpayment
        self.total_payout = total_payout


class MonthlyPaymentInfo(object):
    def __init__(self, monthly_payment_amount, repayment_of_principal, interest_payment, left_to_pay):
        self.monthly_payment_amount = monthly_payment_amount
        self.repayment_of_principal = repayment_of_principal
        self.interest_payment = interest_payment
        self.left_to_pay = left_to_pay
