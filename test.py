import tkinter as tk
from tkinter import ttk, messagebox
import sv_ttk
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class StockInvestmentSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Investment Simulator")
        self.root.geometry("1000x800")
        
        # Apply modern theme
        sv_ttk.set_theme("dark")
        
        # Initialize variables with affordable values
        self.user_balance = 50000  # Increased starting balance
        self.invested_amount = 0
        self.invested_stocks = []
        self.simulation_active = False
        self.simulation_duration = 30  # seconds
        self.current_time = 0
        
        # Affordable stock data with volatility factors
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
        
        # Historical data for plotting
        self.historical_data = {stock["symbol"]: [] for stock in self.stocks}
        self.portfolio_history = []
        self.time_points = []
        
        # Initialize UI
        self.create_welcome_page()
    
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
            text=f"Current Balance: ${self.user_balance:,.2f}",
            font=("Helvetica", 14, "bold"),
            foreground="#4CAF50"
        )
        self.balance_label.pack(pady=20)
        
        start_button = ttk.Button(
            frame,
            text="Start Investing",
            command=self.create_investment_page
        )
        start_button.pack(pady=20)
    
    def create_investment_page(self):
        """Create the stock selection and investment page"""
        self.clear_window()
        
        main_frame = ttk.Frame(self.root)
        main_frame.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Left panel for investment controls
        control_frame = ttk.Frame(main_frame, width=300)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right panel for the combined chart
        chart_frame = ttk.Frame(main_frame)
        chart_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        # Investment controls
        ttk.Label(
            control_frame,
            text="Investment Portfolio",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Balance display
        self.portfolio_balance_label = ttk.Label(
            control_frame,
            text=f"Available: ${self.user_balance:,.2f}",
            font=("Helvetica", 12)
        )
        self.portfolio_balance_label.pack(pady=5)
        
        # Stock selection combobox
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
        ttk.Label(control_frame, text="Shares to buy:").pack(pady=5)
        self.shares_var = tk.IntVar(value=10)
        shares_spin = ttk.Spinbox(
            control_frame,
            from_=1,
            to=1000,
            textvariable=self.shares_var,
            width=10
        )
        shares_spin.pack(pady=5)
        
        # Buy button
        buy_button = ttk.Button(
            control_frame,
            text="Buy Shares",
            command=self.buy_stock,
            style="Accent.TButton"
        )
        buy_button.pack(pady=20)
        
        # Portfolio summary
        ttk.Separator(control_frame).pack(fill="x", pady=10)
        ttk.Label(
            control_frame,
            text="Your Portfolio",
            font=("Helvetica", 12, "bold")
        ).pack(pady=5)
        
        self.portfolio_tree = ttk.Treeview(
            control_frame,
            columns=("symbol", "shares", "value"),
            show="headings",
            height=8
        )
        self.portfolio_tree.heading("symbol", text="Symbol")
        self.portfolio_tree.heading("shares", text="Shares")
        self.portfolio_tree.heading("value", text="Value")
        self.portfolio_tree.column("symbol", width=80)
        self.portfolio_tree.column("shares", width=80, anchor="e")
        self.portfolio_tree.column("value", width=100, anchor="e")
        self.portfolio_tree.pack(fill="both", expand=True, pady=5)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill="x", pady=10)
        
        simulate_button = ttk.Button(
            button_frame,
            text="Simulate",
            command=self.start_simulation,
            state="normal" if self.invested_amount > 0 else "disabled"
        )
        simulate_button.pack(side="left", padx=5)
        
        back_button = ttk.Button(
            button_frame,
            text="Dashboard",
            command=self.create_welcome_page
        )
        back_button.pack(side="right", padx=5)
        
        # Create the combined chart
        self.create_combined_chart(chart_frame)
        self.update_portfolio_display()
    
    def create_combined_chart(self, parent):
        """Create the combined stock and portfolio chart"""
        self.fig, self.ax = plt.subplots(figsize=(8, 5), dpi=100)
        self.fig.patch.set_facecolor('#2d2d2d')
        self.ax.set_facecolor('#2d2d2d')
        
        # Style the axes
        for spine in self.ax.spines.values():
            spine.set_color('#444')
        self.ax.tick_params(colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.title.set_color('white')
        
        # Create empty plots
        self.stock_lines = {}
        for stock in self.stocks:
            line, = self.ax.plot([], [], '-', 
                               color=stock["color"],
                               linewidth=1.5,
                               label=stock["symbol"])
            self.stock_lines[stock["symbol"]] = line
        
        # Portfolio line (thicker)
        self.portfolio_line, = self.ax.plot([], [], 'w-', linewidth=2.5, label="PORTFOLIO")
        
        self.ax.set_title("Stock Prices & Portfolio Value")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Value ($)")
        self.ax.legend()
        self.ax.grid(True, color='#444', linestyle='--', alpha=0.5)
        
        # Embed in Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=parent)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both", padx=10, pady=10)
    
    def buy_stock(self):
        """Handle buying shares with immediate updates"""
        selected = self.stock_var.get().split(" - ")[0]
        shares = self.shares_var.get()
        
        if shares <= 0:
            messagebox.showwarning("Invalid Input", "Please enter a positive number of shares")
            return
        
        # Find the stock
        stock = next((s for s in self.stocks if s["symbol"] == selected), None)
        if not stock:
            return
        
        total_cost = shares * stock["price"]
        if total_cost > self.user_balance:
            messagebox.showwarning("Insufficient Funds", 
                                f"You don't have enough funds to buy {shares} shares of {selected}")
            return
        
        # Execute the trade
        stock["shares"] += shares
        self.user_balance -= total_cost
        self.invested_amount += total_cost
        
        # Update the UI immediately
        self.update_portfolio_display()
        messagebox.showinfo("Trade Executed", 
                          f"Bought {shares} shares of {selected} at ${stock['price']:,.2f}")
    
    def update_portfolio_display(self):
        """Update all portfolio displays"""
        # Update balance
        self.balance_label.config(text=f"Current Balance: ${self.user_balance:,.2f}")
        self.portfolio_balance_label.config(text=f"Available: ${self.user_balance:,.2f}")
        
        # Update portfolio tree
        for item in self.portfolio_tree.get_children():
            self.portfolio_tree.delete(item)
        
        for stock in self.stocks:
            if stock["shares"] > 0:
                value = stock["shares"] * stock["price"]
                self.portfolio_tree.insert("", "end", values=(
                    stock["symbol"],
                    stock["shares"],
                    f"${value:,.2f}"
                ))
    
    def start_simulation(self):
        """Start the simulation with combined chart"""
        self.simulation_active = True
        self.current_time = 0
        self.time_points = []
        self.portfolio_history = []
        
        # Initialize historical data
        for stock in self.stocks:
            self.historical_data[stock["symbol"]] = [stock["price"]]
        
        # Create simulation page
        self.create_simulation_page()
        
        # Start animation
        self.ani = FuncAnimation(
            self.fig,
            self.update_simulation,
            frames=self.simulation_duration,
            interval=1000,
            blit=False
        )
        self.canvas.draw()
    
    def create_simulation_page(self):
        """Create the simulation page"""
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")
        
        # Header with simulation info
        header_frame = ttk.Frame(frame)
        header_frame.pack(fill="x", pady=10)
        
        ttk.Label(
            header_frame,
            text="Live Simulation",
            font=("Helvetica", 18, "bold")
        ).pack(side="left")
        
        self.sim_time_label = ttk.Label(
            header_frame,
            text="Time: 0s",
            font=("Helvetica", 12)
        )
        self.sim_time_label.pack(side="right", padx=20)
        
        # Portfolio value display
        self.portfolio_value_label = ttk.Label(
            frame,
            text="Portfolio Value: $0.00",
            font=("Helvetica", 14, "bold"),
            foreground="#4CAF50"
        )
        self.portfolio_value_label.pack(pady=10)
        
        # Recreate the combined chart
        self.create_combined_chart(frame)
        
        # Control buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=10)
        
        self.stop_button = ttk.Button(
            button_frame,
            text="Stop Simulation",
            command=self.stop_simulation
        )
        self.stop_button.pack(side="left", padx=10)
    
    def update_simulation(self, frame):
        """Update function for the animation"""
        if not self.simulation_active:
            return
        
        self.current_time += 1
        self.time_points.append(self.current_time)
        
        # Update stock prices
        portfolio_value = 0
        for stock in self.stocks:
            if stock["shares"] > 0:
                # Random price change based on volatility
                change = random.uniform(-2, 2) * stock["volatility"]
                stock["price"] = max(0.01, stock["price"] + change)
                self.historical_data[stock["symbol"]].append(stock["price"])
                
                # Add to portfolio value
                portfolio_value += stock["shares"] * stock["price"]
        
        self.portfolio_history.append(portfolio_value)
        
        # Update UI
        self.sim_time_label.config(text=f"Time: {self.current_time}s")
        self.portfolio_value_label.config(text=f"Portfolio Value: ${portfolio_value:,.2f}")
        
        # Update all lines
        for symbol, line in self.stock_lines.items():
            if len(self.time_points) == len(self.historical_data[symbol]):
                line.set_data(self.time_points, self.historical_data[symbol])
        
        # Update portfolio line
        if len(self.time_points) == len(self.portfolio_history):
            self.portfolio_line.set_data(self.time_points, self.portfolio_history)
        
        # Adjust view
        self.ax.relim()
        self.ax.autoscale_view()
        
        # Stop if duration reached
        if self.current_time >= self.simulation_duration:
            self.stop_simulation()
        
        return list(self.stock_lines.values()) + [self.portfolio_line]
    
    def stop_simulation(self):
        """Stop the simulation"""
        self.simulation_active = False
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
        self.create_results_page()
    
    def create_results_page(self):
        """Create results page after simulation"""
        self.clear_window()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")
        
        # Calculate final values
        final_value = sum(stock["shares"] * stock["price"] for stock in self.stocks)
        profit_loss = final_value - self.invested_amount
        pl_percent = (profit_loss / self.invested_amount) * 100 if self.invested_amount else 0
        
        # Results header
        ttk.Label(
            frame,
            text="Simulation Results",
            font=("Helvetica", 20, "bold")
        ).pack(pady=10)
        
        # Summary frame
        summary_frame = ttk.Frame(frame)
        summary_frame.pack(fill="x", pady=20)
        
        ttk.Label(
            summary_frame,
            text=f"Initial Investment: ${self.invested_amount:,.2f}",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        ttk.Label(
            summary_frame,
            text=f"Final Portfolio Value: ${final_value:,.2f}",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        # Profit/Loss display
        pl_color = "#4CAF50" if profit_loss >= 0 else "#F44336"
        pl_text = "Profit" if profit_loss >= 0 else "Loss"
        
        ttk.Label(
            summary_frame,
            text=f"{pl_text}: ${abs(profit_loss):,.2f} ({pl_percent:+.2f}%)",
            font=("Helvetica", 14, "bold"),
            foreground=pl_color
        ).pack(anchor="w", pady=10)
        
        # Show the final chart
        self.create_combined_chart(frame)
        
        # Update chart with final data
        for symbol, line in self.stock_lines.items():
            line.set_data(self.time_points, self.historical_data[symbol])
        self.portfolio_line.set_data(self.time_points, self.portfolio_history)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        
        # Action buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(
            button_frame,
            text="New Simulation",
            command=self.create_investment_page
        ).pack(side="left", padx=10)
        
        ttk.Button(
            button_frame,
            text="Back to Dashboard",
            command=self.create_welcome_page
        ).pack(side="right", padx=10)
    
    def clear_window(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StockInvestmentSimulator(root)
    root.mainloop()