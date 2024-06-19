import multiprocessing
import subprocess
import sys


def run_combination(parameters):
    """Run a parameter combination."""
    command = ["python3", "my_IWO.py"] + [str(param) for param in parameters]
    subprocess.run(command)


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ["1", "2"]:
        print(
            "\nUsage: python3 parameter_testing.py [1:parallel|2:sequential]",
            "[directory_path]",
            "\n\nEx: python3 parameter_testing.py 2 results/test\n",
        )
        sys.exit(1)

    # Predefined parameter combinations
    parameter_combinations = [
        (3.0, 0.001, 3.0, 0, 5, 10, 15, 100, 0, sys.argv[2]),
        (8.0, 0.00001, 5.0, 0, 5, 10, 30, 100, 0, sys.argv[2]),
        (2.0, 0.01, 1.0, 0, 1, 10, 10, 100, 0, sys.argv[2]),
        #
        (3.0, 0.001, 3.0, 0, 5, 10, 15, 500, 0, sys.argv[2]),
        (8.0, 0.00001, 5.0, 0, 5, 10, 30, 500, 0, sys.argv[2]),
        (2.0, 0.01, 1.0, 0, 1, 10, 10, 500, 0, sys.argv[2]),
        #
        (3.0, 0.001, 3.0, 0, 5, 10, 15, 1000, 0, sys.argv[2]),
        (8.0, 0.00001, 5.0, 0, 5, 10, 30, 1000, 0, sys.argv[2]),
        (2.0, 0.01, 1.0, 0, 1, 10, 10, 1000, 0, sys.argv[2]),
        #
        (3.0, 0.001, 3.0, 0, 5, 10, 15, 5000, 0, sys.argv[2]),
        (8.0, 0.00001, 5.0, 0, 5, 10, 30, 5000, 0, sys.argv[2]),
        (2.0, 0.01, 1.0, 0, 1, 10, 10, 5000, 0, sys.argv[2]),
        #
        (3.0, 0.001, 3.0, 0, 5, 10, 15, 10000, 0, sys.argv[2]),
        (8.0, 0.00001, 5.0, 0, 5, 10, 30, 10000, 0, sys.argv[2]),
        (2.0, 0.01, 1.0, 0, 1, 10, 10, 10000, 0, sys.argv[2]),
    ]

    print("Number of parameter combinations:", len(parameter_combinations))
    print("Performing tests...")

    mode = sys.argv[1]

    if mode == "1":
        # Run parameter combinations in parallel
        with multiprocessing.Pool() as pool:
            pool.map(run_combination, parameter_combinations)
    elif mode == "2":
        # Run parameter combinations sequentially
        for combination in parameter_combinations:
            run_combination(combination)
    else:
        print("Invalid mode. Choose 1 for parallel or 2 for sequential.")

    print("Testing completed.")
