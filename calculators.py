from http.cookiejar import LWPCookieJar
import json
from queue import Full
from xmlrpc.client import boolean
import numpy as np
from pydantic import parse_obj_as
from mortgage_classes import CalculationBreakdown, AmountCalculatorRequest, AmountCalculatorResponse, BasicCalculatorRequest, BasicCalculatorResponse, CannotBorrowResponse, DelayedMortgageResponse, DoubleMortgageResponse, FullCalculatorRequest, FullCalculatorResponse, HowMuchMortgageRequest, HowMuchMortgageResponse, MaxAmountCalculatorOptions, MaxAmountCalculatorRequest, MaxAmountCalculatorResponse,RemainingEquityRequest,RemainingEquityResponse, SavingsAccountCalculatorRequest
import stamp_duty

def full_calculator(request:FullCalculatorRequest):
    
    house_price_to_sell = request.house_price_to_sell
    mortgage_one_loan_amount = request.mortgage_one.loan_amount
    after_house_sale = house_price_to_sell-mortgage_one_loan_amount
    after_pay_estate_agent = after_house_sale - (house_price_to_sell*(request.estate_agent_commission/100))*1.2
    after_pay_debt = after_pay_estate_agent-request.debts_to_pay_off
    after_pay_solicitor = after_pay_debt-2000
    after_pay_stamp_duty = after_pay_solicitor - stamp_duty.duty_calculator(request.house_price_to_buy)

    calculation_breakdown = CalculationBreakdown(after_house_sale=after_house_sale,after_pay_debt=after_pay_debt,after_pay_estate_agent=after_pay_estate_agent,after_pay_solicitor=after_pay_solicitor,after_pay_stamp_duty=after_pay_stamp_duty)

    # equity = remaining_equity(RemainingEquityRequest(house_price_sale=house_price_to_sell,mortgage_remaining=mortgage_one_loan_amount,debt_to_pay_off=request.debts_to_pay_off,estate_agent_commission=request.estate_agent_commission,pay_stamp_duty=request.use_equity_to_pay_duty))
    # equity.remaining_equity = equity.remaining_equity-request.renovation_money
    total_mortgage_needed = how_much_mortgage_do_i_need(HowMuchMortgageRequest(house_price_to_buy=request.house_price_to_buy,remaining_equity=after_pay_stamp_duty))

    ltv = (total_mortgage_needed.total_mortgage_needed/request.house_price_to_buy)*100
 
    
    if ltv>request.max_ltv or total_mortgage_needed.total_mortgage_needed>request.max_borrowing:
        response = CannotBorrowResponse(ltv=ltv,borrowing_needed=total_mortgage_needed.total_mortgage_needed)
        if ltv>request.max_ltv:
            response.ltv_too_high = True
        if total_mortgage_needed.total_mortgage_needed>request.max_borrowing:
            response.borrowing_too_high = True
        return response
        
    mortgage_two_loan_amount = total_mortgage_needed.total_mortgage_needed-mortgage_one_loan_amount

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
        total_mortgage_payment_after_fixed_term=total_mortgage_monthly_payments_after_fixed_term,
        equity=after_pay_stamp_duty)
    

    # non_ported_equity = remaining_equity(RemainingEquityRequest(house_price_sale=house_price_to_sell,mortgage_remaining=mortgage_one_loan_amount,debt_to_pay_off=request.debts_to_pay_off+request.early_payment_fee,estate_agent_commission=request.estate_agent_commission,pay_stamp_duty=False))
    # savings = savings_calculator(SavingsAccountCalculatorRequest(initial_deposit=non_ported_equity.remaining_equity,interest=3,term=1)) 
    
    # savings = savings-stamp_duty.duty_calculator(house_price_to_sell)

    # non_ported_mortgage_needed = how_much_mortgage_do_i_need(HowMuchMortgageRequest(house_price_to_buy=request.house_price_to_buy,remaining_equity=savings))

    # non_ported_mortgage = mortgage_payments(BasicCalculatorRequest(fixed_term_rate_years=request.non_ported_mortgage.fixed_term_rate_years,fixed_term_rate=request.non_ported_mortgage.fixed_term_rate,loan_term_years=request.non_ported_mortgage.loan_term_years,loan_amount=non_ported_mortgage_needed.total_mortgage_needed,rate_after_fixed_term=request.non_ported_mortgage.rate_after_fixed_term))
    
    # # what mortgage can I get with ported payment
    # rent = request.delay_mortgage_details.rent_amount*request.delay_mortgage_details.length_of_rent
    # loan_amount_if_not_buying_straight = mortgage_amount(AmountCalculatorRequest(loan_term_years=request.mortgage_two.loan_term_years,fixed_term_rate=request.delay_mortgage_details.presumed_rate,monthly_payment=total_mortgage_monthly_payments))
    # delayed_property_amount = round(loan_amount_if_not_buying_straight.loan_amount+equity.remaining_equity-request.early_payment_fee-rent)
    # percentage_change = ((request.house_price_to_buy-delayed_property_amount)/request.house_price_to_buy)*100
    # delayed_property_response = DelayedMortgageResponse(loan_amount=loan_amount_if_not_buying_straight.loan_amount,max_property_value=delayed_property_amount,percentage_drop=percentage_change)
    return FullCalculatorResponse(details_with_ported_mortgage=ported_mortgage,ltv=ltv,calculation_breakdown=calculation_breakdown)

def mortgage_payments(mortgage:BasicCalculatorRequest):
  
    loan_term = mortgage.loan_term_years*12
    fixed_rate_months = mortgage.fixed_term_rate_years*12
    original_loan_amount = mortgage.loan_amount
    R = 1 +(mortgage.fixed_term_rate)/(12*100)
    X = original_loan_amount*(R**loan_term)*(1-R)/(1-R**loan_term)
    Monthly_Interest = []
    Monthly_Balance  = []
    fixed_term_interest_paid = 0
    amount_at_fixed_term=0
    repayments_at_fixed_term = 0
    loan_amount = original_loan_amount
    for i in range(1,loan_term+1):
        Interest = loan_amount*(R-1)
        
        loan_amount = loan_amount - (X-Interest)
        if(i==fixed_rate_months):
            amount_at_fixed_term=loan_amount
            fixed_term_interest_paid = np.round(np.sum(Monthly_Interest),2)

        Monthly_Interest = np.append(Monthly_Interest,Interest)
        Monthly_Balance = np.append(Monthly_Balance, loan_amount)
        if(loan_amount<=0):
            loan_term = i
            break
    
    return BasicCalculatorResponse(
        monthly_payment=np.round(X,2),
        total_interest_payments=np.round(np.sum(Monthly_Interest),2),
        remaining_mortgage_at_fixed_term=np.round(amount_at_fixed_term,2),
        interest_paid_at_fixed_term=fixed_term_interest_paid,
        loan_term=loan_term,
        loan_amount=original_loan_amount,
        total_extra_repayments=repayments_at_fixed_term
    )

def remaining_equity(request:RemainingEquityRequest):
    house_price = request.house_price_sale
    
    mortgage_remaining = request.mortgage_remaining
   
    remaining_equity = house_price-mortgage_remaining
    
    remaining_equity = remaining_equity - request.debt_to_pay_off
    
    estate_agent_fee = (house_price*(request.estate_agent_commission/100))*1.2
   
    remaining_equity = remaining_equity - estate_agent_fee
    
    

    stamp_duty_value = stamp_duty.duty_calculator(house_price)
    
    remaining_equity = remaining_equity- stamp_duty_value
        
    return RemainingEquityResponse(remaining_equity=remaining_equity)

def how_much_mortgage_do_i_need(request:HowMuchMortgageRequest):
    mortgage_amount=request.house_price_to_buy - request.remaining_equity
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

def payments_to_amounts_calculator(mortgage:MaxAmountCalculatorRequest,options:MaxAmountCalculatorOptions=MaxAmountCalculatorOptions()):
  
    loan_term = mortgage.max_loan_term_years*12
    monthly_payment = mortgage.max_monthly_payment
    amounts = MaxAmountCalculatorResponse(amounts=[])
    for i in range(options.starting_term*12,loan_term+1,options.increments*12):
        R = 1 +(mortgage.fixed_term_rate)/(12*100)

        breakdown1 = monthly_payment*(1-R**i)
        breakdown2 = breakdown1/(1-R)
        loan_amount = breakdown2/(R**i)
        
        amount =  AmountCalculatorResponse(
            monthly_payment=mortgage.max_monthly_payment,
            loan_amount=loan_amount,
            loan_term = i/12
        )

        amounts.amounts.append(amount)
    return amounts


def savings_calculator(request:SavingsAccountCalculatorRequest):

    # Calculates compound interest
    Amount = request.initial_deposit * (pow((1 + request.interest / 100), request.term))
    return Amount
    # CI = Amount - request.initial_deposit
    