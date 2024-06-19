# Invasive Weed Optimization (IWO) Project

## Description
This project is an implementation of the Invasive Weed Optimization (IWO) algorithm for solving optimization problems. 
The project includes several scripts to execute the IWO algorithm, run parameter tests, visualize population progress, and clean previous runs.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/BarmadShreef4/iwo-project.git
   ```
2. Navigate to the project directory:
   ```bash
   cd iwo-project
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
### Running the IWO Algorithm
To run the IWO algorithm, use the `my_IWO.py` script:
```bash
python3 my_IWO.py 3.0 0.1 10.0 0 3 5 100 20 1 ./results/
```
The arguments are:

[n] [final_sigma] [init_sigma] [min_seeds] [max_seeds] [init_pop_size] [max_pop_size] [num_generations] [save_visu_data] [output_directory]

Where:

n: the nonlinear modulation index.

final_sigma: final value of sigma (standard deviation).

init_sigma: initial value of sigma (standard deviation).

min_seeds: minimum number of seeds allowed per individual.

max_seeds: maximum number of seeds allowed per individual.

init_pop_size: initial population size.

max_pop_size: maximum population size.

num_generations: total number of generations.

save_visu_data: whether to save data for visualisation or not.

output_directory: directory where to store output files.

### Running Parameter Tests
To test different parameter combinations, use the `parameter_testing.py` script:
#### Sequential execution
```bash
python parameter_testing.py 2 results/test
```
#### Parallel execution
```bash
python parameter_testing.py 1 results/test
```

### Visualizing Population Progress
To visualize the population progress, use the `visualize_pop_progress.py` script:
> **_NOTE:_**  This works only with 2-dimensions.
> 
> Make sure to use the following in the `my_IWO.py` before generating the data:
> 
> fids=list(range(1, 2))
> 
> iids=list(range(1, 2))
> 
> dims=[2]
> 
> reps=1
> 
```bash
python visualize_pop_progress.py population_progress.csv
```

### Cleaning Previous Runs
To clean up previous runs, use the `clean.py` script:
```bash
python clean.py
```

# Example
Here's a basic example demonstrating how to run the IWO algorithm and other scripts:

After cloning the repository and navigating to the iwo_project, run the following command:
```bash
python3 my_IWO.py 3.0 0.1 10.0 0 3 5 100 20 1 ./
```

After finishing the run, you should see the files: `ioh_data_IOW(3.0 0.1 10.0 0 3 5 100 20 1).zip` and `population_progress.csv`.

The `ioh_data_IOW(3.0 0.1 10.0 0 3 5 100 20 1).zip` can be uploaded to [IOHanalyzer](https://iohanalyzer.liacs.nl/) for further studies.

If you set the following in the `my_IWO.py` before generating the data:
> 
> fids=list(range(1, 2))
> 
> iids=list(range(1, 2))
> 
> dims=[2]
> 
> reps=1

Then run the following command to see a visualisation of the population progress:
```bash
python visualize_pop_progress.py population_progress.csv
```

