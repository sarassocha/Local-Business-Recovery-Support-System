import simpy
import random
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt

# =========================================================
# TITAN PLAZA - BEHAVIOR ORIENTED SIMULATION
# Workshop 4
# =========================================================

# =========================================================
# CONFIGURATION
# =========================================================

SIMULATION_TIME = 100

# Change scenario here:
# "baseline"
# "optimization"
# "failure"

scenario = "failure"

# =========================================================
# GLOBAL VARIABLES
# =========================================================

inventory = 100
sales = 0
customers = 0
alerts = 0

connectivity = True
sync_delay = 0

response_time = 1.0

weather = "sunny"

# =========================================================
# METRICS
# =========================================================

time_history = []
sales_history = []
inventory_history = []
customers_history = []
delay_history = []
response_history = []
alerts_history = []

# =========================================================
# TKINTER GUI
# =========================================================

root = tk.Tk()

root.title("Titan Plaza Behavior Simulation")

root.geometry("450x500")

# ---------------------------------------------------------

title_label = ttk.Label(
    root,
    text="Titan Plaza Simulation",
    font=("Arial", 16)
)

title_label.pack(pady=10)

# ---------------------------------------------------------

scenario_label = ttk.Label(
    root,
    text=f"Scenario: {scenario.upper()}",
    font=("Arial", 12)
)

scenario_label.pack(pady=5)

# ---------------------------------------------------------

time_label = ttk.Label(
    root,
    text="Time: 0"
)

time_label.pack()

# ---------------------------------------------------------

weather_label = ttk.Label(
    root,
    text="Weather: SUNNY"
)

weather_label.pack()

# ---------------------------------------------------------

customer_label = ttk.Label(
    root,
    text="Customers: 0"
)

customer_label.pack()

# ---------------------------------------------------------

sales_label = ttk.Label(
    root,
    text="Sales: 0"
)

sales_label.pack()

# ---------------------------------------------------------

inventory_label = ttk.Label(
    root,
    text="Inventory: 100"
)

inventory_label.pack()

# ---------------------------------------------------------

connection_label = ttk.Label(
    root,
    text="Connection: ONLINE"
)

connection_label.pack()

# ---------------------------------------------------------

delay_label = ttk.Label(
    root,
    text="Sync Delay: 0"
)

delay_label.pack()

# ---------------------------------------------------------

response_label = ttk.Label(
    root,
    text="Response Time: 1.0"
)

response_label.pack()

# ---------------------------------------------------------

alert_label = ttk.Label(
    root,
    text="Alerts: 0"
)

alert_label.pack()

# ---------------------------------------------------------

status_label = ttk.Label(
    root,
    text="System Running",
    font=("Arial", 10)
)

status_label.pack(pady=10)

# =========================================================
# WEATHER SYSTEM
# =========================================================

def weather_system(env):

    global weather

    while True:

        # 30% chance weather changes

        if random.random() < 0.3:

            if weather == "sunny":

                weather = "rainy"

            else:

                weather = "sunny"

        yield env.timeout(1)

# =========================================================
# CUSTOMER AND SALES SYSTEM
# =========================================================

def customer_generator(env):

    global customers
    global sales
    global inventory
    global alerts
    global response_time

    while True:

        # -------------------------------------------------
        # TRAFFIC MODEL BASED ON DAYS
        # -------------------------------------------------

        day_type = env.now % 7

        # Monday - Thursday
        if day_type in [0, 1, 2, 3]:

            base_customers = random.randint(10, 18)

        # Friday
        elif day_type == 4:

            base_customers = random.randint(18, 28)

        # Saturday / Sunday
        else:

            base_customers = random.randint(25, 40)

        # -------------------------------------------------
        # WEATHER EFFECT
        # -------------------------------------------------

        if weather == "rainy":

            base_customers = int(base_customers * 0.7)

        # -------------------------------------------------
        # RANDOM VARIABILITY
        # -------------------------------------------------

        traffic_variation = random.randint(-3, 3)

        customers = max(
            0,
            base_customers + traffic_variation
        )

        # -------------------------------------------------
        # SCENARIO EFFECTS
        # -------------------------------------------------

        promotion_multiplier = 1.0

        # BASELINE
        if scenario == "baseline":

            response_time = round(
                random.uniform(1.0, 2.0),
                2
            )

        # OPTIMIZATION
        elif scenario == "optimization":

            promotion_multiplier = 1.4

            response_time = round(
                random.uniform(0.5, 1.5),
                2
            )

        # FAILURE
        elif scenario == "failure":

            if not connectivity:

                customers = int(customers * 0.7)

                response_time = round(
                    random.uniform(2.0, 5.0),
                    2
                )

            else:

                response_time = round(
                    random.uniform(1.0, 2.5),
                    2
                )

        # -------------------------------------------------
        # SALES GENERATION
        # -------------------------------------------------

        if inventory > 0:

            generated_sales = int(

                customers *
                promotion_multiplier *
                random.uniform(0.5, 1.0)

            )

            # Prevent overselling
            generated_sales = min(
                generated_sales,
                inventory
            )

            sales += generated_sales

            inventory -= generated_sales

        # -------------------------------------------------
        # INVENTORY ALERTS
        # -------------------------------------------------

        if inventory < 20:

            alerts += 1

            # Optimization restock
            if scenario == "optimization":

                yield env.timeout(1)

                inventory += 40

            else:

                yield env.timeout(3)

                inventory += 25

        yield env.timeout(1)

# =========================================================
# CONNECTIVITY SYSTEM
# =========================================================

def connectivity_monitor(env):

    global connectivity
    global sync_delay

    while True:

        if scenario == "failure":

            # 30% probability of failure

            if random.random() < 0.3:

                connectivity = False

                sync_delay = random.randint(2, 8)

            else:

                connectivity = True

                sync_delay = 0

        else:

            connectivity = True

            sync_delay = 0

        yield env.timeout(1)

# =========================================================
# METRICS COLLECTION
# =========================================================

def metrics_collector(env):

    while True:

        time_history.append(env.now)

        sales_history.append(sales)

        inventory_history.append(inventory)

        customers_history.append(customers)

        delay_history.append(sync_delay)

        response_history.append(response_time)

        alerts_history.append(alerts)

        yield env.timeout(1)

# =========================================================
# GUI UPDATE
# =========================================================

def update_gui(env):

    while True:

        # -------------------------------------------------
        # UPDATE LABELS
        # -------------------------------------------------

        time_label.config(
            text=f"Day: {env.now}"
        )

        weather_label.config(
            text=f"Weather: {weather.upper()}"
        )

        customer_label.config(
            text=f"Customers: {customers}"
        )

        sales_label.config(
            text=f"Sales: {sales}"
        )

        inventory_label.config(
            text=f"Inventory: {inventory}"
        )

        delay_label.config(
            text=f"Sync Delay: {sync_delay}"
        )

        response_label.config(
            text=f"Response Time: {response_time}"
        )

        alert_label.config(
            text=f"Alerts: {alerts}"
        )

        # -------------------------------------------------
        # CONNECTION STATUS
        # -------------------------------------------------

        if connectivity:

            connection_label.config(
                text="Connection: ONLINE"
            )

        else:

            connection_label.config(
                text="Connection: OFFLINE"
            )

        # -------------------------------------------------
        # STATUS WARNINGS
        # -------------------------------------------------

        if inventory < 20:

            status_label.config(
                text="LOW INVENTORY ALERT"
            )

        elif not connectivity:

            status_label.config(
                text="CONNECTIVITY FAILURE"
            )

        else:

            status_label.config(
                text="System Running"
            )

        root.update()

        yield env.timeout(1)

# =========================================================
# CREATE ENVIRONMENT
# =========================================================

env = simpy.Environment()

env.process(weather_system(env))

env.process(customer_generator(env))

env.process(connectivity_monitor(env))

env.process(metrics_collector(env))

env.process(update_gui(env))

# =========================================================
# GRAPH GENERATION
# =========================================================

def generate_graphs():

    # -----------------------------------------------------
    # SALES GRAPH
    # -----------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        time_history,
        sales_history
    )

    plt.title(
        f"Sales Behavior - {scenario.upper()}"
    )

    plt.xlabel("Days")

    plt.ylabel("Sales")

    plt.grid(True)

    plt.show()

    # -----------------------------------------------------
    # INVENTORY GRAPH
    # -----------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        time_history,
        inventory_history
    )

    plt.title(
        f"Inventory Levels - {scenario.upper()}"
    )

    plt.xlabel("Days")

    plt.ylabel("Inventory")

    plt.grid(True)

    plt.show()

    # -----------------------------------------------------
    # RESPONSE TIME GRAPH
    # -----------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        time_history,
        response_history
    )

    plt.title(
        f"Response Time - {scenario.upper()}"
    )

    plt.xlabel("Days")

    plt.ylabel("Response Time")

    plt.grid(True)

    plt.show()

    # -----------------------------------------------------
    # SYNC DELAY GRAPH
    # -----------------------------------------------------

    plt.figure(figsize=(10, 5))

    plt.plot(
        time_history,
        delay_history
    )

    plt.title(
        f"Synchronization Delay - {scenario.upper()}"
    )

    plt.xlabel("Days")

    plt.ylabel("Delay")

    plt.grid(True)

    plt.show()

# =========================================================
# MAIN EXECUTION
# =========================================================

def run_simulation():

    if env.now < SIMULATION_TIME:

        env.step()

        root.after(
            100,
            run_simulation
        )

    else:

        print("Simulation Finished")

        root.destroy()

        generate_graphs()

# =========================================================
# START SIMULATION
# =========================================================

run_simulation()

root.mainloop()