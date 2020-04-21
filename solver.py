from ortools.sat.python import cp_model
from country_printer import CountriesPartialSolutionPrinter
import utils

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--input_file", type=str, help="Countries input file", required=True)
parser.add_argument("--output_file", type=str, help="Optional output file to write solution to (.txt)")
parser.add_argument("--num_solutions", type=int, help="Maximum number of solutions to print, if 0, print all", default = 5)

args = parser.parse_args()

letters = utils.get_letters()
countries = utils.load_countries_file(args.input_file)

def get_all_countries(countries):
    return list(countries.keys())

def get_all_cities(countries):
    all_cities = []
    for country in countries.keys():
        all_cities.extend(countries.get(country))
    return all_cities

def create_country_variables(countries):
    place_country = {}
    place_letter = {}
    all_countries = get_all_countries(countries)
    for co in all_countries:
        # Get the first letter of the country
        country_letter = co[0].lower()
        country_var = model.NewBoolVar("Letter: {0}, Country: {1}".format(country_letter, co))

        # The country starting letter counts towards that country
        place_country.update({co: place_country.get(co, []) + [country_var]})

        # The country starting letter counts towards that letter
        place_letter.update({country_letter: place_letter.get(country_letter, []) + [country_var] })

        for ci in countries[co]:
            # Get the first letter of the city (or place)
            city_letter = ci[0].lower()

            # The city starting letter counts towards that country
            city_var = model.NewBoolVar("Letter: {0}, City: {1}".format(city_letter, ci))
            place_country.update({co: place_country.get(co, []) + [city_var]})

            # The city starting letter counts towards that letter
            place_letter.update({city_letter: place_letter.get(city_letter, []) + [city_var]})
    return place_country, place_letter


all_countries = get_all_countries(countries)
all_cities = get_all_cities(countries)
print("Number of Countries: ", len(all_countries))
print("Number of Cities: ", len(all_cities))

model = cp_model.CpModel()

# For every letter, create a variable for every city and country they're part of.
place_country, place_letter = create_country_variables(countries)

# Each Letter should be used once
for l in letters:
  if place_letter.get(l) is None:
    print("Missing Letter: ", l)
  model.Add(sum(place_letter.get(l, [])) == 1)

# Each Country should be used at least once
for co, var in place_country.items():
  model.Add(sum(var) >= 1)

# Solve the problem
solver = cp_model.CpSolver()
solver.parameters.linearization_level = 0

solution_printer = CountriesPartialSolutionPrinter(place_letter, num_solutions = args.num_solutions)
solver.SearchForAllSolutions(model, solution_printer)

print('Statistics')
print('  - conflicts       : %i' % solver.NumConflicts())
print('  - branches        : %i' % solver.NumBranches())
print('  - wall time       : %f s' % solver.WallTime())
print('  - solutions found : %i' % solution_printer.solution_count())

if args.output_file is not None:
    solution_printer.write(args.output_file)
