from operator import truediv
import unittest
import handler
import mortgage_classes as mc
import full_calculator_mock as fcm
import stamp_duty
import json
from pydantic import parse_obj_as
from py_event_mocks import create_event
import calculators as calc
class TestStringMethods(unittest.TestCase):

    def test_mortgage_payments(self):
        
        for request in requests:
            mortgage = parse_obj_as(mc.BasicCalculatorRequest,request["request"])
            # mortgage = request["request"]
            body = calc.mortgage_payments(mortgage)
            self.assertEqual(round(body.monthly_payment),round(request["answer"]))
            
    def test_remaining_equity(self):
        
        for request in remaining_equity_requests:
            mortgage = parse_obj_as(mc.RemainingEquityRequest,request["request"])
            # mortgage = request["request"]
            body = calc.remaining_equity(mortgage)
            self.assertEqual(round(body.remaining_equity),round(request["answer"]))
    
    def test_stamp_duty(self):
        
        for request in stamp_duty_requests:
            
            body = stamp_duty.duty_calculator(request["request"])
            self.assertEqual(round(body),round(request["answer"]))
    
    def test_mortgage_needed(self):
        
        for request in mortgage_needed_request:
            figures = parse_obj_as(mc.HowMuchMortgageRequest,request["request"])
            body = calc.how_much_mortgage_do_i_need(figures)
            self.assertEqual(round(body.total_mortgage_needed),round(request["answer"]))

    def test_mortgage_mount(self):
        
        for request in mortgage_amount_request:
            figures = parse_obj_as(mc.AmountCalculatorRequest,request["request"])
            body = calc.mortgage_amount(figures)
            self.assertEqual(round(body.loan_amount),round(request["answer"]))
    
    def test_full_calculator(self):
        i = 0
        for request in fcm.requests:
            obj = parse_obj_as(mc.FullCalculatorRequest,request)
            body = calc.full_calculator(obj)
            self.assertEqual(body.details_with_ported_mortgage.mortgage_one_details.monthly_payment,fcm.responses[i]["details_with_ported_mortgage"]["mortgage_one_details"]["monthly_payment"])
   
    def test_payment_to_amounts(self):
        i = 0
        
        body = calc.payments_to_amounts_calculator(mc.MaxAmountCalculatorRequest())
        self.assertIsNotNone(body)
   
    
requests = [
    {"request":mc.BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=21,loan_amount=350000,fixed_term_rate=1.11,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":1558},
    {"request":mc.BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=10,loan_amount=360000,fixed_term_rate=3,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":3476},
    {"request":mc.BasicCalculatorRequest(fixed_term_rate_years=5,loan_term_years=20,loan_amount=500000,fixed_term_rate=3.5,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":2899.80}
]

remaining_equity_requests = [
    {"request":mc.RemainingEquityRequest(mortgage_remaining=355000,house_price_sale=700000,debt_to_pay_off=45000,estate_agent_commission=1,pay_stamp_duty=True).dict(),"answer":291600},
    {"request":mc.RemainingEquityRequest(mortgage_remaining=400000,house_price_sale=750000,debt_to_pay_off=20000,estate_agent_commission=1,pay_stamp_duty=True).dict(),"answer":321000}
]

mortgage_needed_request = [
    {"request":mc.HowMuchMortgageRequest(house_price_to_buy=700000,remaining_equity=300000,use_remaining_equity_for_duty=True).dict(),"answer":375000},
    
]

mortgage_amount_request = [
    {"request":mc.AmountCalculatorRequest(loan_term_years=20,monthly_payment=3107,fixed_term_rate=3.38).dict(),"answer":541466},
    {"request":mc.AmountCalculatorRequest(loan_term_years=20,monthly_payment=5000,fixed_term_rate=4).dict(),"answer":825109},
]

full_calculator_requests = [
    {"request":mc.FullCalculatorRequest(
     house_price_to_sell= 675000,
    house_price_to_buy= 900000,
    current_mortgage= 352000,
    estate_agent_commission= 1,
    mortgage_one_rate= 1.1,
    mortgage_one_fixed_term= 1.5,
    mortgage_one_fixed_term_rate= 6,
    new_mortgage_rate= 4,
    new_mortgage_fixed_term= 2,
    new_mortgage_post_fixed_term_rate= 6,
    current_mortgage_term= 20,
    new_mortgage_term= 20,
    debts_to_pay_off= 45000,
    early_repayment_fee=7000,
    use_equity_to_pay_duty= True),"answer":1473.14},
    
]

stamp_duty_requests = [
    {"request":700000,"answer":25000},
    
]  

if __name__ == '__main__':
    unittest.main()