import re
from colorama import Fore, Style, Back
from typing import Optional
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)

SUBSTITUTIONS = [
    (".$", "$"),
    ("\\$", ""),
    (r"\ ", ""),
    (" ", ""),
    ("mbox", "text"),
    (",\\text{and}", ","),
    ("\\text{and}", ","),
    ("\\text{m}", "\\text{}"),
]
REMOVED_EXPRESSIONS = [
    "square",
    "ways",
    "integers",
    "dollars",
    "mph",
    "inches",
    "hours",
    "km",
    "units",
    "\\ldots",
    "sue",
    "points",
    "feet",
    "minutes",
    "digits",
    "cents",
    "degrees",
    "cm",
    "gm",
    "pounds",
    "meters",
    "meals",
    "edges",
    "students",
    "childrentickets",
    "multiples",
    "\\text{s}",
    "\\text{.}",
    "\\text{\ns}",
    "\\text{}^2",
    "\\text{}^3",
    "\\text{\n}",
    "\\text{}",
    r"\mathrm{th}",
    r"^\circ",
    r"^{\circ}",
    r"\;",
    r",\!",
    "{,}",
    '"',
    "\\dots",
]


def strict(pred_matrix, sol_matrix):
    """All rows should match exactly."""
    match = 0
    for a_sol in sol_matrix:
        for p_sol in pred_matrix:
            if len(a_sol) != len(p_sol):
                return 0
            cnt = 0
            for a, p in zip(a_sol, p_sol):
                if a == p:
                    cnt += 1
            if len(a_sol) == cnt:
                match += 1
    return 1.0 if len(sol_matrix) == match else 0.0


class RelaxShape(ABC):
    def __init__(self, wt):
        self.wt = wt

    @abstractmethod
    def validate(self, yp, y):
        pass


class RShapeRule1(RelaxShape):
    """
    Rule1: The dimensions should be valid.
    """

    def __init__(self, wt):
        """wt - denotes the importance of this rule."""
        self.wt = wt

    def validate(self, yp, y):
        r, c = len(y), len(y[0])
        rp, cp_arr = len(yp), [len(row) for row in yp]
        if r != rp:
            return 0.0
        for cx in cp_arr:
            if cx != c:
                return 0.0
        return 1.0 * self.wt


class RShapeRule2(RelaxShape):
    """
    Rule2: The values in each column should not repeat
    """

    def __init__(self, wt):
        """wt - denotes the importance of this rule."""
        self.wt = wt

    def validate(self, yp, y):
        for col in yp:
            found = {}
            for x in col:
                if x not in found:
                    found[x] = True
                else:
                    return 0.0
        return 1.0 * self.wt


def relax(pred_matrix, sol_matrix):
    """Partial row matching is allowed."""
    match = 0
    for a_sol in sol_matrix:
        for p_sol in pred_matrix:
            if len(a_sol) != len(p_sol):
                return 0
            cnt = 0
            for a, p in zip(a_sol, p_sol):
                if a == p:
                    cnt += 1
            if len(a_sol) == cnt:
                match += 1
    """Shape Match: 0.2; Solution Match: 0.8"""
    recipe_wt = [0.4, 0.6]
    recipes = [RShapeRule1(recipe_wt[0]), RShapeRule2(recipe_wt[1])]
    score_shape, score_solution = 0, 0
    for recipe in recipes:
        score_shape += recipe.validate(pred_matrix, sol_matrix)
    score_solution = match / len(sol_matrix)
    return score_shape * 0.2 + score_solution * 0.8


def verify(yp, y, strategy):
    if strategy == "strict":
        return strict(yp, y)
    elif strategy == "relax":
        return relax(yp, y)


class ParseSolution:
    def _grid_map(self, arr):
        matrix = []
        for row in arr:
            row = row.split("|")
            temp_row = []
            for x in row:
                if x:
                    temp_row.append(x)
            row = [x.strip() for x in temp_row]
            for idx, element in enumerate(row):
                for before, after in SUBSTITUTIONS:
                    element = element.replace(before, after)
                for expr in REMOVED_EXPRESSIONS:
                    element = element.replace(expr, "")
                row[idx] = element
            matrix.append(row)
        return matrix

    def _get_ref_solution(self, ground_truth: str):
        ground_arr = []
        sentences = re.split(r"\\n|\n", ground_truth)
        for line in sentences:
            line = line.strip().lower()
            if line == "":
                continue
            ground_arr.append(line)
        return self._grid_map(ground_arr)

    def _parse_solution(self, gen: str, grid_solution):

        # Create good elements.
        ref_x = set()
        for row in grid_solution:
            for x in row:
                ref_x.add(x)

        # Calculate score.
        line_arr, indx = [], -1
        score = []
        for line in re.split(r"\\n|\n", gen):
            line = line.lower().strip()
            SIMPLE_SUBSTITUTIONS = "{}()[]\"',"
            for ch in SIMPLE_SUBSTITUTIONS:
                line = line.replace(ch, "")
            indx += 1
            line_arr.append(line)
            acc, total = 0, 0
            if line == "":
                continue
            for x in line.split():
                for ref in ref_x:
                    ref_len, x_len = len(ref), len(x)
                    if ref_len < x_len:
                        continue
                    if ref[:x_len] == x:
                        acc += 1
                        break
                total += 1
            score.append((acc / total, indx))
        score.sort()

        # Pick up lines.
        r = len(grid_solution)
        line_rank = score[-r:]
        line_id = [idx for rank, idx in line_rank]
        solution = [line_arr[idx].strip() for idx in line_id]
        solution_grid = []
        for sx in solution:
            row = []
            for x in sx.split():
                for ref in ref_x:
                    ref_len, x_len = len(ref), len(x)
                    if ref_len < x_len:
                        continue
                    if ref[:x_len] == x:
                        row.append(ref)
            solution_grid.append(row)
        return solution_grid

    def pretty_print(self, grid, title):
        if logger.isEnabledFor(logging.DEBUG):
            print(Back.RED)
            print(f"--- {title} ---")
            print(Style.RESET_ALL)
            print(Fore.GREEN)
            for row in grid:
                print(" ".join(row))
            print()
            print(Style.RESET_ALL)

    def parse(self, solution_str: str, ground_truth: str):
        grid_solution = self._get_ref_solution(ground_truth)
        parsed_solution = self._parse_solution(solution_str, grid_solution)
        return parsed_solution, grid_solution


def compute_score(
    solution_str: str,
    ground_truth: str,
    extra_info: str,
    pause_tokens_index: Optional[list[int]] = None,
) -> float:
    """Compute the reward score for a solution.
    Args:
        solution_str: The solution string
        ground_truth: The ground truth answer
        strict_box_verify: Whether to use strict box verification
        pause_tokens_index: Indices of pause tokens
    Returns:
        Reward score (1.0 for correct, -1.0 for incorrect)
    """
    # Extract solution
    parse_obj = ParseSolution()
    yp, y = parse_obj.parse(solution_str, ground_truth)
    # Verify the solution
    strategy = extra_info["strategy"]
    correct = verify(yp, y, strategy)
    reward, acc = correct, correct
    logger.debug(
        f"""[TM]
            Reward[{reward}]
            RawResponse[{solution_str}]
        """
    )
    parse_obj.pretty_print(yp, title="Predicted Solution")
    parse_obj.pretty_print(y, title="Actual Solution")
    return {"score": reward, "acc": acc, "pred": ground_truth}
