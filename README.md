# Instagram-Alphabet-Travel-Challenge-Solver

# Goal
Given a list of cities or tourism destinations and their respective country, produce a list of places such that:
	- Every letter of the alphabet is represented *exactly once*
	- Every every country is represented *at least once*

## Setup
### Install Dependencies
```{bash}
pip3 install -r requirements.txt
```

### Setup Countries File
Create a new `countries.yaml` file.  Have it setup in this way:
```{yaml}
Canada:
  - Toronto
  - Niagra Falls
  - Kelowna
  - Montreal
United States:
  - Seattle
  - New York
```
Once you have input all of the countries and destinations, you are ready for the next step.

### Run
```{bash}
python3 solver.py --input_file {{ countries file }} --output_file {{ output.txt }} --num_solutions {{ 5 }}
```

Replaces `countries file` with your file, in this case, `countries.yaml`.  The output of each solutions can optionally be written to a file, specified by `--output_file`.  Finally, you can limit the number of solutions printed.  0 for all solutions, defaults to 5.
