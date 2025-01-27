import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
file_path = 'network_delays.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path)

# Calculate the delay in milliseconds
data['delay_ms'] = (data['terminate'] - data['start']) / 1_000_000  # Convert ns to ms

# Calculate the average delay
average_delay = data['delay_ms'].mean()

# Sort the delay values for CDF calculation
sorted_delays = np.sort(data['delay_ms'])
cdf = np.arange(1, len(sorted_delays) + 1) / len(sorted_delays)

# Plot the CDF
plt.figure(figsize=(10, 6))
plt.plot(sorted_delays, cdf, marker='o', linestyle='-', color='b')
plt.title('CDF of Response Time to Policy Updates Requiring Data Termination')
plt.xlabel('Response Time (ms)')
plt.ylabel('Cumulative Probability')
plt.grid(True)

# Plot the average delay as a vertical line
plt.axvline(average_delay, color='r', linestyle='--', label=f'Average Response Time: {average_delay:.2f} ms')
plt.legend()

# Show the plot and display the average delay
plt.show()

print(f"Average Delay: {average_delay:.2f} ms")
