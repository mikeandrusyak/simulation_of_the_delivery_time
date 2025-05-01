import numpy as np
import matplotlib.pyplot as plt

# Simulation Parameters
N_SIMULATIONS = 10000
BASE_DELIVERY_TIME = 3  # typical base delivery time in days

# External delays (weather, strikes)
WEATHER_PROB = 0.1  # 10% parcels affected by weather delays
WEATHER_DELAY_DAYS = np.random.randint(1, 3, N_SIMULATIONS)  # 1-2 days delay

STRIKE_PROB = 0.05  # 5% chance of strike delay
STRIKE_DELAY_DAYS = np.random.randint(2, 4, N_SIMULATIONS)  # 2-3 days delay

# Queuing parameters at sorting hub (M/M/1 queue)
ARRIVAL_RATE = 500  # parcels/hour arriving at the hub
SERVICE_RATE = 550  # parcels/hour hub capacity

# Convert rates into daily numbers (assuming 8 hours of operation)
ARRIVAL_RATE_DAILY = ARRIVAL_RATE * 8
SERVICE_RATE_DAILY = SERVICE_RATE * 8

# Queuing Simulation Function
def simulate_hub_queue(arrival_rate, service_rate, num_parcels):
    # Generate random arrival and service times
    inter_arrival_times = np.random.exponential(1/arrival_rate, num_parcels)
    arrival_times = np.cumsum(inter_arrival_times)

    service_times = np.random.exponential(1/service_rate, num_parcels)

    start_service_times = np.zeros(num_parcels)
    departure_times = np.zeros(num_parcels)
    waiting_times = np.zeros(num_parcels)

    for i in range(num_parcels):
        if i == 0:
            start_service_times[i] = arrival_times[i]
        else:
            start_service_times[i] = max(arrival_times[i], departure_times[i-1])
        waiting_times[i] = start_service_times[i] - arrival_times[i]
        departure_times[i] = start_service_times[i] + service_times[i]

    # Convert waiting times from hours to days (assuming 8-hour day)
    waiting_days = waiting_times / 8
    return waiting_days

# Monte Carlo Simulation
def monte_carlo_delivery_simulation(n_simulations):
    # Queuing delay at sorting hub
    queuing_delays = simulate_hub_queue(ARRIVAL_RATE, SERVICE_RATE, n_simulations)

    # External delays
    weather_occurs = np.random.rand(n_simulations) < WEATHER_PROB
    strike_occurs = np.random.rand(n_simulations) < STRIKE_PROB

    total_external_delay = (weather_occurs * WEATHER_DELAY_DAYS +
                            strike_occurs * STRIKE_DELAY_DAYS)

    # Total delivery time = base + queuing delays + external delays
    total_delivery_times = BASE_DELIVERY_TIME + queuing_delays + total_external_delay

    return total_delivery_times, queuing_delays, total_external_delay

# Run simulation
total_times, queuing_times, external_delays = monte_carlo_delivery_simulation(N_SIMULATIONS)

# Statistical summary
print(f"Average total delivery time: {np.mean(total_times):.2f} days")
print(f"Median total delivery time: {np.median(total_times):.2f} days")
print(f"Probability delivery > 3 days: {np.mean(total_times > 3):.2%}")
print(f"Probability delivery > 5 days: {np.mean(total_times > 5):.2%}")

# Visualization
plt.figure(figsize=(12,6))
plt.hist(total_times, bins=30, color='lightblue', edgecolor='black', alpha=0.8)
plt.title('Distribution of Simulated Parcel Delivery Times')
plt.xlabel('Total Delivery Time (days)')
plt.ylabel('Number of Parcels')
plt.axvline(3, color='orange', linestyle='dashed', linewidth=1, label='3 Days')
plt.axvline(5, color='red', linestyle='dashed', linewidth=1, label='5 Days')
plt.legend()
plt.grid(alpha=0.3)
plt.show()
