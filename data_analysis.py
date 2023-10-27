import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px



def fetch_data(company_name):
    income_statement = pd.read_csv(f'{company_name}_income_statement.csv')
    balance_sheet = pd.read_csv(f'{company_name}_balance_sheet.csv')
    cash_flow = pd.read_csv(f'{company_name}_cash_flow.csv')
    
    return income_statement, balance_sheet, cash_flow


def line_graph_income_stmnt(file, company):
    file = file.iloc[::-1]
    plt.plot(file['fiscalDateEnding'], file['totalRevenue'])
    plt.title(f'Total Revenue of {company}')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue')
    plt.savefig(f'{company}_revenue_graph.png')


def line_graph_balance_sheet(file, company):
    file = file.iloc[::-1]
    plt.plot(file['fiscalDateEnding'], file['totalAssets'])
    plt.plot(file['fiscalDateEnding'], file['totalLiabilities'])
    plt.title(f'Assets V/S Liabilities {company}')
    plt.xlabel('Date')
    plt.legend(loc='best')
    plt.savefig(f'{company}_assets_liabilities_graph.png')



def bar_graphs(file, company, x_col, y_col):
    title = ''
    i = 0
    for char in y_col:
        if char.isupper():
            title = title + ' ' + char
        else:
            if i == 0:
                title = title + char.upper()
            else:
                title = title + char
        i += 1

    if y_col in ['totalRevenue', 'netIncome', 'grossProfit']:
        fig = px.bar(file, x=x_col, y=y_col, title=title, color=y_col, hover_data=['ebitda', 'netIncome'])
    else:
        fig = px.bar(file, x=x_col, y=y_col, title=title, color=y_col)



def indicator(value):
    fig = go.Figure(go.Indicator(mode="gauge+number", value=value, title={'text': 'Fundamental Health'}, domain={'x': [0, 1], 'y': [0, 1]}))

