def get_temp0():
    return """Form a grid puzzle using the following template. 
A logic grid puzzle should have a story and clues.

For example a 3x4 grid puzzle should have 3 categories, and each category should contain 4 distinct values.
The solution to a grid puzzle 

Categories:
{}

{}: {}
{}: {}

Clues:
{} and {} are directly related.

Donot provide extra clues, if there is one clue under the sub topic Clues, provide only one clue.
Your job is to fill in the following values in the following JSON.
{{
    "story": "",
    "clues": "",
}}
No extra commentary or explanation. Only output valid JSON."""


def get_temp1():
    return """Form a grid puzzle using the following template. 
A logic grid puzzle should have a story and clues.

For example a 3x4 grid puzzle should have 3 categories, and each category should contain 4 distinct values.
The solution to a grid puzzle 

Categories:
{}

{}: {}
{}: {}

Clues:
{} is not related to {}.

Donot provide extra clues, if there is one clue under the sub topic Clues, provide only one clue.
Your job is to fill in the following values in the following JSON.
{{
    "story": "",
    "clues": "",
}}
No extra commentary or explanation. Only output valid JSON."""
