import ioh
import sys
import numpy as np


#################################### IWO ####################################
class IWO:
    """Invasive Weed Optimization algorithm

    Args:
        min_seeds: minimum number of seeds allowed per individual
        max_seeds: maximum number of seeds allowed per individual
        n: the nonlinear modulation index
        final_sigma: final value of sigma (standard deviation)
        init_sigma: initial value of sigma (standard deviation)
        curr_sigma: current value of sigma
        init_pop_size: initial population size
        max_pop_size: maximum population size
        num_generations: total number of generations
    """

    def __init__(
        self,
        min_seeds: int,
        max_seeds: int,
        n: float,
        final_sigma: float,
        init_sigma: float,
        init_pop_size: int,
        max_pop_size: int,
        num_generations: int,
        save_visu_data: int = 0,
    ):
        self.min_seeds: int = min_seeds
        self.max_seeds: int = max_seeds
        self.n: float = n
        self.final_sigma: float = final_sigma
        self.init_sigma: float = init_sigma
        self.curr_sigma: float = 0.0
        self.init_pop_size: int = init_pop_size
        self.max_pop_size: int = max_pop_size
        self.num_generations: int = num_generations
        self.save_visu_data: int = save_visu_data
        self.population = []
        self.fitness = []

    def _save_visu_data(self, generation):
        """Save the positions and fitness of the population members to a file.
           For visualization purposes only.

        Args:
            generation (int): The actual generation number.
        """
        for agent_index in range(len(self.population)):
            # Append the data for each member of the population along
            # with the generation number
            output_file.write(
                ",".join(
                    map(
                        str,
                        [generation]
                        + np.append(
                            self.population[agent_index],
                            self.fitness[agent_index],
                        ).tolist(),
                    )
                )
                + "\n"
            )

    def _calculate_sigma(self, curr_generation: int) -> None:
        """Calculates the Spatial Dispersal coefficient (eq. 1).

        Args:
            curr_generation: Current generation number.
        """
        coef = (
            (self.num_generations - curr_generation) / (self.num_generations)
        ) ** self.n

        self.curr_sigma = (
            coef * (self.init_sigma - self.final_sigma) + self.final_sigma
        )

    def _initialize_population(self, problem):
        self.population = np.random.uniform(
            low=problem.bounds.lb,
            high=problem.bounds.ub,
            size=(self.init_pop_size, problem.meta_data.n_variables),
        )
        # Evaluate fitness for each agent (weed)
        self.fitness = problem(self.population)

    def _reproduction_phase(self):
        # Sort agents based on fitness
        sorted_indices = np.argsort(self.fitness)
        self.population = self.population[sorted_indices]
        self.fitness.sort()

        # Calculate the number of seeds for each agent (weed) based
        # on its rank (its fitness)
        n_seeds = np.round(
            np.interp(
                self.fitness,
                [self.fitness[0], self.fitness[-1]],
                [self.max_seeds, self.min_seeds],
            )
        ).astype(int)
        return n_seeds

    def _spatial_dispersal_phase(self, problem, generation, n_seeds):
        # Calculat the sigma (standard deviation) for spatial randomness
        # for the current iteration (generation)
        self._calculate_sigma(generation)

        # Iterate through each agent in the population
        for agent_index in range(len(self.population)):
            # Generate positions for the seeds based on normal distribution
            # with the standard deviation curr_sigma
            seeds = np.random.normal(
                self.population[agent_index],
                self.curr_sigma,
                size=(n_seeds[agent_index], len(self.population[agent_index])),
            )

            if seeds.size != 0:
                # Evaluate fitness for each seed
                seeds_fitness = problem(seeds)

                # Update population
                self.fitness = np.concatenate((self.fitness, seeds_fitness))
                self.population = np.concatenate((self.population, seeds))

    def _competitive_exclusion_phase(self):
        # Sort agents based on fitness
        sorted_indices = np.argsort(self.fitness)
        self.population = self.population[sorted_indices]
        self.fitness.sort()

        # Eliminate agents with lower fitness to reach the maximum
        # allowable population size
        if len(self.population) > self.max_pop_size:
            self.population = self.population[: self.max_pop_size]
            self.fitness = self.fitness[: self.max_pop_size]

    def __call__(self, problem: ioh.problem.RealSingleObjective) -> None:
        "Optimize the problem with the Invasive Weed Optimization algorithm"

        ################## Initialization phase ##################
        self._initialize_population(problem)

        # Iterating through each generation
        for generation in range(self.num_generations):
            ####################### Reproduction phase #######################
            n_seeds = self._reproduction_phase()

            if self.save_visu_data:
                # Save population progress data across generations
                # (for visualization)
                self._save_visu_data(generation)

            #################### Spatial dispersal phase ####################
            self._spatial_dispersal_phase(problem, generation, n_seeds)

            ################## Competitive exclusion phase ##################
            self._competitive_exclusion_phase()


if __name__ == "__main__":
    # Retrieve command-line arguments
    args = sys.argv[1:]
    usage_info = [
        "\nUsage: python3 my_IWO.py [n] [final_sigma] [init_sigma]",
        "[min_seeds] [max_seeds] [init_pop_size] [max_pop_size]",
        "[num_generations] [save_visu_data] [output_directory]\n\n",
        "                 n: the nonlinear modulation index\n",
        "       final_sigma: final value of sigma (standard deviation)\n",
        "        init_sigma: initial value of sigma (standard deviation)\n",
        "         min_seeds: minimum number of seeds allowed per individual\n",
        "         max_seeds: maximum number of seeds allowed per individual\n",
        "     init_pop_size: initial population size\n",
        "      max_pop_size: maximum population size\n",
        "   num_generations: total number of generations\n",
        "    save_visu_data: whether to save data for visualisation or not\n",
        "  output_directory: directory where to store output files."
        "\n\nEx: python3 my_IWO.py 3.0 0.1 10.0 1 5 5 40 50 1 ./results/\n",
    ]

    # Check if the correct number of arguments is provided
    if len(args) != 10:
        print(*usage_info)
        sys.exit(1)

    # Convert arguments to appropriate types
    n, final_sigma, init_sigma = map(float, args[:3])
    (
        min_seeds,
        max_seeds,
        init_pop_size,
        max_pop_size,
        num_generations,
        save_visu_data,
    ) = map(int, args[3:-1])
    output_directory = args[-1]

    # Create a folder name for this run based on used parameters
    ioh_data_folder_name = (
        "ioh_data_IOW("
        + str(n)
        + " "
        + str(final_sigma)
        + " "
        + str(init_sigma)
        + " "
        + str(min_seeds)
        + " "
        + str(max_seeds)
        + " "
        + str(init_pop_size)
        + " "
        + str(max_pop_size)
        + " "
        + str(num_generations)
        + " "
        + str(save_visu_data)
        + ")"
    )

    if save_visu_data == 1:
        # Open a file for writing population progress data
        # across generations
        output_file = open("population_progress.csv", "w")

    experiment = ioh.Experiment(
        algorithm=IWO(
            min_seeds,
            max_seeds,
            n,
            final_sigma,
            init_sigma,
            init_pop_size,
            max_pop_size,
            num_generations,
            save_visu_data,
        ),  # An algorithm instance
        fids=list(range(1, 25)),  # the id's of the problems we want to test
        iids=list(range(1, 6)),  # the instances
        dims=[
            2,
            5,
            20,
            40,
        ],  # the dimensions (number of variables for each agent)
        reps=5,  # the number of runs for each combination (fids, iids, dims),
        problem_class=ioh.ProblemClass.BBOB,
        algorithm_name=ioh_data_folder_name,
        remove_data=True,  # delete data in the folder (Not the .zip file)
        zip_output=True,
        algorithm_info="",
        store_positions=True,
        merge_output=True,
        folder_name=ioh_data_folder_name,
        output_directory=output_directory,
    )

    print("started:", ioh_data_folder_name)
    experiment()

    if save_visu_data == 1:
        # Close the file
        output_file.close()
