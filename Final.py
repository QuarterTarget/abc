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
        
        #This next portion is almost all codes for the GUI. I will label each section with a comment so it is visible who did what and what it does.
        # Stock data with color coding. This part was made with Chatgpt, mostly due to me not being arsed to manually type it out. Are you serious? My fingers will hurt
        self.stocks = [
            {"name": "Tesla", "symbol": "TSLA", "price": 25.50, "volatility": random.uniform(-4, 4), "shares": 0, "color": "#1f77b4"},
            {"name": "Apple", "symbol": "AAPL", "price": 18.75, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#ff7f0e"},
            {"name": "Amazon", "symbol": "AMZN", "price": 15.20, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#2ca02c"},
            {"name": "Silly strange crypto some guy advertised on twitter", "symbol": "SCAM", "price": 69.42, "volatility":  random.uniform(-100, 100), "shares": 0, "color": "#964b00"},
            {"name": "Google", "symbol": "GOOGL", "price": 14.80, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#d62728"},
            {"name": "Microsoft", "symbol": "MSFT", "price": 30.25, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#9467bd"},                #The prices are low and the budget is high. I might change this later but tbh I will keep it. if it works dont fix it!
            {"name": "Netflix", "symbol": "NFLX", "price": 40.60, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#8c564b"},                  #volatility will determine how much the different stocks change in price. for example a higher volatility means higher jumps in price. 
            {"name": "Nvidia", "symbol": "NVDA", "price": 60.75, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#e377c2"},                   #volatility is determined by a random number generator I have created
            {"name": "Meta", "symbol": "META", "price": 35.40, "volatility":  random.uniform(-4, 4), "shares": 0, "color": "#7f7f7f"}
            
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
            text="📈 Stock Investment Simulator 📉",          #Heh, emojis
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)
        
        description = ttk.Label(
            frame,
            text="Invest in simulated stocks and track your portfolio performance with the MarcMax Ultra Realistic Stock Simulator!",
            font=("Helvetica", 12),        #Helvetic looks neat and it fits with the GUI we shamelessly stole from Github
            wraplength=600
        )
        description.pack(pady=10)
 # Display current balance. Made by me. With a lot of cursing. Did you know chatgpt is incapable of making a simple label? AHHHHHHHH
        self.balance_label = ttk.Label(
            frame,
            text=f"Starting Balance: ${self.initial_balance:,.2f}",        #to be fully serious, I used some youtube tutorial for this. 
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
        
        # Left panel - Trading controls. I learned how to frame things! Yay!                   
        control_frame = ttk.Frame(main_frame, width=350)
        control_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        # Right panel - Chart
        chart_frame = ttk.Frame(main_frame)
        chart_frame.pack(side="right", expand=True, fill="both", padx=10, pady=10)
        
        # Trading controls. .pack is needed 
        ttk.Label(
            control_frame,
            text="Investment Controls",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # udpates and shows the current balance of the veri smart investor 
        self.update_balance_display(control_frame)
        
        # Stock selection. I thought a dropdown menu like this is pretty cool. Tutorial was needed. Thanks random bengali guy on youtube! I was thinking about adding the current price of the stock as well.
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
        
        # Shares the input
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
        
        # Buy/Sell buttons. Pretty simple
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
        
        # Portfolio summary box. shows the current portfolio of the user. I used a treeview for this.
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
        self.portfolio_tree.heading("value", text="Value")                           #This was reformatted with AI. same excuse as before. my fingers hurt and I hate repetetive typing
        self.portfolio_tree.column("symbol", width=80)
        self.portfolio_tree.column("shares", width=80, anchor="e")
        self.portfolio_tree.column("price", width=90, anchor="e")
        self.portfolio_tree.column("value", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=self.portfolio_tree.yview)
        self.portfolio_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.portfolio_tree.pack(fill="both", expand=True)
        
        # simulation controls. 
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
        
        # Creates the portfolio chart. I think? It works? hmmm
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
            font=("Helvetica", 12, "bold"),                                  #oH my god! This section broke me. I HATE CHARTS
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
        
        # Axes verändert. Max
        for spine in self.ax.spines.values():
            spine.set_color('#444')
        self.ax.tick_params(colors='white')
        self.ax.yaxis.label.set_color('white')
        self.ax.xaxis.label.set_color('white')
        self.ax.title.set_color('white')
        
        # leere portfolio line. Max
        self.portfolio_line, = self.ax.plot([], [], 'w-', linewidth=2, label="Portfolio Value")
        
        self.ax.set_title("Portfolio Value Over Time", pad=20)
        self.ax.set_xlabel("Time (s)", labelpad=10)
        self.ax.set_ylabel("Value ($)", labelpad=10)
        self.ax.legend()
        self.ax.grid(True, color='#444', linestyle='--', alpha=0.5)
        
        # ganzi in TKinter einfügen. Max
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
        
        # findet stock in der liste. Max
        stock = next((s for s in self.stocks if s["symbol"] == selected), None)
        if not stock:
            return
        
        if action == "buy":
            total_cost = shares * stock["price"]
            if total_cost > self.user_balance:
                messagebox.showwarning("Insufficient Funds", 
                                    f"You don't have enough funds to buy {shares} shares of {selected}")
                return
            
            # executes the buy
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
            
            # executes the sell
            total_value = shares * stock["price"]
            stock["shares"] -= shares
            self.user_balance += total_value
            self.invested_amount -= total_value
            
            messagebox.showinfo("Trade Executed", 
                             f"Sold {shares} shares of {selected} at ${stock['price']:,.2f}")
        
        # changes the UI and updates the portfolio. before I added this it was a mess and you had to go back and forth and reset before it would register any change
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
        
        # nimmt vorherige historical daten.
        for stock in self.stocks:
            self.historical_data[stock["symbol"]] = [stock["price"]]
        
        # OK OK OK it works? sorta?? This opens the simulation.
        self.create_simulation_page()
        
        # start animation. this uses the funcanimation I mentioned at the start. Deepseek many thanks! I will donate to the chinese gov. for this. 
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
        
        # mit ttk ein header mit information. max
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
        
        # display von value.
        self.portfolio_value_label = ttk.Label(
            frame,
            text="Portfolio Value: $0.00",
            font=("Helvetica", 14, "bold"),
            foreground="#4CAF50"
        )
        self.portfolio_value_label.pack(pady=10)
        
        # portfolio chart recreation
        self.create_portfolio_chart(frame)
        
        # the stop button. now pressing it during the simulation honestly really doesnt do anything. it kind of freezes and doesnt properly work. will keep it inside though
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
        
        # Update the price of the stocks, but only the ones that are invested. obviously
        portfolio_value = 0
        for stock in self.stocks:
            if stock["shares"] > 0:
                # Random price change based on volatility using the random. import 
                change = random.uniform(-2, 2) * stock["volatility"]
                stock["price"] = max(0.01, stock["price"] + change)
                self.historical_data[stock["symbol"]].append(stock["price"])
                
                # Adds said change to portfolio value
                portfolio_value += stock["shares"] * stock["price"]
        
        self.portfolio_history.append(portfolio_value)
        
        # Updates the UI
        self.sim_time_label.config(text=f"Time: {self.current_time}s")
        self.portfolio_value_label.config(text=f"Portfolio Value: ${portfolio_value:,.2f}")
        
        # Updates the  portfolio line
        if len(self.time_points) == len(self.portfolio_history):
            self.portfolio_line.set_data(self.time_points, self.portfolio_history)
        
        # Adjusts view so that the graph is always visible and not cutting off. first iteration kept doing this. Max fixed it. Thanks Max
        self.ax.relim()
        self.ax.autoscale_view()
        
        # we made a 30 second sim time in total. so at 30 secs the simulation stops and the value of the stock at 30 seconds is recorded.
        if self.current_time >= self.simulation_duration:
            self.stop_simulation()
        
        return [self.portfolio_line]
    
    def stop_simulation(self):
        """Stop the simulation and show results"""
        self.simulation_active = False
        if hasattr(self, 'ani'):
            self.ani.event_source.stop()
        self.show_results()
    
    def show_results(self):
        """Show final results with detailed analysis"""
        # calculates the final value of the portfolio
        final_value = sum(stock["shares"] * stock["price"] for stock in self.stocks)
        profit_loss = final_value - self.invested_amount
        pl_percent = (profit_loss / self.invested_amount) * 100 if self.invested_amount else 0
        
        # creates a results window. opens it in a new window
        result_window = tk.Toplevel(self.root)
        result_window.title("Simulation Results")
        result_window.geometry("1100x900")
        
        # Main container
        main_frame = ttk.Frame(result_window, padding=20)
        main_frame.pack(expand=True, fill="both")
        
        # Results header
        ttk.Label(
            main_frame,
            text="Simulation Results",
            font=("Helvetica", 20, "bold")
        ).pack(pady=10)
        
        # Summary frame
        summary_frame = ttk.Frame(main_frame)
        summary_frame.pack(fill="x", pady=20)
        
        # Portfolio summary
        pl_color = "#4CAF50" if profit_loss >= 0 else "#F44336"
        pl_text = "PROFIT" if profit_loss >= 0 else "LOSS"
        
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
        
        ttk.Label(
            summary_frame,
            text=f"{pl_text}: ${abs(profit_loss):,.2f} ({pl_percent:+.2f}%)",
            font=("Helvetica", 14, "bold"),
            foreground=pl_color
        ).pack(anchor="w", pady=10)
        
        # Stock performance details section thingie
        ttk.Separator(main_frame).pack(fill="x", pady=10)
        ttk.Label(
            main_frame,
            text="Stock Performance Details",
            font=("Helvetica", 16, "bold")
        ).pack(pady=10)
        
        # Create a notebook for different views
        notebook = ttk.Notebook(main_frame)
        notebook.pack(expand=True, fill="both", pady=10)
        
        # Tab 1: Performance Table                                                                       #Now i was going to add a second tab to show a historical slider of the stocks
        table_frame = ttk.Frame(notebook)                                                                #However, this just DID not work. i just removed it and it seems to be fine as it is. if there is any strange code here that seems to be not needed its because i forgot to remove it and it doesnt affect the code
        notebook.add(table_frame, text="Performance Table")
        
        # Create treeview for stock performance
        columns = ("symbol", "name", "shares", "start", "end", "change", "value")
        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=8
        )
        
        # Configure columns
        tree.heading("symbol", text="Symbol")
        tree.heading("name", text="Company")
        tree.heading("shares", text="Shares")
        tree.heading("start", text="Start Price")
        tree.heading("end", text="End Price")
        tree.heading("change", text="Change")
        tree.heading("value", text="Value")
        
        tree.column("symbol", width=80, anchor="center")
        tree.column("name", width=120, anchor="w")
        tree.column("shares", width=80, anchor="e")
        tree.column("start", width=100, anchor="e")
        tree.column("end", width=100, anchor="e")
        tree.column("change", width=100, anchor="e")
        tree.column("value", width=120, anchor="e")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Populate with invested stocks
        for stock in self.stocks:
            if stock["shares"] > 0:
                start_price = self.historical_data[stock["symbol"]][0]
                end_price = stock["price"]
                change = end_price - start_price
                change_percent = (change / start_price) * 100
                value = stock["shares"] * end_price
                
                tree.insert("", "end", values=(
                    stock["symbol"],
                    stock["name"],
                    stock["shares"],
                    f"${start_price:,.2f}",
                    f"${end_price:,.2f}",
                    f"{'+' if change >= 0 else ''}{change:,.2f} ({change_percent:+.2f}%)",
                    f"${value:,.2f}"
                ), tags=("profit" if change >= 0 else "loss"))
        
        # Configure tag colors
        tree.tag_configure("profit", foreground="#4CAF50")
        tree.tag_configure("loss", foreground="#F44336")
        
        # Action button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=20)
        
        ttk.Button(
            button_frame,
            text="Try Again",
            command=lambda: [result_window.destroy(), self.reset_and_restart()],
            style="Accent.TButton"
        ).pack(expand=True)
        
        result_window.transient(self.root)
        result_window.grab_set()
        self.root.wait_window(result_window)
    
    def update_interactive_view(self, *args):
        """Update the interactive view based on slider position"""
        time_idx = self.slider_var.get()
        if time_idx >= len(self.time_points):
            return
        
        self.interactive_ax.clear()
        
        # Update time label
        self.time_label.config(text=f"{self.time_points[time_idx]}s")
        
        # Plot all invested stocks up to current time
        for stock in self.stocks:
            if stock["shares"] > 0:
                self.interactive_ax.plot(
                    self.time_points[:time_idx+1],
                    self.historical_data[stock["symbol"]][:time_idx+1],
                    '-',
                    color=stock["color"],
                    linewidth=1.5,
                    label=f"{stock['symbol']}"
                )
        
        self.interactive_ax.set_title(f"Stock Prices at {self.time_points[time_idx]}s", pad=20)
        self.interactive_ax.set_xlabel("Time (s)", labelpad=10)
        self.interactive_ax.set_ylabel("Price ($)", labelpad=10)
        self.interactive_ax.legend()
        self.interactive_ax.grid(True, color='#444', linestyle='--', alpha=0.5)
        self.interactive_ax.set_xlim(0, self.time_points[-1])
        
        self.interactive_canvas.draw()
    
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
       
      