from array import ArrayType
from typing import Optional, List
from xmlrpc.client import boolean
from pydantic import BaseModel
from pydantic import parse_obj_as


class BasicCalculatorRequest(BaseModel):
    fixed_term_rate_years:int=2
    loan_term_years:int=20
    loan_amount:float=350000
    fixed_term_rate:float=1.1
    rate_after_fixed_term:float=5
    extra_repayments:Optional[float] = 500

class AmountCalculatorRequest(BaseModel):
    loan_term_years:int
    monthly_payment:float
    fixed_term_rate:float

class AmountCalculatorResponse(BaseModel):
    monthly_payment:float
    loan_amount:float
    loan_term:Optional[float]

class MaxAmountCalculatorRequest(BaseModel):
    max_loan_term_years:int = 20
    max_monthly_payment:float = 3000
    fixed_term_rate:float = 3.38

class MaxAmountCalculatorResponse(BaseModel):
    amounts: List[AmountCalculatorResponse]

class MaxAmountCalculatorOptions(BaseModel):
    starting_term:Optional[int] = 5
    increments:Optional[int] = 5

class BasicCalculatorResponse(BaseModel):
    monthly_payment:float
    total_interest_payments:float
    interest_paid_at_fixed_term:float
    remaining_mortgage_at_fixed_term:float
    loan_term:int
    loan_amount:float
    total_extra_repayments:float

class RemainingEquityRequest(BaseModel):
    house_price_sale:float
    mortgage_remaining:float
    debt_to_pay_off:float
    pay_stamp_duty: bool
    estate_agent_commission:int

class RemainingEquityResponse(BaseModel):
    remaining_equity:float

class HowMuchMortgageRequest(BaseModel):
    house_price_to_buy:float
    remaining_equity:float

class HowMuchMortgageResponse(BaseModel):
    total_mortgage_needed:float

class DelayMortgageRequest(BaseModel):
    length_of_rent:int=12
    rent_amount:int=3250
    presumed_rate:float=4

class FullCalculatorRequest(BaseModel):
    house_price_to_sell:float = 675000
    house_price_to_buy:float = 1000000
    estate_agent_commission:float = 1
    mortgage_one:BasicCalculatorRequest=BasicCalculatorRequest(fixed_term_rate=1.1)
    mortgage_two:BasicCalculatorRequest=BasicCalculatorRequest(fixed_term_rate=3.38)
    non_ported_mortgage:BasicCalculatorRequest=BasicCalculatorRequest(fixed_term_rate=2)
    delay_mortgage_details:DelayMortgageRequest=DelayMortgageRequest()
    debts_to_pay_off:float = 45000
    early_payment_fee:float = 7000
    use_equity_to_pay_duty:bool = True
    max_ltv:int = 70
    max_borrowing:int=723000
    renovation_money:int=100000



class DoubleMortgageResponse(BaseModel):
    mortgage_one_details: BasicCalculatorResponse
    mortgage_two_details: BasicCalculatorResponse
    total_mortgage_payment:float
    total_mortgage:float
    equity:float
    mortgage_one_after_fixed_term:BasicCalculatorResponse
    mortgage_two_after_fixed_term:BasicCalculatorResponse
    total_mortgage_payment_after_fixed_term:float
    total_mortgage_after_fixed_term:float

class DelayedMortgageResponse(BaseModel):
    loan_amount:float
    max_property_value:float
    percentage_drop:float


class CannotBorrowResponse(BaseModel):
    ltv_too_high:bool=False
    borrowing_too_high:bool=False
    ltv:Optional[int]
    borrowing_needed:Optional[int]

class CalculationBreakdown(BaseModel):
    after_house_sale:float
    after_pay_estate_agent:float
    after_pay_debt:float
    after_pay_solicitor:float
    after_pay_stamp_duty:float
    

class FullCalculatorResponse(BaseModel):
    details_with_ported_mortgage:Optional[DoubleMortgageResponse]
    details_with_delayed_buy:Optional[DelayedMortgageResponse]
    calculation_breakdown:CalculationBreakdown
    ltv:float

class SavingsAccountCalculatorRequest(BaseModel):
    initial_deposit:float=250000
    interest:float=3
    term:int=12



   


    