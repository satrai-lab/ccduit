import os
import subprocess
import time
import shutil
import plot



# Windows flag to suppress new window creation
# CREATE_NO_WINDOW = 0x08000000

# Define file paths
startup_file = "startup_log_ngsild_ngsild.txt"
end_time_file = "end_delays.txt"


def run_occupancy_script():
    """Runs community2_Occupancy.py and ensures process completion."""
    print("Running community2_Occupancy.py...")
    
    occupancy_process = subprocess.Popen(
        ["python", "community2_Occupancy.py"],
        # stdout=subprocess.PIPE,
        # stderr=subprocess.PIPE,
        text=True,
        cwd="./" #,
        # creationflags=CREATE_NO_WINDOW
    )

   
    return occupancy_process

def main():
    verify_process = subprocess.Popen(
        ["python", "verify.py"],
        text=True,
        cwd="./" #,
        # creationflags=CREATE_NO_WINDOW
    )
    # time.sleep(1)  # Give it time to initialize    

    for i in range(5):  # Run the sequence 5 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        occupancy_process = subprocess.Popen(
        ["python", "community2_Occupancy.py"],
        text=True,
        cwd="./" #,
        # creationflags=CREATE_NO_WINDOW
        )
        # time.sleep(1)  # Give it time to initialize    
        print(f"occupancy_process: {occupancy_process}")
        occupancy_process.wait()

        # Move log file
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

    # Run the plot function
    plot.main()

if __name__ == '__main__':
    main()
