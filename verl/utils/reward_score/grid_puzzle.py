import re 
import logging 
from typing import Optional
logger = logging.getLogger(__name__)

# Constants for normalization
SUBSTITUTIONS = [
    ("an ", ""),
    ("a ", ""),
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
            if len(a_sol) != len(p_sol): return 0 
            cnt = 0 
            for a, p in zip(a_sol, p_sol):
                if a == p: cnt += 1
            if len(a_sol) == cnt: 
                match += 1
    return 1.0 if len(sol_matrix) == match else 0.0 


def relax(pred_matrix, sol_matrix):
    """Partial row matching is allowed."""
    match = 0
    for a_sol in sol_matrix:
        for p_sol in pred_matrix:
            if len(a_sol) != len(p_sol): return 0 
            cnt = 0 
            for a, p in zip(a_sol, p_sol):
                if a == p: cnt += 1
            if len(a_sol) == cnt: 
                match += 1
    return match/len(sol_matrix)


def grid_map(arr):
    matrix = []
    for row in arr:
        row = row.split('|')
        temp_row = []
        for x in row:
            if x: temp_row.append(x)
        row = [x.strip() for x in temp_row]
        # Apply substitutions and removals
        for idx, element in enumerate(row):
            for before, after in SUBSTITUTIONS:
                element = element.replace(before, after)
            for expr in REMOVED_EXPRESSIONS:
                element = element.replace(expr, "")
            row[idx] = element
        matrix.append(row)
    return matrix


def beautify_print(arr):
    for x in arr:
        logging.debug(x)
    logging.debug(f'-.'*25)


def verify(prediction, ground_truth, strategy):
    ground_truth_lower = ground_truth.lower()
    ground_arr, prediction_arr = [], []
    for x in ground_truth_lower.split('\n'):
        ground_arr.append(x)
    # beautify_print(ground_arr)
    ground_arr_x = grid_map(ground_arr)
    
    prediction_lower = prediction.lower()
    repeat = len(ground_arr)
    match_prediction = re.search(r'final answer\s*:?' + r'\s*(.*)'*repeat, prediction_lower)
    if match_prediction:
        for idx in range(repeat):
            prediction_arr.append(match_prediction.group(idx+1))
    # beautify_print(prediction_arr)
    prediction_arr_x = grid_map(prediction_arr)
    
    if strategy == 'strict':
        return strict(prediction_arr_x, ground_arr_x)
    elif strategy == 'relax':
        return relax(prediction_arr_x, ground_arr_x)


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
    # Verify the solution
    strategy = extra_info
    correct = verify(solution_str, ground_truth, strategy)
    
    # reward = 1.0 if correct else -1.0
    reward = correct
    acc = correct
    
    # [TM] score is what is important here 
    return {
        "score": reward,
        "acc": acc,
        "pred": ground_truth
    }
