import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the Excel file
file_path = 'network_delays.xlsx'  # Replace with the actual file path
data = pd.read_excel(file_path)

# Extract the relevant columns for delays
delays = data[['Delay F1 to F2 (ms)', 'Delay F2 to F3 (ms)', 'Delay F1 to F3 (ms)']]

# Create boxplots for the delays
plt.figure(figsize=(10, 6))
delays.boxplot(column=['Delay F1 to F2 (ms)', 'Delay F2 to F3 (ms)', 'Delay F1 to F3 (ms)'], grid=False)
plt.title('Delays for Policy Adaptation Across Federations')
plt.ylabel('Delay (ms)')
plt.xticks([1, 2, 3], ['Federation 1 to Federation 2', 'Federation 2 to Federation 3', 'Federation 1 to Federation 3'])

plt.savefig('response_time_boxplots.png')  # Saves the plot to a PNG file
# Show the plot
plt.show()
