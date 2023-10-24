from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/company')
def company():
    return render_template('company.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')



app.run(debug=True)
