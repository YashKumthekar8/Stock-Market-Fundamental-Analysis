import pandas as pd
import numpy as np
from datetime import datetime

# Counting the values of each year increasing
def counter_increase(val_before, values):
    count = 0
    for value in values:
        if value > val_before:
            count += 1
        val_before = value

    return count

# Counting the values of each year decreasing
def counter_decrease(val_before, values):
    count = 0
    for value in values:
        if value < val_before:
            count += 1
        val_before = value

    return count

# Counting the values increase, decrease of the ratios
def financial_ratios(ticker):
    files = [f'data/{ticker}_Income_Statement.csv', f'data/{ticker}_Balance_Sheet.csv']
    financial_statement = pd.read_csv(files[0])
    balance_sheet = pd.read_csv(files[1])

    for col in financial_statement.columns:
        if col[0] != ' ':
            financial_statement.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    for col in balance_sheet.columns:
        if col[0] != ' ':
            balance_sheet.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    counts = []

    earnings_per_share = financial_statement[' Net Profit '] / balance_sheet[' Equity Share Capital ']
    counts.append(counter_increase(earnings_per_share[0], earnings_per_share))

    debt_to_equity_ratio = balance_sheet[' Other Liabilities '] / balance_sheet[' No. of Equity Shares ']
    counts.append(counter_decrease(debt_to_equity_ratio[0], debt_to_equity_ratio))

    return_on_equity = financial_statement[' Net Profit '] / balance_sheet[' No. of Equity Shares ']
    counts.append(counter_increase(return_on_equity[0], return_on_equity))

    return counts

# Analyzing the income statement file with various columns
def income_statement_analysis(ticker):
    files = f'data/{ticker}_Income_Statement.csv'
    financial_statement = pd.read_csv(files)

    for col in financial_statement.columns:
        if col[0] != ' ':
            financial_statement.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    indices = [' Sales ', ' Profit before tax ']
    counts = []
    for i in range(0, 2):
        count = 0
        val_before = financial_statement[indices[i]][0]
        for value in financial_statement[indices[i]]:
            if value > val_before:
                count += 1
            val_before = value
        counts.append(count)

    return counts
    # if all the counters has more than 7 counts its good    

# Analyzing the cash flow file with various columns
def cash_flow_analysis(ticker):
    files = f'data/{ticker}_Cash_Flow.csv'
    cash_flow_statement = pd.read_csv(files)

    for col in cash_flow_statement.columns:
        if col[0] != ' ':
            cash_flow_statement.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    indices = [' Cash from Operating Activity ', ' Dividend Amount ', ' Cash from Financing Activity ']
    cash_flow_statement[' Dividend Amount '].fillna(0, inplace=True)
    counts = []
    for i in range(0, 3):
        if(i != 2):
            count = 0
            val_before = cash_flow_statement[indices[i]][0]
            for value in cash_flow_statement[indices[i]]:
                if value > val_before:
                    count += 1
                val_before = value

            counts.append(count)

        else:
            count = 0
            val_before = cash_flow_statement[indices[i]][0]
            for value in cash_flow_statement[indices[i]]:
                if value < val_before:
                    count += 1
                val_before = value

            counts.append(count)

    counts[1], counts[2] = counts[2], counts[1]
    return counts

# Providing the pointer scheme for increase, decrease counter and score for it
def pointer_scheme(values):
    pointers = {'earning_per_share': [1, 5, 10],
                'debt_to_equity': [1, 5, 10],
                'return_on_equity': [1, 5, 10],
                'total_revenue': [1, 5, 10],
                'ebitda': [1, 5, 10],
                'operating_cash_flow': [1, 5, 10],
                'cashflow_from_financing': [1, 5, 10],
                'dividend_payout': [5, 10]
                }

    total_points = 0
    i = 0
    for val in pointers:
        if val == 'dividend_payout':
            if values[i] >= 7:
                total_points += pointers[val][1]
            elif values[i] > 4 and values[i] < 7:
                total_points += pointers[val][0]
        else:
            if values[i] >= 7:
                total_points += pointers[val][2]
            elif values[i] > 4 and values[i] < 7:
                total_points += pointers[val][1]
            elif values[i] > 2 and values[i] <= 4:
                total_points += pointers[val][0]

        i += 1

    return total_points
            
# adding the final recommend function which invokes all the sub functions for calculations
def recommend(ticker):

    counts = financial_ratios(ticker)

    counts_inc_stmnt = income_statement_analysis(ticker)
    for count in counts_inc_stmnt:
        counts.append(count)


    counts_cf = cash_flow_analysis(ticker)
    for count in counts_cf:
        counts.append(count)

    points = pointer_scheme(counts)
    return points


# print('Reliance : ', recommend('RELIANCE'))
# print('ICICI : ', recommend('ICICI'))
# print('HDFC : ', recommend('HDFC'))
# print('SBI : ', recommend('SBI'))
# print('TCS : ', recommend('TCS'))
# print('Infosys : ', recommend('INFY'))
# print('Mahindra & Mahindra : ', recommend('M&M'))
# print('Tech Mahindra : ', recommend('TECHM'))
# print('Tata Motors : ', recommend('TATAMOTORS'))
