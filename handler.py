import json
import numpy as np
from pydantic import BaseModel

def main(event, context):
    print(event)
    body =json.loads(event["body"])
    mortgage = Mortgage(fixed_term_rate_years=body["fixed_term_rate_years"],loan_term_years=body["loan_term_years"],loan_amount=body["loan_amount"],fixed_term_rate=body["fixed_term_rate"],rate_after_fixed_term=body["rate_after_fixed_term"],extra_repayments=body["extra_repayments"])
    result = mortgage_payments(mortgage)
    print("Before return")
    print(result)
    return {'statusCode': 200,
            'body': json.dumps(result),
            'headers': {'Content-Type': 'application/json'}}


class Mortgage(BaseModel):
    fixed_term_rate_years:int
    loan_term_years:int
    loan_amount:float
    fixed_term_rate:float
    rate_after_fixed_term:float
    extra_repayments:float

def mortgage_payments(mortgage:Mortgage):
    
    loan_term = mortgage.loan_term_years*12
    fixed_rate_months = mortgage.fixed_term_rate_years*12
    original_loan_amount = mortgage.loan_amount
    R = 1 +(mortgage.fixed_term_rate)/(12*100)
    X = original_loan_amount*(R**loan_term)*(1-R)/(1-R**loan_term)
    Monthly_Interest = []
    Monthly_Balance  = []
    amount_at_fixed_term=0
    repayments_at_fixed_term = 0
    loan_amount = original_loan_amount
    for i in range(1,loan_term+1):
        Interest = loan_amount*(R-1)
        
        loan_amount = loan_amount - (X-Interest)
        if(i==fixed_rate_months):
            amount_at_fixed_term=loan_amount

        Monthly_Interest = np.append(Monthly_Interest,Interest)
        Monthly_Balance = np.append(Monthly_Balance, loan_amount)
        if(loan_amount<=0):
            loan_term = i
            break
    
    return {
        "monthly_payment":np.round(X,2),
        "total_interest_payments":np.round(np.sum(Monthly_Interest),2),
        "remaining_mortgage_at_fixed_term":np.round(amount_at_fixed_term,2),
        "loan_term":loan_term,
        "total_extra_repayments":repayments_at_fixed_term
    }


	
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