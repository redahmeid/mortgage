import unittest
import handler
import json
from pydantic import parse_obj_as
from py_event_mocks import create_event
class TestStringMethods(unittest.TestCase):

    def test_mortgage_payments(self):
        
        for request in requests:
            mortgage = parse_obj_as(handler.BasicCalculatorRequest,request["request"])
            # mortgage = request["request"]
            body = handler.mortgage_payments(mortgage)
            self.assertEqual(round(body.monthly_payment),round(request["answer"]))

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

    
requests = [
    {"request":handler.BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=21,loan_amount=350000,fixed_term_rate=1.11,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":1558},
    {"request":handler.BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=10,loan_amount=360000,fixed_term_rate=3,rate_after_fixed_term=5.38,extra_repayments=0).dict(),"answer":3476},
]

    

if __name__ == '__main__':
    unittest.main()