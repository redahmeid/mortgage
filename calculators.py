import json
from queue import Full
from xmlrpc.client import boolean
import numpy as np
from pydantic import parse_obj_as
from mortgage_classes import BasicCalculatorRequest, BasicCalculatorResponse, FullCalculatorRequest, FullCalculatorResponse, HowMuchMortgageRequest, HowMuchMortgageResponse,RemainingEquityRequest,RemainingEquityResponse
import stamp_duty

def full_calculator(request:FullCalculatorRequest):
    
    house_price_to_sell = request.house_price_to_sell
    current_mortgage = request.current_mortgage

    equity = remaining_equity(RemainingEquityRequest(house_price_sale=house_price_to_sell,mortgage_remaining=current_mortgage,debt_to_pay_off=request.debts_to_pay_off,estate_agent_commission=request.estate_agent_commission))

    total_mortgage_needed = how_much_mortgage_do_i_need(HowMuchMortgageRequest(house_price_to_buy=request.house_price_to_buy,remaining_equity=equity,use_remaining_equity_for_duty=request.use_equity_to_pay_duty))

    extra_mortgage_needed = total_mortgage_needed.total_mortgage_needed-current_mortgage

    current_payments = mortgage_payments(BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=request.current_mortgage_term,loan_amount=request.current_mortgage,fixed_term_rate=request.current_mortgage_rate, rate_after_fixed_term=5,extra_repayments=0))
    extra_payments = mortgage_payments(BasicCalculatorRequest(fixed_term_rate_years=2,loan_term_years=request.new_mortgage_term,loan_amount=extra_mortgage_needed,fixed_term_rate=request.new_mortgage_rate, rate_after_fixed_term=5,extra_repayments=0))

    return FullCalculatorResponse(current_mortgage_payment=current_payments,new_mortgage_payment=extra_payments)

def mortgage_payments(mortgage:BasicCalculatorRequest):
  
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
    
    return BasicCalculatorResponse(
        monthly_payment=np.round(X,2),
        total_interest_payments=np.round(np.sum(Monthly_Interest),2),
        remaining_mortgage_at_fixed_term=np.round(amount_at_fixed_term,2),
        loan_term=loan_term,
        total_extra_repayments=repayments_at_fixed_term
    )

def remaining_equity(request:RemainingEquityRequest):
    house_price = request.house_price_sale
    mortgage_remaining = request.mortgage_remaining

    remaining_equity = house_price-mortgage_remaining

    remaining_equity = remaining_equity - request.debt_to_pay_off

    estate_agent_fee = (house_price*(request.estate_agent_commission/100))*1.2

    remaining_equity = remaining_equity - estate_agent_fee

    return RemainingEquityResponse(remaining_equity=remaining_equity)

def how_much_mortgage_do_i_need(request:HowMuchMortgageRequest):
    mortgage_amount=request.house_price_to_buy - request.remaining_equity
    if(request.use_remaining_equity_for_duty):
        stamp_duty_value = stamp_duty.duty_calculator(request.house_price_to_buy)
        mortgage_amount = mortgage_amount - stamp_duty_value
    return HowMuchMortgageResponse(total_mortgage_needed=mortgage_amount)