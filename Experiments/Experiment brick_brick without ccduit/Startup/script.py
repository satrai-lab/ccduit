import os
import sys
import subprocess
import time
import shutil
import psutil
import plot
# Set up module paths

# Windows flag to suppress new window creation

def run_occupancy_script():
    """Runs community1_Occupancy.py, prints real-time output, and handles failures."""
    print("Running community1_Occupancy.py...")
    
    occupancy_process = subprocess.Popen(
        ["python", "community1_Occupancy.py"],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,
        cwd="./"
    )
    
    # # Optionally, you can capture and print output here if needed
    # for line in occupancy_process.stdout:
    #     print(f"{line.strip()}")
    
    return occupancy_process

def main():

    for i in range(20):  # Run the sequence 20 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        # print(f"Working directory: {os.getcwd()}")
        
        # # Launch clean.py without opening a new window
        # clean_process = subprocess.Popen(
        #     ["python", "clean.py"],
        #     cwd="./"
        # )
        
        print("Running verify.py...")
        # Launch verify.py without opening a new window
        verify_process = subprocess.Popen(
            ["python", "verify.py"],
            cwd="./"
        )
        
        occupancy_process = run_occupancy_script()
        verify_process.wait()  # Wait for verify.py to complete
        occupancy_process.terminate()  # Terminate community1_Occupancy.py
        
    # Run the plot function
    plot.main()

if __name__ == '__main__':
    main()
