import json
from queue import Full
from xmlrpc.client import boolean
import numpy as np
from pydantic import parse_obj_as
from mortgage_classes import AmountCalculatorRequest, AmountCalculatorResponse, BasicCalculatorRequest, BasicCalculatorResponse, DelayedMortgageResponse, DoubleMortgageResponse, FullCalculatorRequest, FullCalculatorResponse, HowMuchMortgageRequest, HowMuchMortgageResponse,RemainingEquityRequest,RemainingEquityResponse
import stamp_duty

def full_calculator(request:FullCalculatorRequest):
    
    house_price_to_sell = request.house_price_to_sell
    mortgage_one_loan_amount = request.mortgage_one.loan_amount

    equity = remaining_equity(RemainingEquityRequest(house_price_sale=house_price_to_sell,mortgage_remaining=mortgage_one_loan_amount,debt_to_pay_off=request.debts_to_pay_off,estate_agent_commission=request.estate_agent_commission))

    total_mortgage_needed = how_much_mortgage_do_i_need(HowMuchMortgageRequest(house_price_to_buy=request.house_price_to_buy,remaining_equity=equity.remaining_equity,use_remaining_equity_for_duty=request.use_equity_to_pay_duty))

    print("Total mortgage %s"%total_mortgage_needed)
    mortgage_two_loan_amount = total_mortgage_needed.total_mortgage_needed-mortgage_one_loan_amount

    
    ltv = (total_mortgage_needed.total_mortgage_needed/request.house_price_to_buy)*100
   

    mortgage_one = mortgage_payments(request.mortgage_one)

   
    mortgage_one_remaining = mortgage_one.remaining_mortgage_at_fixed_term
    mortgage_one_after_fixed_term = mortgage_payments(BasicCalculatorRequest(loan_term_years=request.mortgage_one.loan_term_years-request.mortgage_one.fixed_term_rate_years,loan_amount=mortgage_one_remaining,fixed_term_rate=request.mortgage_two.rate_after_fixed_term))
    
    mortgage_two_request = request.mortgage_two
    mortgage_two_request.loan_amount=mortgage_two_loan_amount
    mortgage_two = mortgage_payments(mortgage_two_request)
    mortgage_two_remaining_mortgage = mortgage_two.remaining_mortgage_at_fixed_term
    mortgage_two_after_fixed_term=mortgage_payments(BasicCalculatorRequest(loan_term_years=request.mortgage_two.loan_term_years-request.mortgage_two.fixed_term_rate_years,loan_amount=mortgage_two_remaining_mortgage,fixed_term_rate=request.mortgage_two.rate_after_fixed_term))
    
    total_mortgage_monthly_payments = mortgage_one.monthly_payment+mortgage_two.monthly_payment
    
    total_mortgage_monthly_payments_after_fixed_term = mortgage_two_after_fixed_term.monthly_payment+mortgage_one_after_fixed_term.monthly_payment
    total_mortgage_after_fixed_term = mortgage_two.remaining_mortgage_at_fixed_term+mortgage_one.remaining_mortgage_at_fixed_term
    ported_mortgage = DoubleMortgageResponse(
        mortgage_one_details=mortgage_one,
        mortgage_one_after_fixed_term=mortgage_one_after_fixed_term,
        mortgage_two_after_fixed_term=mortgage_two_after_fixed_term,
        mortgage_two_details=mortgage_two,
        total_mortgage=total_mortgage_needed.total_mortgage_needed,
        total_mortgage_payment=total_mortgage_monthly_payments,
        total_mortgage_after_fixed_term=total_mortgage_after_fixed_term,
        total_mortgage_payment_after_fixed_term=total_mortgage_monthly_payments_after_fixed_term)
    
    # what mortgage can I get with ported payment
    rent = request.delay_mortgage_details.rent_amount*request.delay_mortgage_details.length_of_rent
    loan_amount_if_not_buying_straight = mortgage_amount(AmountCalculatorRequest(loan_term_years=request.mortgage_two.loan_term_years,fixed_term_rate=request.delay_mortgage_details.presumed_rate,monthly_payment=total_mortgage_monthly_payments))
    delayed_property_amount = round(loan_amount_if_not_buying_straight.loan_amount+equity.remaining_equity-request.early_payment_fee-rent)
    percentage_change = ((request.house_price_to_buy-delayed_property_amount)/request.house_price_to_buy)*100
    delayed_property_response = DelayedMortgageResponse(loan_amount=loan_amount_if_not_buying_straight.loan_amount,max_property_value=delayed_property_amount,percentage_drop=percentage_change)
    return FullCalculatorResponse(details_with_ported_mortgage=ported_mortgage,details_with_delayed_buy=delayed_property_response,ltv=ltv)

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


def mortgage_amount(mortgage:AmountCalculatorRequest):
  
    loan_term = mortgage.loan_term_years*12
    monthly_payment = mortgage.monthly_payment
    R = 1 +(mortgage.fixed_term_rate)/(12*100)

    breakdown1 = monthly_payment*(1-R**loan_term)
    breakdown2 = breakdown1/(1-R)
    loan_amount = breakdown2/(R**loan_term)

    print("Loan amount %s"%loan_amount)

   
    
    return AmountCalculatorResponse(
        monthly_payment=mortgage.monthly_payment,
        loan_amount=loan_amount
    )
