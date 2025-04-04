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
        self.root.geometry("1100x800")
        
        # Apply modern theme
        sv_ttk.set_theme("dark")
        
        # Initialize game state
        self.reset_game()
        
        # Initialize UI
        self.create_welcome_page()
    
    def reset_game(self):
        """Reset all game variables to initial state"""
        self.initial_balance = 50000
        self.user_balance = self.initial_balance
        self.invested_amount = 0
        self.invested_stocks = []
        self.simulation_active = False
        self.simulation_duration = 30  # seconds
        self.current_time = 0
        
        # Stock data with color coding
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
        
        # Right panel - Combined chart
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
        
        # Create the combined chart
        self.create_combined_chart(chart_frame)
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
    
    def create_combined_chart(self, parent):
        """Create the combined stock and portfolio chart"""
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
        
        # Create empty plots - we'll create actual lines when simulation starts
        self.stock_lines = {}
        self.portfolio_line = None
        
        self.ax.set_title("Stock Prices & Portfolio Value", pad=20)
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
                ))
    
    def start_simulation(self):
        """Start the stock simulation"""
        self.simulation_active = True
        self.current_time = 0
        self.time_points = []
        self.portfolio_history = []
        
        # Initialize historical data
        for stock in self.stocks:
            self.historical_data[stock["symbol"]] = [stock["price"]]
        
        # Create simulation page
        self.create_simulation_page()
        
        # Initialize plot lines for invested stocks only
        self.ax.clear()  # Clear previous lines
        
        # Create lines for invested stocks
        self.stock_lines = {}
        for stock in self.stocks:
            if stock["shares"] > 0:
                line, = self.ax.plot([], [], '-', 
                                   color=stock["color"],
                                   linewidth=1.5,
                                   label=f"{stock['symbol']}")
                self.stock_lines[stock["symbol"]] = line
        
        # Create portfolio line (thicker)
        self.portfolio_line, = self.ax.plot([], [], 'w-', linewidth=3, label="PORTFOLIO")
        
        # Reconfigure plot
        self.ax.set_title("Stock Prices & Portfolio Value", pad=20)
        self.ax.set_xlabel("Time (s)", labelpad=10)
        self.ax.set_ylabel("Value ($)", labelpad=10)
        self.ax.legend()
        self.ax.grid(True, color='#444', linestyle='--', alpha=0.5)
        
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
            command=self.stop_simulation,
            style="Accent.TButton"
        )
        self.stop_button.pack(pady=10)
    
    def update_simulation(self, frame):
        """Update function for the animation"""
        if not self.simulation_active:
            return
        
        self.current_time += 1
        self.time_points.append(self.current_time)
        
        # Update stock prices (only for invested stocks)
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
        
        # Update all lines for invested stocks
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
        """Stop the simulation and show results"""
        self.simulation_active = False
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
        self.show_results()
    
    def show_results(self):
        """Show final results and ask to play again"""
        # Calculate final values
        final_value = sum(stock["shares"] * stock["price"] for stock in self.stocks)
        profit_loss = final_value - self.invested_amount
        pl_percent = (profit_loss / self.invested_amount) * 100 if self.invested_amount else 0
        
        # Show results dialog
        pl_color = "#4CAF50" if profit_loss >= 0 else "#F44336"
        pl_text = "PROFIT" if profit_loss >= 0 else "LOSS"
        
        result_window = tk.Toplevel(self.root)
        result_window.title("Simulation Results")
        result_window.geometry("500x400")
        
        frame = ttk.Frame(result_window, padding=20)
        frame.pack(expand=True, fill="both")
        
        ttk.Label(
            frame,
            text="Simulation Complete!",
            font=("Helvetica", 18, "bold")
        ).pack(pady=10)
        
        # Results summary
        summary_frame = ttk.Frame(frame)
        summary_frame.pack(fill="x", pady=20)
        
        ttk.Label(
            summary_frame,
            text=f"Initial Investment: ${self.invested_amount:,.2f}",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        ttk.Label(
            summary_frame,
            text=f"Final Value: ${final_value:,.2f}",
            font=("Helvetica", 12)
        ).pack(anchor="w", pady=5)
        
        ttk.Label(
            summary_frame,
            text=f"{pl_text}: ${abs(profit_loss):,.2f} ({pl_percent:+.2f}%)",
            font=("Helvetica", 14, "bold"),
            foreground=pl_color
        ).pack(anchor="w", pady=10)
        
        # Action buttons
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(
            button_frame,
            text="Try Again",
            command=lambda: [result_window.destroy(), self.reset_and_restart()],
            style="Accent.TButton"
        ).pack(side="left", padx=10)
        
        ttk.Button(
            button_frame,
            text="Quit",
            command=self.root.quit
        ).pack(side="right", padx=10)
        
        result_window.transient(self.root)
        result_window.grab_set()
        self.root.wait_window(result_window)
    
    def reset_and_restart(self):
        """Reset the game and return to welcome page"""
        self.reset_game()
        self.create_welcome_page()
    
    def clear_window(self):
        """Clear all widgets from the root window"""
        for widget in self.root.winfo_children():
            widget.destroy()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = StockInvestmentSimulator(root)
    root.mainloop()