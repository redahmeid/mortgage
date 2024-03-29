import json
import numpy as np
from pydantic import parse_obj_as
from mortgage_classes import BasicCalculatorRequest, BasicCalculatorResponse, FullCalculatorRequest, FullCalculatorResponse, HowMuchMortgageRequest, HowMuchMortgageResponse, MaxAmountCalculatorOptions, MaxAmountCalculatorRequest,RemainingEquityRequest,RemainingEquityResponse
import stamp_duty
import calculators as calc



def main(event, context):
    body =json.loads(event["body"])
    mortgage = BasicCalculatorRequest(fixed_term_rate_years=body["fixed_term_rate_years"],loan_term_years=body["loan_term_years"],loan_amount=body["loan_amount"],fixed_term_rate=body["fixed_term_rate"],rate_after_fixed_term=body["rate_after_fixed_term"],extra_repayments=body["extra_repayments"])
    result = calc.mortgage_payments(mortgage)
    return {'statusCode': 200,
            'body': result.json(),
            'headers': {'Content-Type': 'application/json'}}

def full_calculator_api(event, context):
    body =json.loads(event["body"])
    full_calculator_request = parse_obj_as(FullCalculatorRequest,body)
    result = calc.full_calculator(full_calculator_request)
    return {'statusCode': 200,
            'body': result.json(),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Credentials" : "true" 
      }}

def payment_to_amount_calculator_api(event, context):
    body =json.loads(event["body"])
    query_parameters = event["queryStringParameters"] if 'queryStringParameters' in event else None
    print("PAYMENT TO AMOUNT")
    print(query_parameters)
    starting_term = query_parameters["starting_term"] if query_parameters is not None and 'starting_term' in query_parameters else None
    increments = query_parameters["increments"] if query_parameters is not None and 'increments' in query_parameters else None
    
    options = MaxAmountCalculatorOptions()
    if starting_term is not None: options.starting_term = int(starting_term)
    if increments is not None: options.increments = int(increments)
    full_calculator_request = parse_obj_as(MaxAmountCalculatorRequest,body)
    result = calc.payments_to_amounts_calculator(full_calculator_request,options)
    return {'statusCode': 200,
            'body': result.json(),
            'headers': {'Content-Type': 'application/json',"Access-Control-Allow-Origin" : "*",
                    "Access-Control-Allow-Credentials" : "true" 
      }}

def full_calculator_head(event, context):
    return_obj = {'statusCode': 200,
            'body': FullCalculatorRequest().json(),
            'headers': {'Content-Type': 'application/json'}}
    print(return_obj)
    return return_obj

def remaining_equity_api(event, context):
    body =json.loads(event["body"])
    request = RemainingEquityRequest(house_price_sale=body["house_price_sale"],mortgage_remaining=body["mortgage_remaining"],debt_to_pay_off=body["debt_to_pay_off"],estate_agent_commission=body["estate_agent_commission"])
    result = calc.remaining_equity(request)
    return {'statusCode': 200,
            'body': result.json(),
            'headers': {'Content-Type': 'application/json'}}



	
if __name__ == "__main__":
    event = {
            "fixed_term_rate_years":2,
            "loan_term_years":21,
            "loan_amount":350000,
            "fixed_term_rate":3.38,
            "rate_after_fixed_term":5,
            "extra_repayments":500
        }
    main(event, '')