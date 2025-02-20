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
    print("Running verify.py...")
    # Launch verify.py without opening a new window
    verify_process = subprocess.Popen(
        ["python", "verify.py"],
        cwd="./"
    )
    
    for i in range(5):  # Run the sequence 20 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        # print(f"Working directory: {os.getcwd()}")
        
        # # Launch clean.py without opening a new window
        # clean_process = subprocess.Popen(
        #     ["python", "clean.py"],
        #     cwd="./"
        # )
        
        
        occupancy_process = run_occupancy_script()
        occupancy_process.wait()  # Wait for verify.py to complete
        
        if os.path.exists("delay.txt"):
            new_file_path = os.path.join(f"delay_{i+1}.txt")
            shutil.move("delay.txt", new_file_path)
            print(f"📂 File moved successfully to {new_file_path}.")
        else:
            print("⚠️ delay.txt not found; skipping move.")

        print(f"🟢 Run {i + 1} - Completed.\n")
        time.sleep(1)

    # Terminate verify.py
    print("🛑 All iterations completed, terminating verify.py...")
    verify_process.terminate()
    verify_process.wait()
    print("✅ verify.py terminated.")

    # Run the plot function
    plot.main()

if __name__ == '__main__':
    main()
