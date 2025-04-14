import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Path to the results file where each line is a startup delay for a run.
    file_path = './Results/startup_log_brick_brick.txt'
    
    # Load the text file into a DataFrame.
    # Assuming the file has 20 lines, each representing the delay for one run.
    df = pd.read_csv(file_path, header=None, names=['Delay'])
    
    # Create a 'Run' column (Run 1 to Run 20)
    df['Run'] = range(1, len(df) + 1)
    
    # Calculate the overall average delay
    overall_average_delay = df['Delay'].mean()
    
    # Plotting the startup delay for each run as a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(df['Run'], df['Delay'], color='skyblue', edgecolor='black', label='Startup Delay')
    
    # Plot the overall average delay as a horizontal dashed line
    plt.axhline(overall_average_delay, color='red', linestyle='--',
                label=f'Overall Average: {overall_average_delay:.2f} ms')
    
    # Add labels and title
    plt.xlabel('Run')
    plt.ylabel('Delay (ms)')
    plt.title('Startup Delay for 20 Runs with Overall Average')
    plt.xticks(range(1, 21))  # Ensure x-axis shows runs 1 through 20
    plt.legend()
    
    # Adjust layout and display the plot
    plt.tight_layout()
    plt.show()

# if __name__ == '__main__':
#     main()

