import os
import sys
import subprocess
import time
import shutil
import psutil
import plot


# Ensure necessary directories exist
results_dir = "Results"
os.makedirs(results_dir, exist_ok=True)

# Windows flag to suppress new window creation



# Define file paths
startup_file = "startup_log_ngsild_ngsild.txt"
end_time_file = "end_time_logs.txt"
delay_file = "delay.txt"
results_dir = "results"

# Ensure results directory exists
os.makedirs(results_dir, exist_ok=True)

# Function to extract timestamp from a file
def extract_timestamp(file_path):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
            if lines:
                return float(lines[-1].strip())  # Assuming last line contains the timestamp
    except Exception as e:
        print(f"⚠️ Error reading {file_path}: {e}")
    return None





def run_occupancy_script():
    """Runs community2_Occupancy.py, prints real-time output, and handles failures."""
    print("Running community2_Occupancy.py...")
    
    occupancy_process = subprocess.Popen(
        ["python", "community2_Occupancy.py"],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,
        cwd="./"
    )
    
    # Optionally, you can capture and print output here if needed
    # for line in occupancy_process.stdout:
    #     print(f"community2_Occupancy.py output: {line.strip()}")
    
    return occupancy_process

def main():


    for i in range(20):  # Run the sequence 20 times
        print(f"\n🟢 Run {i + 1} - Starting...")

        
        occupancy_process = run_occupancy_script()
        time.sleep(1)  # Give it time to initialize
        
        # Launch verify.py without opening a new window
        verify_process = subprocess.Popen(
            ["python", "verify.py"],
            text=True,
            cwd="./"
        )
        time.sleep(1)  # Give it time to initialize
                
    
    # Ensure both files exist
    # if not os.path.exists(startup_file) or not os.path.exists(end_time_file):
    #     print("⚠️ One or both files are missing. Exiting...")
    #     exit()

    # # Open both files and compute delays
    # with open(startup_file, "r") as start_f, open(end_time_file, "r") as end_f, open(delay_file, "w") as delay_f:
    #     startup_lines = start_f.readlines()
    #     end_time_lines = end_f.readlines()

    #     # Ensure both files have the same number of lines
    #     if len(startup_lines) != len(end_time_lines):
    #         print("⚠️ Warning: The two files have different numbers of lines. Processing only matching pairs.")

    #     min_lines = min(len(startup_lines), len(end_time_lines))

    #     for i in range(min_lines):
    #         try:
    #             startup_time = float(startup_lines[i].strip())  # Convert to float
    #             end_time = float(end_time_lines[i].strip())  # Convert to float
    #             delay_ms = (end_time - startup_time)/1_000_000  # Convert to milliseconds

    #             # Write to delay file
    #             delay_f.write(f"{delay_ms:.3f}\n")
    #         except ValueError:
    #             print(f"⚠️ Skipping line {i+1} due to invalid data.")

    # print(f"✅ Delay calculations saved to {delay_file}.")

    # Terminate verify.py
    print("🛑 All iterations completed, terminating verify.py...")

    # Run the plot function
    plot.main()

if __name__ == '__main__':
    main()
