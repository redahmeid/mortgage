import unittest
import handler
import mortgage_classes as mc
import stamp_duty
import json
from pydantic import parse_obj_as
from py_event_mocks import create_event

class TestStringMethods(unittest.TestCase):
    def test_api(self):
        
        for request in requests:
            # mortgage = parse_obj_as(handler.BasicCalculatorRequest,)
            event = create_event(
                event_type="aws:api-gateway-event",body={
                    "body":json.dumps(request["request"])
                }
                )
            # mortgage = request["request"]
            response = handler.main(event,None)
            self.assertEqual(round(json.loads(response["body"])["monthly_payment"]),round(request["answer"]))

    def test_full_calculator_api(self):
        
        for request in full_calculator_requests:
            # mortgage = parse_obj_as(handler.BasicCalculatorRequest,)
            event = create_event(
                event_type="aws:api-gateway-event",body={
                    "body":json.dumps(request["request"])
                }
                )
            # mortgage = request["request"]
            response = handler.full_calculator_api(event,None)
            # self.assertIsNotNone(round(json.loads(response["body"])["delayed_loan_amount"]))
            # self.assertEqual(round(json.loads(response["body"])["monthly_payment"]),round(request["answer"]))


    def test_payment_to_amount_calculator_api(self):
        
       
            event = create_event(
                event_type="aws:api-gateway-event",body={
                    "body":json.dumps(mc.MaxAmountCalculatorRequest().dict()),
                    "queryStringParameters":None
                }
                )
            response = handler.payment_to_amount_calculator_api(event,None)
            # self.assertIsNotNone(round(json.loads(response["body"])["delayed_loan_amount"]))
            # self.assertEqual(round(json.loads(response["body"])["monthly_payment"]),round(request["answer"]))


    def test_remaining_equity_api(self):
        
        for request in remaining_equity_requests:
            # mortgage = parse_obj_as(handler.BasicCalculatorRequest,)
            event = create_event(
                event_type="aws:api-gateway-event",body={
                    "body":json.dumps(request["request"])
                }
                )
            # mortgage = request["request"]
            response = handler.remaining_equity_api(event,None)
            self.assertEqual(round(json.loads(response["body"])["remaining_equity"]),round(request["answer"]))
    
    def test_full_calculator_head(self):
        
       
            event = create_event(
                event_type="aws:api-gateway-event"
                )
            # mortgage = request["request"]
            response = handler.full_calculator_head(event,None)
            
            self.assertIsNotNone(json.loads(response["body"]))


requests = [
    {"request":mc.BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=21,loan_amount=350000,fixed_term_rate=1.11,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":1558},
    {"request":mc.BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=10,loan_amount=360000,fixed_term_rate=3,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":3476},
    {"request":mc.BasicCalculatorRequest(fixed_term_rate_years=5,loan_term_years=20,loan_amount=500000,fixed_term_rate=3.5,rate_after_fixed_term=5.38).dict(),"answer":2899.80}
]

remaining_equity_requests = [
    {"request":mc.RemainingEquityRequest(mortgage_remaining=355000,house_price_sale=700000,debt_to_pay_off=45000,estate_agent_commission=1).dict(),"answer":291600},
    {"request":mc.RemainingEquityRequest(mortgage_remaining=400000,house_price_sale=750000,debt_to_pay_off=20000,estate_agent_commission=1).dict(),"answer":321000}
]

mortgage_needed_request = [
    {"request":mc.HowMuchMortgageRequest(house_price_to_buy=700000,remaining_equity=300000,use_remaining_equity_for_duty=True).dict(),"answer":375000},
    
]

stamp_duty_requests = [
    {"request":700000,"answer":25000},
    
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
    use_equity_to_pay_duty= True).dict(),"answer":1473.14},
    
]