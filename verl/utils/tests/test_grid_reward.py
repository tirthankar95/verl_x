import sys

sys.path.append("/Users/tmittra/verl_x/")
from verl.utils.reward_score.grid_puzzle import compute_score
import pytest


def test_strict(test_suite1):
    extra_info = {"strategy": "strict"}
    # For 'solution_str': It should extract everything after 'Final Answer:'
    res_arr = []
    res = compute_score(
        test_suite1["prediction1"], test_suite1["ground_truth1"], extra_info
    )
    res_arr.append(res["score"] == 0)
    res = compute_score(
        test_suite1["prediction2"], test_suite1["ground_truth2"], extra_info
    )
    res_arr.append(res["score"] == 0)
    res = compute_score(
        test_suite1["ground_truth1"], test_suite1["ground_truth1"], extra_info
    )
    res_arr.append(res["score"] == 1.0)
    res = compute_score(
        test_suite1["ground_truth2"], test_suite1["ground_truth2"], extra_info
    )
    res_arr.append(res["score"] == 1.0)
    assert tuple(res_arr) == (True, True, True, True)


def test_relax(test_suite1):
    extra_info = {"strategy": "relax"}
    # For 'solution_str': It should extract everything after 'Final Answer:'
    res_arr = []
    res = compute_score(
        test_suite1["prediction1"], test_suite1["ground_truth1"], extra_info
    )
    res_arr.append(res["score"] == 0)
    res = compute_score(
        test_suite1["prediction2"], test_suite1["ground_truth2"], extra_info
    )
    res_arr.append(res["score"] > 0.4)
    res = compute_score(
        test_suite1["ground_truth1"], test_suite1["ground_truth1"], extra_info
    )
    res_arr.append(res["score"] == 1.0)
    res = compute_score(
        test_suite1["ground_truth2"], test_suite1["ground_truth2"], extra_info
    )
    res_arr.append(res["score"] == 1.0)
    assert tuple(res_arr) == (True, True, True, True)


@pytest.fixture
def test_suite1():
    ground_truth1 = """    2006 | nibner newt | 350\\n2007 | eldar elk | 315
    2008 | perens pig | 385\\n2009 | dobra dingo | 455
        """
    prediction1 = """Step-by-step solution:\\n1. First, we need to find the
    year when the dobra dingo was added to the endangered species list. Since it 
    was listed 2 years after the species with a population size of 315, the 
    dobra dingo was listed in 2006.\\n2. Next, we need to find the year when the 
    perens pig was added to the endangered species list. Since it was listed 2 
    years before the perens pig, the perens pig was added in 2004.\\n3. Then, we 
    need to find the year when the nibner newt was added to the endangered 
    species list. Since it was recognized as endangered in 2006, the nibner newt 
    was added in 2008.\\n4. Finally, we need to find the country in which each 
    species lives. From the clues, we know that the dobra dingo lives in South 
    Africa, the perens pig lives in Brazil, the nibner newt lives in Canada, and '
    the perens pig lives in the United States.\\nFinal Answer:\\n| Year | Species | Country | Population 
    |\\n|-------|----------|---------|-------------|\\n| 2006 | dobra dingo | South Africa | 315         |\\n| 2004 | perens pig | Brazil   | 350         
    |\\n| 2008 | nibner newt | Canada   | 385         |\\n| 2008 | perens pig | United States | 455         |
    """

    ground_truth2 = """"175 | Giraffe
    200 | Elephant
    150 | Kangaroo
    """
    prediction2 = """Step-by-step solution:

    First, let's create a table to organize the information.

    Height (in cm)	Animal Species
    150	Elephant
    175	Giraffe
    200	Kangaroo
    Now, let's assign a clue to each animal based on the given information:

    The elephant is the tallest animal. So, the elephant should be the tallest animal, and its height should be 200 cm.
    The giraffe is not the shortest animal. Since the elephant is the tallest, the giraffe should be the second tallest, and its height should be between 150 cm and 175 cm.
    The giraffe is the tallest animal. So, the giraffe should be the tallest animal, and its height should be 200 cm.
    The elephant is the tallest animal. So, the elephant should be the tallest animal, and its height should be 200 cm.
    The giraffe is not the shortest animal. So, the giraffe should be the second tallest animal, and its height should be between 150 cm and 175 cm.
    The elephant is the tallest animal. So, the elephant should be the tallest animal, and its height should be 200 cm.
    The giraffe is not the shortest animal. So, the giraffe should be the second tallest animal, and its height should be between 150 cm and 175 cm.
    The giraffe is the tallest animal. So, the giraffe should be the tallest animal, and its height should be 200 cm.
    The elephant is the tallest animal. So, the elephant should be the tallest animal, and its height should be 200 cm.
    Therefore, the animals in order of height are:

    Giraffe (150 cm)
    Elephant (175 cm)
    Kangaroo (200 cm)"""
    return {
        "ground_truth1": ground_truth1,
        "prediction1": prediction1,
        "ground_truth2": ground_truth2,
        "prediction2": prediction2,
    }
