from flask import Flask, render_template, request, flash, redirect
from fileinput import filename
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import recommendation as rd

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/company',  methods = ['GET','POST'])
def company():
    # trading_view chart of company for its share price value if possible
    company_name = 'AdaniEnterp'
    if request.method == "POST":
        _name = request.form['company_name']
        if _name:
            company_name = _name
        
    income_statement, balance_sheet, cash_flow = fetch_data(company_name)
    graphs = []
    income_statement_cols = [' Profit before tax ', ' Net Profit ', ' Sales ']
    balance_sheet_cols = [' Other Assets ', ' Other Liabilities ', ' Reserves ']
    x = ' Report Date '

    for col in income_statement.columns:
        if col[0] != ' ':
            income_statement.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    for col in balance_sheet.columns:
        if col[0] != ' ':
            balance_sheet.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    for col in cash_flow.columns:
        if col[0] != ' ':
            cash_flow.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    columns = [' Net Profit ', ' Dividend Amount ', ' Sales ', ' Profit before tax ', ' Equity Share Capital ', 
    ' Other Liabilities ', ' No. of Equity Shares ', ' Other Assets ', ' Reserves ', ' Investments ', ' Cash & Bank ']

    for i in range(0, len(columns)):
        if i < 4:
            income_statement[columns[i]] = income_statement[columns[i]] * 100000
        else:
            balance_sheet[columns[i]] = balance_sheet[columns[i]] * 100000

    earnings_per_share = income_statement[' Net Profit '] / balance_sheet[' Equity Share Capital ']

    debt_to_equity_ratio = balance_sheet[' Other Liabilities '] / balance_sheet[' No. of Equity Shares ']

    return_on_equity = income_statement[' Net Profit '] / balance_sheet[' No. of Equity Shares ']

    graphs.append(line_graph_income_stmnt(income_statement, balance_sheet))
    # graphs.append(line_graph_balance_sheet(balance_sheet, company_name))

    for y_col in income_statement_cols:
        graphs.append(bar_graphs(income_statement, company_name, x, y_col))

    for y_col in balance_sheet_cols:
        graphs.append(bar_graphs(balance_sheet, company_name, x, y_col))

    ratios = [earnings_per_share, debt_to_equity_ratio, return_on_equity]
    ratio_name = ['earnings_per_share', 'debt_to_equity_ratio', 'return_on_equity']

    graphs.append(line_graph_ratios(income_statement, company, ratios, ratio_name))

    score = rd.recommend(company_name)
    graphs.append(indicator(score))

    return render_template('company.html', graphs=graphs, filename=company_name)


@app.route("/dashboard", methods = ['GET','POST'])
def dashboard():
    if request.method == 'POST':
        if 'file' not in request.files:
            print("No file found")
            return redirect(request.url)
        uploaded_file = request.files['file']
        uploaded_file.save('./data/'+uploaded_file.filename)
        file = uploaded_file.filename
        company_name = file.split('_')[0]
        print(company_name)

    income_statement, balance_sheet, cash_flow = fetch_data(company_name)
    graphs = []
    income_statement_cols = [' Profit before tax ', ' Net Profit ', ' Sales ']
    balance_sheet_cols = [' Other Assets ', ' Other Liabilities ', ' Reserves ']
    x = ' Report Date '

    if income_statement.empty == 0:
        for col in income_statement.columns:
            if col[0] != ' ':
                income_statement.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    if balance_sheet.empty == 0:
        for col in balance_sheet.columns:
            if col[0] != ' ':
                balance_sheet.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    if cash_flow.empty == 0:
        for col in cash_flow.columns:
            if col[0] != ' ':
                cash_flow.rename(columns = {col: ' ' + col + ' '}, inplace = True)

    columns = [' Net Profit ', ' Dividend Amount ', ' Sales ', ' Profit before tax ', ' Equity Share Capital ', 
    ' Other Liabilities ', ' No. of Equity Shares ', ' Other Assets ', ' Reserves ', ' Investments ', ' Cash & Bank ']

    for i in range(0, len(columns)):
        if i < 4:
            if income_statement.empty == 0:
                income_statement[columns[i]] = income_statement[columns[i]] * 100000
        else:
            if balance_sheet.empty == 0:  
                balance_sheet[columns[i]] = balance_sheet[columns[i]] * 100000

    if income_statement.empty == 0 and balance_sheet.empty == 0:
        earnings_per_share = income_statement[' Net Profit '] / balance_sheet[' Equity Share Capital ']

        debt_to_equity_ratio = balance_sheet[' Other Liabilities '] / balance_sheet[' No. of Equity Shares ']

        return_on_equity = income_statement[' Net Profit '] / balance_sheet[' No. of Equity Shares ']

    if income_statement.empty == 0 and balance_sheet.empty == 0:
        graphs.append(line_graph_income_stmnt(income_statement, balance_sheet))
    # graphs.append(line_graph_balance_sheet(balance_sheet, company_name))

    if income_statement.empty == 0:
        for y_col in income_statement_cols:
            graphs.append(bar_graphs(income_statement, company_name, x, y_col))

    if balance_sheet.empty == 0:
        for y_col in balance_sheet_cols:
            graphs.append(bar_graphs(balance_sheet, company_name, x, y_col))

    if income_statement.empty == 0 and balance_sheet.empty == 0:
        ratios = [earnings_per_share, debt_to_equity_ratio, return_on_equity]
        ratio_name = ['earnings_per_share', 'debt_to_equity_ratio', 'return_on_equity']

        graphs.append(line_graph_ratios(income_statement, company, ratios, ratio_name))

    if income_statement.empty == 0:
        graphs.append(funnel(income_statement))

    if income_statement.empty == 0 and balance_sheet.empty == 0 and cash_flow.empty == 0:
        score = rd.recommend(company_name)
        graphs.append(indicator(score))
        
    

    return render_template('company.html', graphs=graphs, filename=uploaded_file.filename)


def fetch_data(company_name):

    income_statement, balance_sheet, cash_flow = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    if os.path.isfile(f'data/{company_name}_Income_Statement.csv'):
        income_statement = pd.read_csv(f'data/{company_name}_Income_Statement.csv')

    if os.path.isfile(f'data/{company_name}_Balance_Sheet.csv'):
        balance_sheet = pd.read_csv(f'data/{company_name}_Balance_Sheet.csv')

    if os.path.isfile(f'data/{company_name}_Cash_Flow.csv'):
        cash_flow = pd.read_csv(f'data/{company_name}_Cash_Flow.csv')

    
    return income_statement, balance_sheet, cash_flow


def line_graph_ratios(income_statement, company, ratio, ratio_name):

    fig = make_subplots(rows=1, cols=3, subplot_titles=("Earning Per Share (EPS)", "Debt To Equity Ratio (D/E)", "Return On Equity (ROE)"))

    fig.add_trace(
        go.Line(x=income_statement[' Report Date '], y=ratio[0]),
        row=1, col=1
    )

    fig.add_trace(
        go.Line(x=income_statement[' Report Date '], y=ratio[1]),
        row=1, col=2
    )

    fig.add_trace(
        go.Line(x=income_statement[' Report Date '], y=ratio[2]),
        row=1, col=3
    )

    return fig.to_html()


def line_graph_income_stmnt(income_statement, balance_sheet):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Total Revenue", "Assets V/S Liabilities"))

    fig.add_trace(
        go.Line(x=income_statement[' Report Date '], y=income_statement[' Profit before tax ']),
        row=1, col=1
    )

    y_col = [' Other Assets ', ' Other Liabilities ']
    fig.add_trace(
        # go.Line(balance_sheet, x=' Report Date ', y=y_col),
        go.Line(x=balance_sheet[' Report Date '], y=balance_sheet[' Other Assets '], name='Total Assets'),
        row=1, col=2
    )

    fig.add_trace(
        # go.Line(balance_sheet, x=' Report Date ', y=y_col),
        go.Line(x=balance_sheet[' Report Date '], y=balance_sheet[' Other Liabilities '], name='Total Liabilities'),
        row=1, col=2
    )

    # fig = px.line(file, x=' Report Date ', y=' Profit before tax ', title='Total Revenue', markers=True)
    return fig.to_html()


# def line_graph_balance_sheet(file, company):
#     y_col = [' Other Assets ', ' Other Liabilities ']
#     fig = px.line(file, x=' Report Date ', y=y_col, title='Assets V/S Liabilities', markers=True)
#     return fig.to_html()



def bar_graphs(file, company, x_col, y_col):
    print(x_col)
    if y_col in [' Profit before tax ', ' Net Profit ', ' Sales ']:
        fig = px.bar(file, x=x_col, y=y_col, title=y_col, color=y_col, hover_data=[' Dividend Amount '])
    else:
        if y_col == ' Other Assets ':
            title = 'Total Assets'
        elif y_col == ' Other Liabilities ':
            title = 'Total Liabilities'
        else:
            title = y_col
        fig = px.bar(file, x=x_col, y=y_col, title=title, color=y_col, hover_data=[' Investments ', ' Cash & Bank '])

    return fig.to_html()



def indicator(value):
    limit = 80

    fig = go.Figure()

    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=value,
        title="Fundamental Health Of Company",
        gauge={'axis': {'range': [None, limit]},
            'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': limit}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ))

    return fig.to_html()


def funnel(income_statement):
    data = dict(
        values = [income_statement[' Sales '].sum(), income_statement[' Profit before tax '].sum(), 
        income_statement[' Net Profit '].sum(), (income_statement[' Profit before tax '].sum() - income_statement[' Net Profit '].sum())],
        title = ['Sales', 'Profit Before Tax', 'Net Profit', 'Tax']
    )
    fig = px.funnel(data, x='values', y='title')
    return fig.to_html()


app.run(debug=True)
