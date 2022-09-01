import typing
from pydantic import BaseModel
from pydantic import parse_obj_as


class BasicCalculatorRequest(BaseModel):
    fixed_term_rate_years:int
    loan_term_years:int
    loan_amount:float
    fixed_term_rate:float
    rate_after_fixed_term:float
    extra_repayments:typing.Optional[float] = 500

class BasicCalculatorResponse(BaseModel):
    monthly_payment:float
    total_interest_payments:float
    remaining_mortgage_at_fixed_term:float
    loan_term:int
    total_extra_repayments:float

class RemainingEquityRequest(BaseModel):
    house_price_sale:float
    mortgage_remaining:float
    debt_to_pay_off:float
    estate_agent_commission:int

class RemainingEquityResponse(BaseModel):
    remaining_equity:float

class HowMuchMortgageRequest(BaseModel):
    house_price_to_buy:float
    remaining_equity:float
    use_remaining_equity_for_duty:bool

class HowMuchMortgageResponse(BaseModel):
    total_mortgage_needed:float

class FullCalculatorRequest(BaseModel):
    house_price_to_sell:float = 700000
    house_price_to_buy:float = 850000
    current_mortgage:float = 355000
    estate_agent_commission:float = 1
    current_mortgage_rate:float = 1.1
    new_mortgage_rate:float = 3.38
    current_mortgage_term:int = 20
    new_mortgage_term:int = 20
    debts_to_pay_off:float = 45000
    use_equity_to_pay_duty:bool = True

class FullCalculatorResponse(BaseModel):
    current_mortgage_payment:float
    new_mortgage_payment:float



    