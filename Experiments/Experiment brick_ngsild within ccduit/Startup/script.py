import os
import sys
import subprocess
import time
import shutil
import psutil

# Set up module paths
modules_path_1 = os.path.join(os.getcwd(), './Federation2')
if os.path.exists(modules_path_1):
    sys.path.append(modules_path_1)

# Import required modules
from Interaction_Handling_Service import create_Interaction, terminate_Interaction, remove_Interaction
import policy_monitoring
import plot

# Ensure necessary directories exist
results_dir = "Results"
os.makedirs(results_dir, exist_ok=True)

# Windows flag to suppress new window creation
CREATE_NO_WINDOW = 0x08000000

def run_occupancy_script():
    """Runs community1_Occupancy.py, prints real-time output, and handles failures."""
    print("Running community1_Occupancy.py...")
    
    occupancy_process = subprocess.Popen(
        ["python", "community1_Occupancy.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="./",
        creationflags=CREATE_NO_WINDOW  # Suppress window
    )
    
    # # Optionally, you can capture and print output here if needed
    # for line in occupancy_process.stdout:
    #     print(f"{line.strip()}")
    
    return occupancy_process

def main():
    print("Running verify.py...")
    time.sleep(2)  # Give it time to initialize

    # Launch verify.py without opening a new window
    verify_process = subprocess.Popen(
        ["python", "verify.py"],
        cwd="../Communities/community2_endpoint",
        creationflags=CREATE_NO_WINDOW
    )
    time.sleep(2)  # Give it time to initialize

    for i in range(20):  # Run the sequence 20 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        print(f"Working directory: {os.getcwd()}")
        
        # # Launch clean.py without opening a new window
        # clean_process = subprocess.Popen(
        #     ["python", "clean.py"],
        #     cwd="./",
        #     creationflags=CREATE_NO_WINDOW
        # )
        
        # Create interaction
        print("Creating interaction ...")
        interaction_id, pid = create_Interaction(
            "Federation2", "Community1", "Community2", "community", "active",
            "Brick", "NGSI-LD", "community1/occupancy","" 
        )
        print(f"Interaction created with ID: {interaction_id} and PID: {pid}")
        # Run the occupancy script
        occupancy_process = run_occupancy_script()
        # Monitor and eventually terminate the interaction process
        interaction_process = psutil.Process(pid)
        # time.sleep(3)  # Allow some processing time
        
        while interaction_process.is_running():
            time.sleep(0.1)  # Check every 0.1 seconds
        occupancy_process.terminate()
        print(f"🟢 Run {i + 1} - Completed.\n")
        time.sleep(1)

    # Move log file if it exists
    if os.path.exists("startup_log_brick_ngsild.txt"):
        new_file_path = os.path.join(results_dir, "startup_log_brick_ngsild.txt")
        shutil.move("startup_log_brick_ngsild.txt", new_file_path)
        print(f"📂 File moved successfully to {new_file_path}.")
    else:
        print("⚠️ startup_log_brick_ngsild.txt not found; skipping move.")

    # Terminate verify.py
    print("🛑 All iterations completed, terminating verify.py...")
    verify_process.terminate()
    verify_process.wait()
    print("✅ verify.py terminated.")

    # Run the plot function
    plot.main()

if __name__ == '__main__':
    main()
