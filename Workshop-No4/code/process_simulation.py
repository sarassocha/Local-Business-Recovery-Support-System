import simpy
import random
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# =========================================================
# PROCESS SIMULATION - SINGLE LOCAL STORE
# Workshop 4 - 7 days (Monday to Sunday)
# =========================================================

SIMULATION_TIME = 7

# =========================================================
# TICS (Time steps: t1 = Monday, t2 = Tuesday, ..., t7 = Sunday)
# =========================================================

TIC_NAMES = {
    0: "t1\nMon",
    1: "t2\nTue",
    2: "t3\nWed",
    3: "t4\nThu",
    4: "t5\nFri",
    5: "t6\nSat",
    6: "t7\nSun"
}

# Rango de visitantes por día (min, max)
CC_VISITORS_RANGE = {
    "t1\nMon": (6000, 8000),
    "t2\nTue": (6000, 8000),
    "t3\nWed": (6000, 8000),
    "t4\nThu": (6000, 8000),
    "t5\nFri": (10000, 12000),
    "t6\nSat": (28000, 32000),
    "t7\nSun": (30000, 34000)
}

# =========================================================
# STORE CALCULATIONS
# =========================================================
LOCAL_STORE_PERCENTAGE = 0.1176
STORE_SHARE_PERCENTAGE = 0.04

# Tasas de conversión por escenario
CONVERSION_RATES = {
    "baseline": 0.30,      # 30% normal
    "optimization": 0.50,  # 50% con promociones
    "failure": 0.18        # 18% por problemas (lluvia)
}

# Efecto de lluvia en visitantes (aumenta flujo pero reduce conversión)
RAIN_VISITOR_BOOST = 1.3   # +30% visitantes cuando llueve
RAIN_CONVERSION_PENALTY = 0.7  # -30% de conversión cuando llueve

INVENTORY_START = 150
ALERT_THRESHOLD = 50

# =========================================================
# SIMULATION CLASS
# =========================================================

class Simulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Titan Plaza - Process Simulation with TICS")
        self.root.geometry("1200x800")
        
        self.inventory = INVENTORY_START
        self.total_sales = 0
        self.customers_served = 0
        self.alerts = 0
        
        self.tics_list = []
        self.daily_sales = []
        self.daily_inventory = []
        self.daily_buyers = []
        self.daily_cc_visitors = []
        self.daily_potential_customers = []
        self.full_log = []
        
        self.create_widgets()
        
    def create_widgets(self):
        control_frame = ttk.LabelFrame(self.root, text="Simulation Controls", padding=10)
        control_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(control_frame, text="Scenario:").grid(row=0, column=0, padx=5)
        self.scenario_var = tk.StringVar(value="optimization")
        scenario_combo = ttk.Combobox(control_frame, textvariable=self.scenario_var, 
                                       values=["baseline", "optimization", "failure"], width=15)
        scenario_combo.grid(row=0, column=1, padx=5)
        
        self.run_button = ttk.Button(control_frame, text="RUN SIMULATION", command=self.run_simulation)
        self.run_button.grid(row=0, column=2, padx=10)
        
        log_frame = ttk.LabelFrame(self.root, text="Simulation Log", padding=10)
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = tk.Text(log_frame, height=15, width=80, wrap=tk.WORD)
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        graph_frame = ttk.LabelFrame(self.root, text="Simulation Graphs", padding=10)
        graph_frame.pack(fill="x", padx=10, pady=5)
        
        self.graph_area = ttk.Frame(graph_frame)
        self.graph_area.pack()
        
    def add_log(self, message):
        self.full_log.append(message)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def process_customer(self, env, customer_id, conversion_rate):
        browse_time = random.uniform(1.0, 4.0)
        yield env.timeout(browse_time)
        
        buys = random.random() < conversion_rate
        
        if not buys:
            return
        
        self.total_sales += 1
        self.inventory -= 1
        self.customers_served += 1
        
        self.add_log(f"      Customer {customer_id} bought. Inventory left: {self.inventory}")
    
    def customer_generator(self, env):
        while True:
            tic_index = int(env.now) % 7
            tic_name = TIC_NAMES[tic_index]
            
            # Obtener rango y generar visitantes aleatorios
            min_visitors, max_visitors = CC_VISITORS_RANGE[tic_name]
            cc_visitors = random.randint(min_visitors, max_visitors)
            
            scenario = self.scenario_var.get()
            
            # =============================================
            # EFECTOS POR ESCENARIO
            # =============================================
            
            # 1. LLUVIA (solo en failure)
            is_raining = False
            if scenario == "failure" and random.random() < 0.4:  # 40% probabilidad de lluvia
                is_raining = True
                cc_visitors = int(cc_visitors * RAIN_VISITOR_BOOST)
            
            # 2. CONECTIVIDAD (solo en failure)
            connectivity_issue = False
            if scenario == "failure" and random.random() < 0.3:  # 30% probabilidad
                connectivity_issue = True
            
            # 3. TASA DE CONVERSIÓN BASE
            conversion_rate = CONVERSION_RATES[scenario]
            
            # 4. APLICAR PENALIZACIONES POR LLUVIA (solo en failure)
            if is_raining:
                conversion_rate = conversion_rate * RAIN_CONVERSION_PENALTY
            
            # 5. APLICAR PENALIZACIONES POR CONECTIVIDAD (solo en failure)
            if connectivity_issue:
                conversion_rate = conversion_rate * 0.85  # 15% menos por problemas técnicos
            
            # Asegurar límites realistas
            conversion_rate = max(0.10, min(0.60, conversion_rate))
            
            # Calcular clientes potenciales de la tienda
            local_store_visitors = int(cc_visitors * LOCAL_STORE_PERCENTAGE)
            potential_customers = int(local_store_visitors * STORE_SHARE_PERCENTAGE)
            potential_customers = max(1, potential_customers)
            
            # Log de condiciones
            self.add_log(f"")
            self.add_log(f"{tic_name}")
            if is_raining:
                self.add_log(f"  WEATHER: Rainy (+{int((RAIN_VISITOR_BOOST-1)*100)}% visitors, -{int((1-RAIN_CONVERSION_PENALTY)*100)}% conversion)")
            else:
                self.add_log(f"  WEATHER: Sunny")
            
            if connectivity_issue:
                self.add_log(f"  CONNECTION: OFFLINE (data sync issues)")
            else:
                self.add_log(f"  CONNECTION: ONLINE")
            
            self.add_log(f"  Visitors at Titan Plaza: {cc_visitors:,}")
            self.add_log(f"  Visitors in local stores (11.76%): {local_store_visitors:,}")
            self.add_log(f"  Potential customers for this store: {potential_customers}")
            self.add_log(f"  Conversion rate: {conversion_rate*100:.0f}%")
            
            previous_buyers = self.customers_served
            
            for i in range(potential_customers):
                env.process(self.process_customer(env, i, conversion_rate))
            
            yield env.timeout(1)
            
            daily_buyers = self.customers_served - previous_buyers
            
            self.add_log(f"  Customers who bought: {daily_buyers}")
            self.add_log(f"  Inventory left: {self.inventory}")
            
            self.tics_list.append(tic_name)
            self.daily_sales.append(self.total_sales)
            self.daily_inventory.append(self.inventory)
            self.daily_buyers.append(daily_buyers)
            self.daily_cc_visitors.append(cc_visitors)
            self.daily_potential_customers.append(potential_customers)
            
            # Restock según escenario
            if self.inventory < ALERT_THRESHOLD:
                self.alerts += 1
                self.add_log(f"  ALERT: Low inventory ({self.inventory} units remaining)")
                
                if scenario == "optimization":
                    yield env.timeout(1)
                    self.inventory += 100
                    self.add_log(f"  Auto restock: +100 units (total {self.inventory})")
                elif scenario == "failure":
                    yield env.timeout(5)
                    self.inventory += 50
                    self.add_log(f"  Slow restock due to issues: +50 units (total {self.inventory})")
                else:
                    yield env.timeout(3)
                    self.inventory += 50
                    self.add_log(f"  Restock ordered: +50 units (total {self.inventory})")
    
    def show_graphs(self):
        for widget in self.graph_area.winfo_children():
            widget.destroy()
        
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(14, 5))
        
        # Graph 1: CC Visitors per TIC
        ax1.bar(self.tics_list, self.daily_cc_visitors, color='blue', edgecolor='black')
        ax1.set_title(f'Titan Plaza Visitors - {self.scenario_var.get().upper()}')
        ax1.set_xlabel('TIC (t1 to t7)')
        ax1.set_ylabel('Number of Visitors')
        
        # Graph 2: Potential vs Actual customers
        x = range(len(self.tics_list))
        width = 0.35
        ax2.bar([i - width/2 for i in x], self.daily_potential_customers, width, label='Potential', color='orange')
        ax2.bar([i + width/2 for i in x], self.daily_buyers, width, label='Actual Buyers', color='green')
        ax2.set_title(f'Potential vs Actual Buyers - {self.scenario_var.get().upper()}')
        ax2.set_xlabel('TIC (t1 to t7)')
        ax2.set_ylabel('Number of Customers')
        ax2.set_xticks(x)
        ax2.set_xticklabels(self.tics_list)
        ax2.legend()
        
        # Graph 3: Inventory over time
        ax3.plot(self.tics_list, self.daily_inventory, 'r-', linewidth=2, marker='o')
        ax3.axhline(y=ALERT_THRESHOLD, color='r', linestyle='--', label='Alert Threshold')
        ax3.set_title(f'Inventory Level - {self.scenario_var.get().upper()}')
        ax3.set_xlabel('TIC (t1 to t7)')
        ax3.set_ylabel('Inventory (units)')
        ax3.legend()
        
        plt.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        canvas.draw()
        canvas.get_tk_widget().pack()
    
    def run_simulation(self):
        self.inventory = INVENTORY_START
        self.total_sales = 0
        self.customers_served = 0
        self.alerts = 0
        
        self.tics_list.clear()
        self.daily_sales.clear()
        self.daily_inventory.clear()
        self.daily_buyers.clear()
        self.daily_cc_visitors.clear()
        self.daily_potential_customers.clear()
        self.full_log.clear()
        
        self.log_text.delete(1.0, tk.END)
        
        self.add_log("="*60)
        self.add_log("PROCESS SIMULATION - SINGLE LOCAL STORE")
        self.add_log("7 TICS (t1 = Monday, t2 = Tuesday, ..., t7 = Sunday)")
        scenario = self.scenario_var.get()
        self.add_log(f"Scenario: {scenario.upper()}")
        self.add_log("="*60)
        self.add_log("")
        
        if scenario == "baseline":
            self.add_log("BASELINE CONDITIONS:")
            self.add_log("  - Conversion rate: 30%")
            self.add_log("  - No promotions")
            self.add_log("  - Normal restock speed")
        elif scenario == "optimization":
            self.add_log("OPTIMIZATION CONDITIONS:")
            self.add_log("  - Conversion rate: 50% (+20% vs baseline)")
            self.add_log("  - Promotions active")
            self.add_log("  - Fast auto-restock")
        else:
            self.add_log("FAILURE CONDITIONS:")
            self.add_log("  - Conversion rate: 18% (reduced by technical issues)")
            self.add_log("  - Rain reduces conversion further")
            self.add_log("  - Connectivity issues cause data loss")
            self.add_log("  - Slow restock")
        
        self.add_log("="*60)
        self.add_log("")
        
        env = simpy.Environment()
        env.process(self.customer_generator(env))
        env.run(until=SIMULATION_TIME)
        
        self.add_log("")
        self.add_log("="*60)
        self.add_log("SIMULATION RESULTS - 7 TICS")
        self.add_log("="*60)
        self.add_log(f"Scenario: {scenario}")
        self.add_log(f"Total customers who bought: {self.customers_served}")
        self.add_log(f"Total sales (units): {self.total_sales}")
        self.add_log(f"Final inventory: {self.inventory} units")
        self.add_log(f"Inventory alerts triggered: {self.alerts}")
        self.add_log("="*60)
        
        self.show_graphs()


if __name__ == "__main__":
    root = tk.Tk()
    app = Simulation(root)
    root.mainloop()