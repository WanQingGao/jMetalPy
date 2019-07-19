from enum import Enum
from typing import TypeVar, List

from jmetal.util.density_estimator import DensityEstimator

from jmetal.util.ranking import Ranking

S = TypeVar('S')


class RemovalPolicyType(Enum):
    SEQUENTIAL = 1
    ONE_SHOT = 2


class RankingAndDensityEstimatorReplacement():

    def __init__(self, ranking: Ranking, density_estimator: DensityEstimator,
                 removal_policy=RemovalPolicyType.ONE_SHOT):
        self.ranking = ranking
        self.density_estimator = density_estimator
        self.removal_policy = removal_policy

    def replace(self, solution_list: List[S], offspring_list: List[S]) -> List[S]:
        join_population = solution_list + offspring_list

        """
        for solution in solution_list:
            print(solution.objectives)
        print("-----------")
        for solution in offspring_list:
            print(solution.objectives)
        """

        self.ranking.compute_ranking(join_population)
        # if self.removal_policy is RemovalPolicyType.SEQUENTIAL:
        result_list = self.sequential_truncation(0, len(solution_list))

        return result_list

    def sequential_truncation(self, ranking_id: int, size_of_the_result_list: int) -> List[S]:
        current_rank_solutions = self.ranking.get_subfront(ranking_id)
        self.density_estimator.compute_density_estimator(current_rank_solutions)

        result_list: List[S] = []

        if len(current_rank_solutions) < size_of_the_result_list:
            result_list.extend(self.ranking.get_subfront(ranking_id))
            result_list.extend(self.sequential_truncation(ranking_id + 1, size_of_the_result_list - len(
                current_rank_solutions)))
        else:
            for solution in current_rank_solutions:
                result_list.append(solution)

            while len(result_list) > size_of_the_result_list:
                self.density_estimator.sort(result_list)

                del result_list[-1]
                self.density_estimator.compute_density_estimator(result_list)

        return result_list