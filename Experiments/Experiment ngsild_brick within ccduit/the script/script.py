import os
import sys
import subprocess
import time
import shutil
import psutil

# Set up module paths
modules_path_1 = os.path.join(os.getcwd(), '../Federation1')

if os.path.exists(modules_path_1):
    sys.path.append(modules_path_1)

# Import required modules
from Interaction_Handling_Service import create_Interaction, terminate_Interaction, remove_Interaction
import policy_monitoring
import plot

# Ensure necessary directories exist
results_dir = "Results"
os.makedirs(results_dir, exist_ok=True)


def run_occupancy_script():
    """Runs community2_Occupancy.py, prints real-time output, and handles failures."""
    print("Running community2_Occupancy.py...")
    
    occupancy_process = subprocess.Popen(
        ["python", "community2_Occupancy.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="../Communities/community2_endpoint"
    )

    # Check if process started correctly
    time.sleep(1)
    if occupancy_process.poll() is not None:
        print("⚠️ Error: community2_Occupancy.py failed to start!")
        stdout, stderr = occupancy_process.communicate()
        print(f"STDOUT:\n{stdout}")
        print(f"STDERR:\n{stderr}")
        return None

    # Print real-time output
    for line in occupancy_process.stdout:
        print(f"community2_Occupancy.py output: {line.strip()}")
    
    for err in occupancy_process.stderr:
        print(f"community2_Occupancy.py error: {err.strip()}")

    # Wait for process to complete, but with a timeout
    try:
        occupancy_process.wait(timeout=60)  # Adjust timeout as needed
    except subprocess.TimeoutExpired:
        print("⏳ Timeout: community2_Occupancy.py is taking too long. Terminating...")
        occupancy_process.terminate()
        occupancy_process.wait()
    
    return occupancy_process


def main():
    print("Running verify.py...")
    verify_process=subprocess.Popen(
        ['cmd', '/c', 'start', 'cmd', '/k', 'python verify.py'],
        cwd="../Communities/community1_endpoint",
        shell=True
    )

    time.sleep(3)  # Give it time to initialize

    for i in range(5):  # Run the sequence 5 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        print(f"Working directory: {os.getcwd()}")

        # Create interaction
        print("Creating interaction ...")
        interaction_id, pid = create_Interaction(
            "Federation1", "Community2", "Community1", "community", "active",
            "NGSI-LD", "Brick", "/?type=OccupancyReading", "community2/occupancy"
        )
        print(f"Interaction created with ID: {interaction_id} and PID: {pid}")

        interaction_process = psutil.Process(pid)
        print(interaction_process)
        time.sleep(2)
        # Run occupancy script
        occupancy_process = run_occupancy_script()
        if not occupancy_process:
            print("❌ Skipping this run due to occupancy script failure.")
            continue

        # Check if occupancy process is still running
        if occupancy_process.poll() is None:
            print("✅ community1_Occupancy.py completed successfully.")
        else:
            print("community1_Occupancy.py terminated.")

        # Stop interaction
        if interaction_process.is_running():
            print(f"🔴 Terminating interaction process (PID: {pid})...")
            interaction_process.terminate()
            interaction_process.wait()
            print("✅ Interaction process terminated.")

        # Move log file
        if os.path.exists("time_log.txt"):
            new_file_path = os.path.join(results_dir, f"time_log_{i+1}.txt")
            shutil.move("time_log.txt", new_file_path)
            print(f"📂 File moved successfully to {new_file_path}.")
        else:
            print("⚠️ time_log.txt not found; skipping move.")

        print(f"🟢 Run {i + 1} - Completed.\n")
        time.sleep(1)

    # Terminate verify.py
    print("🛑 All iterations completed, terminating verify.py...")
    verify_process.terminate()
    verify_process.wait()
    print("✅ verify.py terminated.")

    # Run plot function
    plot.main()


if __name__ == '__main__':
    main()
