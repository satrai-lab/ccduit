# import os
# import sys
# import subprocess
# import time
# import shutil
# import psutil
# import plot


# def run_occupancy_script():
#     """Runs community1_Occupancy.py, prints real-time output, and handles failures."""
#     print("Running community1_Occupancy.py...")
    
#     occupancy_process = subprocess.Popen(
#         ["python", "community1_Occupancy.py"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         shell=True,
#         cwd="./"
#     )
    
#     # Capture and print output in real-time
#     for line in occupancy_process.stdout:
#         print(f"{line.strip()}")
    
#     return occupancy_process

# def main():
#     print("Running verify.py...")
#     # Launch verify.py without opening a new window
#     verify_process = subprocess.Popen(
#         ["python", "verify.py"],
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#         shell=True,
#         cwd="./"
#     )
#     occupancy_process = run_occupancy_script()
#     for i in range(20):  # Run the sequence 20 times
#         print(f"\n🟢 Run {i + 1} - Starting...")
        
#         bridge_process = subprocess.Popen(
#             ["python", "bridge.py"],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             cwd="./"
#         )
#         print(f"🟢 Run {i + 1} - Completed.")
        
#     # Terminate other processes
#     occupancy_process.terminate()
#     verify_process.terminate()
    
#     # Check if processes are still alive and kill them if necessary
#     if occupancy_process.poll() is None:
#         occupancy_process.kill()
#     if verify_process.poll() is None:
#         verify_process.kill()
        
        
    
#     # Run the plot function
#     plot.main()

# if __name__ == '__main__':
#     main()

import subprocess
import time
import plot
import os
def run_occupancy_script():
    """Runs community1_Occupancy.py."""
    print("Running community1_Occupancy.py...")
    occupancy_process = subprocess.Popen(
        ["python", "community1_Occupancy.py"],
        cwd="./"
    )
    return occupancy_process

def run_verify_script():
    """Runs verify.py."""
    print("Running verify.py...")
    # For Windows, if you want to open it in a new command prompt, use:
    verify_process = subprocess.Popen('start cmd /k python verify.py', shell=True, cwd="./")
    # verify_process = subprocess.Popen(
    #     ["python", "verify.py"],
    #     shell=True,
    #     cwd="./"
    # )
    return verify_process

def run_bridge_script():
    """Runs bridge.py."""
    print("Running bridge.py...")
    bridge_process = subprocess.Popen('start cmd /k python bridge.py', shell=True, cwd="./")
    # bridge_process = subprocess.Popen(
    #     ["python", "bridge.py"],
    #     cwd="./"
    # )
    return bridge_process

def main():
    verify_process = run_verify_script()
    bridge_process = run_bridge_script()
    for i in range(5):  # Run the sequence 20 times
        print(f"\n🟢 Run {i + 1} - Starting...")
        
        occupancy_process = run_occupancy_script()
        print(f"🟢 Run {i + 1} - Completed.")
        occupancy_process.wait()
        if os.path.exists("delays.txt"):
            os.rename("delays.txt", f"delay_{i+1}.txt")
        
    # Check and terminate each process if it's still running
    for proc, name in [
        (verify_process, "verify.py"), 
        (occupancy_process, "community1_Occupancy.py"), 
        (bridge_process, "bridge.py")
    ]:
        if proc.poll() is None:  # Process is still running
            print(f"Terminating {name}")
            proc.terminate()
            proc.wait()  # Ensure the process has terminated

    # Run the plot function after all iterations
    plot.main()

if __name__ == '__main__':
    main()
