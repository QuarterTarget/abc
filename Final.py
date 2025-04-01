import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#This imports all necessary libraries and modules for the program to run.
#tkinter for creating gui (we used one taken from github named sv_ttk. It is modern and looks quite nice)
#random is for random numbers, duh. We use it to randomly generate the data for the fake stocks
#all of the matplotlib libraries are for creating the graphs and animating them.
#the idea for funcanimation was taken from a medium article I have forgotten the name of


#here we begin with the stock simulator:

class StockInvestmentSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Investment Simulator")
        self.root.geometry("1100x800")
        
        # Apply the theme
        sv_ttk.set_theme("dark")
        
        # Initialize game state (Thanks Deepseek! I was so confused about this part)
        self.reset_game()
        
        # Initialize UI
        self.create_welcome_page()
    
    def reset_game(self):
        """Reset all game variables to beginner state"""
        self.initial_balance = 50000
        self.user_balance = self.initial_balance
        self.invested_amount = 0
        self.simulation_active = False
        self.simulation_duration = 30  # seconds
        self.current_time = 0
        
        #This next portion is almost all codes for the GUI. I will label each section
        # Stock data with color coding. This part was made with Chatgpt, mostly due to me not being arsed to manually type it out. Are you serious? My fingers will hurt
        self.stocks = [
            {"name": "Tesla", "symbol": "TSLA", "price": 25.50, "volatility": 1.5, "shares": 0, "color": "#1f77b4"},
            {"name": "Apple", "symbol": "AAPL", "price": 18.75, "volatility": 1.0, "shares": 0, "color": "#ff7f0e"},
            {"name": "Amazon", "symbol": "AMZN", "price": 15.20, "volatility": 1.2, "shares": 0, "color": "#2ca02c"},
            {"name": "Google", "symbol": "GOOGL", "price": 14.80, "volatility": 1.1, "shares": 0, "color": "#d62728"},
            {"name": "Microsoft", "symbol": "MSFT", "price": 30.25, "volatility": 0.9, "shares": 0, "color": "#9467bd"},
            {"name": "Netflix", "symbol": "NFLX", "price": 40.60, "volatility": 1.3, "shares": 0, "color": "#8c564b"},
            {"name": "Nvidia", "symbol": "NVDA", "price": 60.75, "volatility": 1.8, "shares": 0, "color": "#e377c2"},
            {"name": "Meta", "symbol": "META", "price": 35.40, "volatility": 1.4, "shares": 0, "color": "#7f7f7f"}
        ]
        
        # Historical data for plotting. This portion was originally coded by Max, didn't work well, we reformatted it via Chatgpt, but the majority is our own here
        self.historical_data = {stock["symbol"]: [] for stock in self.stocks}
        self.portfolio_history = []
        self.time_points = []
    
    def create_welcome_page(self):
        """Create the welcome/intro page"""
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")
        
        title_label = ttk.Label(
            frame, 
            text="📈 Stock Investment Simulator 📉", 
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)
        
        description = ttk.Label(
            frame,
            text="Invest in simulated stocks and track your portfolio performance in real-time",
            font=("Helvetica", 12),
            wraplength=600
        )
        description.pack(pady=10)
 # Display current balance
        self.balance_label = ttk.Label(
            frame,
            text=f"Starting Balance: ${self.initial_balance:,.2f}",
            font=("Helvetica", 14, "bold"),
            foreground="#4CAF50"
        )
        self.balance_label.pack(pady=20)
        
        start_button = ttk.Button(
            frame,
            text="Start Investing",
            command=self.create_investment_page,
            style="Accent.TButton"
        )
        start_button.pack(pady=20)
    
    def create_investment_page(self):
        """Create the investment page with trading controls"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel - Trading controls
        control_frame = ttk.Frame(main_frame, width=350)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right panel - Chart
        chart_frame = ttk.Frame(main_frame)
        chart_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        # Trading controls
        ttk.Label(
            control_frame,
            text="Investment Controls",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Balance display
        self.update_balance_display(control_frame)
        
        # Stock selection
        ttk.Label(control_frame, text="Select Stock:").pack(pady=5)
        self.stock_var = tk.StringVar()
        stock_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.stock_var,
            values=[f"{stock['symbol']} - {stock['name']}" for stock in self.stocks],
            state="readonly"
        )
        stock_combobox.pack(fill="x", pady=5)
        stock_combobox.current(0)
        
        # Shares input
        ttk.Label(control_frame, text="Shares to trade:").pack(pady=5)
        self.shares_var = tk.IntVar(value=10)
        shares_spin = ttk.Spinbox(
            control_frame,
            from_=1,
            to=1000,
            textvariable=self.shares_var,
            width=10
        )
        shares_spin.pack(pady=5)
        
        # Buy/Sell buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(
            button_frame,
            text="Buy",
            command=lambda: self.trade_stock("buy"),
            style="Accent.TButton"
        ).pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Sell",
            command=lambda: self.trade_stock("sell")
        ).pack(side="left", padx=5)
        
        # Portfolio summary
        ttk.Separator(control_frame).pack(fill="x", pady=10)
        ttk.Label(
            control_frame,
            text="Your Portfolio",
            font=("Helvetica", 12, "bold")
        ).pack(pady=5)
        
        self.portfolio_tree = ttk.Treeview(
            control_frame,
            columns=("symbol", "shares", "price", "value"),
            show="headings",
            height=8
        )
        self.portfolio_tree.heading("symbol", text="Symbol")
        self.portfolio_tree.heading("shares", text="Shares")
        self.portfolio_tree.heading("price", text="Price")
        self.portfolio_tree.heading("value", text="Value")
        self.portfolio_tree.column("symbol", width=80)
        self.portfolio_tree.column("shares", width=80, anchor="e")
        self.portfolio_tree.column("price", width=90, anchor="e")
        self.portfolio_tree.column("value", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=self.portfolio_tree.yview)
        self.portfolio_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.portfolio_tree.pack(fill="both", expand=True)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=10)
        
        self.simulate_button = ttk.Button(
            button_frame,
            text="Simulate",
            command=self.start_simulation,
            style="Accent.TButton",
            state="normal" if self.invested_amount > 0 else "disabled"
        )
        self.simulate_button.pack(side="left", padx=5)
        
        ttk.Button(
            button_frame,
            text="Dashboard",
            command=self.create_welcome_page
        ).pack(side="right", padx=5)
        
        # Create the portfolio chart
        self.create_portfolio_chart(chart_frame)
        self.update_portfolio_display()
    
    def update_balance_display(self, parent):
        """Update the balance display"""
        if hasattr(self, 'balance_frame'):
            self.balance_frame.destroy()
            
        self.balance_frame = ttk.Frame(parent)
        self.balance_frame.pack(fill="x", pady=10)
        
        ttk.Label(
            self.balance_frame,
            text=f"Available: ${self.user_balance:,.2f}",
            font=("Helvetica", 12, "bold"),
            foreground="#4CAF50"
        ).pack(side="left")
        
        ttk.Label(
            self.balance_frame,
            text=f"Invested: ${self.invested_amount:,.2f}",
            font=("Helvetica", 12),
            foreground="#FF9800"
        ).pack(side="right")
    
    def create_portfolio_chart(self, parent):
        """Create the portfolio chart"""
        self.fig, self.ax = plt.subplots(figsize=(9, 5), dpi=100)
        self.fig.patch.set_facecolor('#2d2d2d')
        self.ax.set_facecolor('#2d2d2d')
        
        # Style the axes
        for spine in self.ax.spines.values():
            spine.set_color('#444')
        self.ax.tick_params(colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.title.set_color('white')
        
        # Create empty portfolio line
        self.portfolio_line, = self.ax.plot([], [], 'w-', linewidth=2, label="Portfolio Value")
        
        self.ax.set_title("Portfolio Value Over Time", pad=20)
        self.ax.set_xlabel("Time (s)", labelpad=10)
        self.ax.set_ylabel("Value ($)", labelpad=10)
        self.ax.legend()
        self.ax.grid(True, color='#444', linestyle='--', alpha=0.5)
        
        # Embed in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)
    
    def trade_stock(self, action):
        """Handle buying or selling shares"""
        selected = self.stock_var.get().split(" - ")[0]
        shares = self.shares_var.get()
        
        if shares <= 0:
            messagebox.showwarning("Invalid Input", "Please enter a positive number of shares")
            return
        
        # Find the stock
        stock = next((s for s in self.stocks if s["symbol"] == selected), None)
        if not stock:
            return
        
        if action == "buy":
            total_cost = shares * stock["price"]
            if total_cost > self.user_balance:
                messagebox.showwarning("Insufficient Funds", 
                                    f"You don't have enough funds to buy {shares} shares of {selected}")
                return
            
            # Execute buy
            stock["shares"] += shares
            self.user_balance -= total_cost
            self.invested_amount += total_cost
            
            messagebox.showinfo("Trade Executed", 
                             f"Bought {shares} shares of {selected} at ${stock['price']:,.2f}")
        
        elif action == "sell":
            if stock["shares"] < shares:
                messagebox.showwarning("Insufficient Shares", 
                                    f"You don't have enough shares to sell {shares} of {selected}")
                return
            
            # Execute sell
            total_value = shares * stock["price"]
            stock["shares"] -= shares
            self.user_balance += total_value
            self.invested_amount -= total_value
            
            messagebox.showinfo("Trade Executed", 
                             f"Sold {shares} shares of {selected} at ${stock['price']:,.2f}")
        
        # Update UI immediately
        self.update_portfolio_display()
        self.update_balance_display(self.portfolio_tree.master)
        self.simulate_button.config(state="normal" if self.invested_amount > 0 else "disabled")
    
    def update_portfolio_display(self):
        """Update the portfolio treeview"""
        for item in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(item)
        
        for stock in self.stocks:
            if stock["shares"] > 0:
                value = stock["shares"] * stock["price"]
                self.portfolio_tree.insert("", "end", values=(
                    stock["symbol"],
                    stock["shares"],
                    f"${stock['price']:,.2f}",
                    f"${value:,.2f}"