import tkinter as tk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt

class StockSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Simulator")
        
        self.budget = 1000  # Starting budget
        self.stocks = {f"Stock {i+1}": round(random.uniform(10, 100), 2) for i in range(10)}
        self.investments = {stock: 0 for stock in self.stocks}
        
        self.create_widgets()
        
    def create_widgets(self):
        tk.Label(self.root, text=f"Starting Budget: ${self.budget}", font=("Arial", 12)).pack()
        
        self.entries = {}
        for stock, price in self.stocks.items():
            frame = tk.Frame(self.root)
            frame.pack()
            tk.Label(frame, text=f"{stock} - Initial Price: ${price:.2f}").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=10)
            entry.pack(side=tk.LEFT)
            self.entries[stock] = entry
        
        self.start_button = tk.Button(self.root, text="Invest and Simulate", command=self.start_simulation)
        self.start_button.pack()
    
    def start_simulation(self):
        total_invested = 0
        for stock, entry in self.entries.items():
            try:
                amount = float(entry.get()) if entry.get() else 0
                if amount < 0:
                    raise ValueError
                total_invested += amount
                self.investments[stock] = amount
            except ValueError:
                messagebox.showerror("Input Error", f"Invalid investment in {stock}")
                return
        
        if total_invested > self.budget:
            messagebox.showerror("Input Error", "You cannot invest more than your budget!")
            return
        
        self.simulate_stock_changes()
        
    def simulate_stock_changes(self):
        self.stock_prices = {stock: [price] for stock, price in self.stocks.items()}
        for _ in range(20):  # Simulating 20 time steps
            for stock in self.stock_prices:
                change = round(random.uniform(-5, 5), 2)
                new_price = max(1, self.stock_prices[stock][-1] + change)
                self.stock_prices[stock].append(round(new_price, 2))
        
        self.plot_stock_prices()
    
    def plot_stock_prices(self):
        fig, ax = plt.subplots()
        
        for stock, prices in self.stock_prices.items():
            ax.plot(prices, label=stock)
        
        ax.set_title("Stock Price Simulation")
        ax.set_xlabel("Time Steps")
        ax.set_ylabel("Stock Price")
        ax.legend()
        plt.show()
        
        self.calculate_earnings()
    
    def calculate_earnings(self):
        total_value = 0
        for stock, amount in self.investments.items():
            if amount > 0:
                initial_price = self.stock_prices[stock][0]
                final_price = self.stock_prices[stock][-1]
                shares = amount / initial_price
                total_value += shares * final_price
        
        earnings = total_value - sum(self.investments.values())
        messagebox.showinfo("Simulation Complete", f"Final Portfolio Value: ${total_value:.2f}\nEarnings: ${earnings:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockSimulator(root)
    root.mainloop()
