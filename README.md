# Loadsmart Challenge

the most fun I've done so far

## Required
* Python (3.7) 

## Installation

Create an virtual environment

    python3 -m venv venv
    

Activate the environment

    source venv/bin/activate

Install dependencies (pytest, isort and flake8)

    pip install -r requirements.txt
    
    
## Use guide

To get the best result


    python main.py
    
To get other results ordered by it's distances


    python main.py --all-combinations
    
*if you do not want verbose logs just add `--no-verbose`*

## To run lint and tests

    make test
    
    
Thanks!
