import pandas as pd
import matplotlib.pyplot as plt
def main():
    # Load the text files into DataFrames
    file_paths = [
        'delay_1.txt',
        'delay_2.txt',
        'delay_3.txt',
        'delay_4.txt',
        'delay_5.txt'
    ]

    # Load and create a DataFrame for all files
    dataframes = [pd.read_csv(file, header=None, names=['Delay']) for file in file_paths]

    # Combine all dataframes into one with an identifier for each run
    for i, df in enumerate(dataframes, start=1):
        df['Run'] = f'Run {i}'

    combined_df = pd.concat(dataframes, ignore_index=True)

    # Calculate the overall average delay
    overall_average_delay = combined_df['Delay'].mean()

    # Create the boxplot
    plt.figure(figsize=(10, 6))
    boxplot = combined_df.boxplot(column='Delay', by='Run', grid=False, showmeans=True, meanline=True, showcaps=True)

    # Highlight the overall average with a horizontal line
    plt.axhline(overall_average_delay, color='red', linestyle='--', label=f'Overall Average: {overall_average_delay:.2f} ms')

    # Add labels and title
    plt.title('MQTT(Brick) to MQTT(Brick) without CCDUIT')
    plt.suptitle('')  # Suppress the default title
    plt.xlabel('Run')
    plt.ylabel('Delay (ms)')
    plt.xticks(rotation=45)
    plt.legend()

    # Display the plot
    plt.tight_layout()
    plt.show()
# main()
