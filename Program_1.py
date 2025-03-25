from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# Example stock names
stocks = ["Apple", "Tesla", "Amazon", "Google", "Microsoft"]

@app.route('/')
def index():
    return render_template('test.html', stocks=stocks)

@app.route('/invest', methods=['POST'])
def invest():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        
        # Simulate stock price changes (up or down)
        stock_results = {}
        for stock in stocks:
            change_percentage = random.uniform(-0.1, 0.1)  # Random change between -10% and +10%
            new_value = amount * (1 + change_percentage)
            stock_results[stock] = round(new_value, 2)
        
        # Return the simulation results 
        return jsonify(stock_results)

if __name__ == '__main__':
    app.run(debug=True)
