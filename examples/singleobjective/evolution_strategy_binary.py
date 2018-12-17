from jmetal.algorithm.singleobjective.evolution_strategy import EvolutionStrategy
from jmetal.operator import BitFlip
from jmetal.problem import OneMax
from jmetal.util.termination_criteria import StoppingByEvaluations

if __name__ == '__main__':
    problem = OneMax(number_of_bits=512)

    algorithm = EvolutionStrategy(
        problem=problem,
        mu=1,
        lambda_=10,
        mutation=BitFlip(probability=1.0 / problem.number_of_bits),
        elitist=True,
        termination_criteria=StoppingByEvaluations(max=25000)
    )

    algorithm.run()
    result = algorithm.get_result()

    print('Algorithm: ' + algorithm.get_name())
    print('Problem: ' + problem.get_name())
    print('Solution: ' + str(result.variables[0]))
    print('Fitness:  ' + str(result.objectives[0]))
    print('Computing time: ' + str(algorithm.total_computing_time))