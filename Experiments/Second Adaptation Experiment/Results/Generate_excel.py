import pandas as pd

# File paths
start_times_file = 'start_times_Fed1.txt'
received_time_file = 'End_times_Fed2.txt'
received_f2_file = 'End_times_Fed3.txt'

# Read the data from the text files
start_times = []
received_times_fed2 = []
received_f3 = []

# Function to read data from a file
def read_data(file_path):
    with open(file_path, 'r') as file:
        return [int(line.strip()) for line in file.readlines()]

# Read each file
start_times = read_data(start_times_file)
received_times_fed2 = read_data(received_time_file)
received_f3 = read_data(received_f2_file)

# Calculate delays
def calculate_delays(start, end):
    return [(e - s) / 1_000_000 for s, e in zip(start, end)]  # Convert nanoseconds to milliseconds

delay_f1_to_f2 = calculate_delays(start_times, received_times_fed2)
delay_f2_to_f3 = calculate_delays(received_times_fed2, received_f3)
delay_f1_to_f3 = calculate_delays(start_times, received_f3)

# Create a DataFrame
data = {
    'Start Time Fed1': start_times,
    'Received Time Fed2': received_times_fed2,
    'Received Time F3': received_f3,
    'Delay F1 to F2 (ms)': delay_f1_to_f2,
    'Delay F2 to F3 (ms)': delay_f2_to_f3,
    'Delay F1 to F3 (ms)': delay_f1_to_f3
}
df = pd.DataFrame(data)

# Save to an Excel file
output_file = 'network_delays.xlsx'
df.to_excel(output_file, index=False)

print(f"Excel file created at {output_file}")
