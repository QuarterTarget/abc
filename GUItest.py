import tkinter as tk
from tkinter import ttk
import sv_ttk
import random
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sample stocks (name, price)
stocks = [
    {"name": "Tesla", "price": 500},
    {"name": "Apple", "price": 500},
    {"name": "Amazon", "price": 500},
    {"name": "Google", "price": 500},
    {"name": "Microsoft", "price": 500},
]

# Initialize user balance
user_balance = 10000
invested_amount = 0
invested_stocks = []

# Function to update the user balance
def update_balance(amount):
    global user_balance
    user_balance += amount
    balance_label.config(text=f"Balance: ${user_balance}")

# Function to simulate investing
def invest():
    global invested_amount, invested_stocks, user_balance  # Add global declaration
    if invested_amount <= user_balance:
        # Transition to loading screen
        transition_to_loading()
        
        # Simulate the investment in a separate thread
        threading.Thread(target=process_investment).start()
    else:
        result_label.config(text="Insufficient balance!")

# Function to simulate the investment process
def process_investment():
    global invested_amount, invested_stocks, user_balance

    # Deduct invested amount from balance
    user_balance -= invested_amount
    update_balance(0)

    # Simulate random stock price fluctuations after investing
    for stock in invested_stocks:
        stock["price"] = random.randint(stock["price"] - 20, stock["price"] + 20)  # Simulating price change

    time.sleep(2)  # Simulate loading time

    # Show results
    show_results()

# Transition to loading screen
def transition_to_loading():
    global invested_amount, invested_stocks
    # Hide main screen content
    frame.pack_forget()

    # Create and pack loading screen elements
    loading_frame = ttk.Frame(root, padding=20)
    loading_frame.pack(expand=True, fill="both")

    loading_label = ttk.Label(loading_frame, text="Loading", font=("Helvetica", 32, "bold"), foreground="white")
    loading_label.pack(pady=20)

    loading_dots_label = ttk.Label(loading_frame, text=".", font=("Helvetica", 32, "bold"), foreground="white")
    loading_dots_label.pack(pady=20)

    # Animate the dots in loading screen
    def animate_loading():
        dots = ""
        while True:
            for i in range(4):
                time.sleep(0.5)
                loading_dots_label.config(text=dots + "." * i)
                root.update()

    threading.Thread(target=animate_loading, daemon=True).start()

# Show the results screen after investing
def show_results():
    # Hide the loading screen
    for widget in root.winfo_children():
        widget.destroy()

    # Show results screen
    results_frame = ttk.Frame(root, padding=20)
    results_frame.pack(expand=True, fill="both")

    title_label = ttk.Label(results_frame, text="Investment Results", font=("Helvetica", 32, "bold"), foreground="white")
    title_label.pack(pady=20)

    result_label = ttk.Label(results_frame, text=f"Invested Amount: ${invested_amount}", font=("Helvetica", 16), foreground="yellow")
    result_label.pack(pady=10)

    # Show each stock's results (profits/losses)
    for stock in invested_stocks:
        price_change = stock["price"] - stock["initial_price"]
        if price_change > 0:
            result_text = f"{stock['name']}: Profit of ${price_change}"
        else:
            result_text = f"{stock['name']}: Loss of ${-price_change}"

        stock_label = ttk.Label(results_frame, text=result_text, font=("Helvetica", 14), foreground="lightblue")
        stock_label.pack(pady=5)

    # Show final balance
    final_balance_label = ttk.Label(results_frame, text=f"Final Balance: ${user_balance}", font=("Helvetica", 16), foreground="green")
    final_balance_label.pack(pady=10)

    # Show stock history (what was invested)
    history_label = ttk.Label(results_frame, text="Investment History:", font=("Helvetica", 16), foreground="white")
    history_label.pack(pady=10)

    for stock in invested_stocks:
        history_label = ttk.Label(results_frame, text=f"- {stock['name']}: ${stock['initial_price']}", font=("Helvetica", 14), foreground="white")
        history_label.pack(pady=5)

    # Start plotting the stock price movements in real-time
    plot_stock_movements(results_frame)

# Function to plot the stock movements dynamically
def plot_stock_movements(results_frame):
    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Initialize the plot data (empty lists for each stock)
    prices = {stock["name"]: [stock["price"]] for stock in invested_stocks}
    time_points = [0]  # Start with time point 0
    
    # Function to update stock prices and plot them
    def update_plot():
        nonlocal time_points
        time_points.append(time_points[-1] + 1)  # Increment time
        
        # Simulate stock price fluctuations for each stock
        for stock in invested_stocks:
            new_price = stock["price"] + random.randint(-10, 10)  # Random fluctuation
            stock["price"] = new_price
            prices[stock["name"]].append(new_price)
        
        # Clear and update the plot
        ax.clear()
        
        # Plot data for each stock
        for stock_name in prices:
            ax.plot(time_points, prices[stock_name], label=stock_name)

        ax.set_title('Stock Price Movements (Real-Time)', fontsize=16)
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Price ($)', fontsize=12)
        ax.legend()
        
        # Redraw the canvas with the updated plot
        canvas.draw()

        # Schedule the next update (10ms delay for real-time simulation)
        if time_points[-1] < 60:  # Limit the number of time points (you can increase this limit)
            root.after(1000, update_plot)  # Update every second (1000ms)
        else:
            canvas.get_tk_widget().pack_forget()  # Remove the graph after 60 updates

    # Embed the initial plot
    canvas = FigureCanvasTkAgg(fig, master=results_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Start updating the plot
    update_plot()

# Function to add stocks to investment
def add_stock(stock_index):
    global invested_amount, invested_stocks  # Add global declaration
    stock = stocks[stock_index]
    stock_amount = stock["price"]
    
    # Only add stock if the user can afford it
    if invested_amount + stock_amount <= user_balance:
        invested_amount += stock_amount
        invested_stocks.append({"name": stock["name"], "price": stock["price"], "initial_price": stock["price"]})
        invested_amount_label.config(text=f"Invested Amount: ${invested_amount}")
    else:
        result_label.config(text="Cannot afford this stock!")

# Function to remove stock from investment
def remove_stock(stock_index):
    global invested_amount, invested_stocks  # Add global declaration
    stock = invested_stocks[stock_index]
    stock_amount = stock["price"]
    
    # Remove stock if it's in the portfolio
    if invested_amount >= stock_amount:
        invested_amount -= stock_amount
        invested_stocks.pop(stock_index)
        invested_amount_label.config(text=f"Invested Amount: ${invested_amount}")
    else:
        result_label.config(text="Error removing stock.")

# Set up the main window
root = tk.Tk()
root.title("Stock Simulator")
root.geometry("900x700")

# Apply the sv_ttk theme
sv_ttk.set_theme("dark")

# Create and place widgets
frame = ttk.Frame(root, padding=20)
frame.pack(expand=True, fill="both")

# Title label
title_label = ttk.Label(frame, text="📈 Stock Investment Simulator 📉", font=("Helvetica", 32, "bold"), foreground="white")
title_label.pack(pady=20)

# Display stocks and buttons to invest
stock_buttons_frame = ttk.Frame(frame)
stock_buttons_frame.pack(pady=20)

for i, stock in enumerate(stocks):
    stock_frame = ttk.Frame(stock_buttons_frame, padding=10)
    stock_frame.grid(row=i, column=0, padx=10, pady=10, sticky="w")

    stock_label = ttk.Label(stock_frame, text=f"{stock['name']} - ${stock['price']}", font=("Helvetica", 14), foreground="lightblue")
    stock_label.pack(side="left", padx=10)

    add_button = ttk.Button(stock_frame, text="➕", command=lambda i=i: add_stock(i), width=5)
    add_button.pack(side="left", padx=10)

    minus_button = ttk.Button(stock_frame, text="➖", command=lambda i=i: remove_stock(i), width=5)
    minus_button.pack(side="left", padx=10)

# Display user's balance
balance_label = ttk.Label(frame, text=f"Balance: ${user_balance}", font=("Helvetica", 16), foreground="green")
balance_label.pack(pady=10)

# Display invested amount
invested_amount_label = ttk.Label(frame, text=f"Invested Amount: ${invested_amount}", font=("Helvetica", 16), foreground="yellow")
invested_amount_label.pack(pady=10)

# Button to invest
invest_button = ttk.Button(frame, text="Invest", command=invest, style="TButton")
invest_button.pack(pady=20)

# Result message
result_label = ttk.Label(frame, text="", font=("Helvetica", 16), foreground="white")
result_label.pack(pady=10)

# Profits and Losses Display
profits_losses_label = ttk.Label(frame, text="", font=("Helvetica", 14), foreground="lightgray")
profits_losses_label.pack(pady=10)

# Run the application
root.mainloop()
