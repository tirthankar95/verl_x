def get_temp0():
    return """Form a grid puzzle using the following template. 
A logic grid puzzle should have a story and clues.

Categories:
{}

{}: {}
{}: {}
{}: {}

Clues:
Create a row in grid puzzle such that {}, {}, {} are in one row(directly related) 
Create a row in grid puzzle such that {}, {}, {} are in one row(directly related) 
Create a row in grid puzzle such that {}, {}, {} are in one row(directly related) 

Your job is to fill in the following values in the following JSON.
{{
    "story": "",
    "clues": "",
}}
No extra commentary or explanation. Only output valid JSON."""


def get_temp1():
    return """Form a grid puzzle using the following template. 
A logic grid puzzle should have a story and clues.

Categories:
{}

{}: {}
{}: {}
{}: {}

Clues:
Create a row in grid puzzle such that {}, {}, {} are in one row(directly related) 
Create a row in grid puzzle such that {}, {}, {} are in one row(directly related) 
{} is either {} or {}
{} and {} are related

Your job is to fill in the following values in the following JSON.
{{
    "story": "",
    "clues": "",
}}
No extra commentary or explanation. Only output valid JSON."""


def get_temp2():
    return """Form a grid puzzle using the following template. 
A logic grid puzzle should have a story and clues.

Categories:
{}

{}: {}
{}: {}
{}: {}

Clues:
Create a row in grid puzzle such that {}, {}, {} are in one row(directly related) 
{} is either {} or {}
{} is either {} or {}
{} and {} are related
{} and {} are related 

Your job is to fill in the following values in the following JSON.
{{
    "story": "",
    "clues": "",
}}
No extra commentary or explanation. Only output valid JSON."""


def get_temp3():
    return """Form a grid puzzle using the following template. 
A logic grid puzzle should have a story and clues.

Categories:
{}

{}: {}
{}: {}
{}: {}

Clues:
{} of {} category relation with {}
{} category relation with {} of {}
{} is either {} or {}
{} and {} are related
{} and {} are related 

Your job is to fill in the following values in the following JSON.
{{
    "story": "",
    "clues": "",
}}
No extra commentary or explanation. Only output valid JSON."""
