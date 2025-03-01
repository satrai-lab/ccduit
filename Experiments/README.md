# Experiments 
In this section, you will find detailed, step-by-step instructions to reproduce all the experiments. For each experiment, we provide a photograph of the results for verification purposes. This folder contains the complete set of experimental setups. To ensure accurate reproduction, we strongly recommend following the steps outlined in the [main guide](https://github.com/satrai-lab/ccduit/) to configure the federations and their respective contexts, as our experiments assume that the collaborative network between federations is already established.

---
# Table of Contents

2. [Data Interaction Between Communities Experiments](#data-interaction-between-communities-experiments)
   - [Step 1: Set Up Community1 Endpoint](#step-1-set-up-community1-endpoint)
   - [Step 2: Set Up Community2 Endpoint](#step-2-set-up-community2-endpoint)
   - [Step 3: Set Up Community3 Endpoint](#step-3-set-up-community3-endpoint)
   - [Step 4: Set Up Community4 Endpoint](#step-4-set-up-community4-endpoint)

3. [Experiment A: Interaction Latency](#experiment-a-interaction-latency)
   - [Experiment 1: Community 1 and Community 2 within CCDUIT](#experiment-1-community-1-and-community-2-within-ccduit)
   - [Experiment 2: Community 2 and Community 1 within CCDUIT](#experiment-2-community-2-and-community-1-within-ccduit)
   - [Experiment 3: Community 2 and Community 3 within CCDUIT](#experiment-3-community-2-and-community-3-within-ccduit)
   - [Experiment 4: Community 4 and Community 1 within CCDUIT](#experiment-4-community-4-and-community-1-within-ccduit)
   - [Experiment 5: Community 2 and Community 3 without CCDUIT](#experiment-5-community-2-and-community-3-without-ccduit)
   - [Experiment 6: Community 4 and Community 1 without CCDUIT](#experiment-6-community-4-and-community-1-without-ccduit)

5. [Experiment B: Adaptation Experiment](#experiment-b-adaptation-experiment)
   - [Experiment 1: First Adaptation Experiment](#experiment-1-first-adaptation-experiment)
   - [Experiment 2: Second Adaptation Experiment](#experiment-2-second-adaptation-experiment)

6. [Running the Second Adaptation Experiment](#running-the-second-adaptation-experiment)
   - [Experiment Steps](#experiment-steps)
   - [Expected Results](#expected-results)
---

# Set Up Communities

Before running the experiments, ensure that all community containers are properly configured. To do this, navigate to the `Communities` folder and set up each community individually. This step is crucial for a smooth execution of the experiments.
move the `Communities` folder:

   ```bash
   cd ../Communities
   ```

## Set Up Community1 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community1_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
   
## Set Up Community2 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community2_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```

## Set Up Community3 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community3_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```
   
 ## Set Up Community4 Endpoint

1. **Open another terminal** and navigate to the `community1_endpoint` folder:

   ```bash
   cd Coomunities/community4_endpoint
   ```

2. **Start the Docker container:**

   ```bash
   docker-compose up -d
   ```

# Experiment A: Interaction Latency: Startup Latency and Ongoing Interaction Latency.  
## Overview
This experiment evaluates the data exchange process between Community X and Community Y **within CCDUIT** and **without CCDUIT**, specifically measuring the delay that an iteration takes from the moment Community X requests data from Community Y until Community X successfully receives it. The evaluation is conducted across **two phases**:

1. **Startup Delay Measurement**: The delay of the first iteration over 20 runs.
2. **Steady-State Interaction**: Data exchange performance in subsequent iterations, executed over 5 runs, with each run comprising approximately 100 iterations.

## Expected Output
- A box plot illustrating the **startup delay** over 20 runs.
- A box plot visualizing the **ongoing interaction delay** over 5 runs.
- 
### Experiment 1: Interaction Between Community 1 and Community 2 within CCDUIT
This experiment demonstrates the interaction between Community 1 and Community 2. Here’s how the data flow works:
- **Community 2** generates synthetic occupancy data in **JSON format** and transmits it via **HTTP protocol**.
- **Community 1** retrieves this data using **CCDUIT** and receives it in **TTL format** over the **MQTT protocol**.

### Startup Delay Output

![Startup Delay Box Plot](path/to/startup_delay_boxplot.png)

### Ongoing Interaction Output

![Ongoing Interaction Box Plot](path/to/ongoing_interaction_boxplot.png)

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_brick within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_brick within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 2: Interaction Between Community 2 and Community 1 within CCDUIT
This experiment demonstrates the interaction between Community 2 and Community 1. Here’s how the data flow works:
- **Community 1** generates synthetic occupancy data in **TTL format** and transmits it via **MQTT protocol**.
- **Community 2** retrieves this data using **CCDUIT** and receives it in **JSON format** over the **HTTP protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_ngsild within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_ngsild within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```

### Experiment 3: Interaction Between Community 2 and Community 3 within CCDUIT
This experiment demonstrates the interaction between Community 2 and Community 3. Here’s how the data flow works:
- **Community 2** generates synthetic occupancy data in **JSON format** and transmits it via **HTTP protocol**.
- **Community 3** retrieves this data using **CCDUIT** and receives it in **JSON format** over the **HTTP protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```

### Experiment 4: Interaction Between Community 4 and Community 1 within CCDUIT
This experiment demonstrates the interaction between Community 4 and Community 1. Here’s how the data flow works:
- **Community 1** generates synthetic occupancy data in **TTL format** and transmits it via **MQTT protocol**.
- **Community 4** retrieves this data using **CCDUIT** and receives it in **TTL format** over the **MQTT protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick within ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick within ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 5: Interaction Between Community 2 and Community 3 without CCDUIT
This experiment demonstrates the interaction between Community 2 and Community 3. Here’s how the data flow works:
- **Community 2** generates synthetic occupancy data in **JSON format** and transmits it via **HTTP protocol**.
- **Community 3** retrieves this data using **CCDUIT** and receives it in **JSON format** over the **HTTP protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild without ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_ngsild without ccduit/the script
   ```
   2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 6: Interaction Between Community 4 and Community 1 without CCDUIT
This experiment demonstrates the interaction between Community 4 and Community 1. Here’s how the data flow works:
- **Community 1** generates synthetic occupancy data in **TTL format** and transmits it via **MQTT protocol**.
- **Community 4** retrieves this data using **CCDUIT** and receives it in **TTL format** over the **MQTT protocol**.

### How to Run
## I. Startup Delay Measurement

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick without ccduit/Startup
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
## II. Steady-State Interaction

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment brick_brick without ccduit/the script
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
# Expeiment B: Adaptation Experiment  
### Experiment 1: First Adaptation Experiment  

## Overview
This experiment aims to evaluate the response time of CCDUIT to policy changes. Specifically, if an ongoing data interaction is no longer permitted due to an updated policy, CCDUIT should detect the change and promptly terminate the interaction.

## Execution Process
The experiment will be conducted over 100 runs, with each run lasting approximately 9 seconds.

## Expected Output
- A box plot illustrating the **response delay** over 100 runs.
- 
### How to Run

1. **Open a terminal** and navigate to the `the script` folder:

   ```bash
   cd Experiments/Experiment ngsild_brick within ccduit/first_adaptation_experiment
   ```

2. **Run the script**

   ```bash
   python3 script.py
   ```
### Experiment 2: Second Adaptation Experiment  

## Overview
In this experiment, we have a linear collaboration between federations. Specifically, Federation1 will update its policy, and we will measure how fast CCDUIT propagates this policy update to:
**Federation2**
**Federation3**
**Federation4**
The goal is to analyze the propagation delay of policy updates across federations and evaluate CCDUIT’s responsiveness.

## Running the Second Adaptation Experiment

We include instructions and a premade setup to **easily and quickly recreate the second adaptation experiment** described in the paper. More pre-configured experiments will be added over time. It should be fairly simple to navigate to the appropriate location in the code to add timers (e.g., at the start of a data request) for the rest of the experiments.

### Experiment Steps

1. **Stop All Previous Terminals:**

   Ensure all previously running terminals are stopped (including any rogue zombie processes). Also make sure to terminate any containers still running (to start from a clean-slate)
  
  ```bash
   docker stop $(docker ps -q) && docker rm $(docker ps -aq)
   ```


2. **Navigate to the Experiment Folder:**

   ```bash
   cd Experiments/Second Adaptation Experiment
   ```

3. **Run Experiment Configuration:**

   The configuration script sets up federations and their interactions needed automatically for the experiment (so you don't have to do the previous steps again):

   ```bash
   python3 Experiment_config.py
   ```

4. **Clean the Results Folder:**
  Make sure to remove all .txt files present in the Results folder. You can do so manually or by something like :
   ```bash
   cd Results
   rm -f *.txt
   ```

5. **Update the Policy:**

   In the **Federation 1** folder, run the `update_policy.py` script to execute **100 iterations** of policy updates:

   ```bash
   python3 update_policy.py
   ```

6. **Generate Results:**

   After completing the iterations, compile the results into an **Excel file**:

   ```bash
   python3 Generate_excel.py
   ```

9. **Visualize Results:**

   Analyze and visualize the outcomes:

   ```bash
   python3 show_result.py
   ```

### Expected Results

- **`network_delays.xlsx`**: Contains detailed delay data.
- **`response_time_boxplots.png`**: Visual representation of response times.
