import sys

sys.path.append("/Users/tmittra/verl_x/")
print(sys.path)
from verl.utils.reward_score.grid_puzzle import compute_score


def test_dummy():
    solution_str = """Step-by-step solution:\\n1. First, we need to find the
year when the dobra dingo was added to the endangered species list. Since it 
was listed 2 years after the species with a population size of 315, the 
dobra dingo was listed in 2006.\\n2. Next, we need to find the year when the 
perens pig was added to the endangered species list. Since it was listed 2 
years before the perens pig, the perens pig was added in 2004.\\n3. Then, we 
need to find the year when the nibner newt was added to the endangered 
species list. Since it was recognized as endangered in 2006, the nibner newt 
was added in 2008.\\n4. Finally, we need to find the country in which each 
species lives. From the clues, we know that the dobra dingo lives in South 
Africa, the perens pig lives in Brazil, the nibner newt lives in Canada, and 
the perens pig lives in the United States.\\nFinal Answer:\\n| Year | 
Species | Country | Population 
|\\n|-------|----------|---------|-------------|\\n| 2006 | dobra dingo | 
South Africa | 315         |\\n| 2004 | perens pig | Brazil   | 350         
|\\n| 2008 | nibner newt | Canada   | 385         |\\n| 2008 | perens pig | 
"United States | 455         |
    """
    ground_truth = """
    2006 | nibner newt | 350\\n2007 | eldar elk | 315\\n2008 | perens pig | 385\\n2009 | dobra dingo | 455
    """
    extra_info = {"strategy": "strict"}
    # For 'solution_str': It should extract everything after 'Final Answer:'
    print(compute_score(solution_str, ground_truth, extra_info))
    assert True
