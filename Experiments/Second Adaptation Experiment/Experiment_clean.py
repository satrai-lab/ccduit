import subprocess
import os

# List of federation folders
federations = ["Federation1", "Federation2", "Federation3"]

def stop_api_services():
    """Stops all python3 app.py processes and clears zombie processes by killing their parent processes."""
    try:
        print("Stopping all 'python3 app.py' processes...")

        # Kill processes running 'python3 app.py'
        subprocess.run("pkill -f 'python3 app.py'", shell=True, check=False)

        # Identify and kill parent processes of zombie processes
        zombie_processes = subprocess.check_output("ps -l | grep defunct", shell=True, text=True).strip().splitlines()
        for line in zombie_processes:
            parts = line.split()
            if len(parts) >= 4:
                ppid = parts[3]
                print(f"Killing parent process with PID: {ppid}")
                subprocess.run(f"kill -9 {ppid}", shell=True, check=False)

        print("All 'python3 app.py' processes and their zombies have been stopped.")
    except subprocess.CalledProcessError:
        print("No 'python3 app.py' processes found or failed to stop.")

def stop_broker_services():
    """Runs docker-compose down in each federation's /brokers subfolder."""
    for federation in federations:
        brokers_path = os.path.join(os.path.abspath(federation), "brokers")
        try:
            print(f"Stopping Docker services in {brokers_path}...")
            subprocess.run("docker-compose down", shell=True, cwd=brokers_path, check=True)
            print(f"Docker services in {brokers_path} have been stopped.")
        except subprocess.CalledProcessError:
            print(f"Failed to stop Docker services in {brokers_path} or no containers were running.")

if __name__ == "__main__":
    # Stop the app.py processes
    stop_api_services()

    # Stop the docker-compose services
    stop_broker_services()

    print("All services have been stopped.")
