from ortools.sat.python import cp_model

class CountriesPartialSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, place_letter, num_solutions = None):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self._place_letter = place_letter
        self._num_solutions = num_solutions
        self._solution_count = 0
        self._solution_vars = []

    def on_solution_callback(self):
        if self._num_solutions is None or self._solution_count in list(range(self._num_solutions)):
          print('Solution %i' % self._solution_count)
          places_str = []
          for l, places in self._place_letter.items():
              for place in places:
                if self.BooleanValue(place):
                  places_str.append(str(place))
          print_places_str = "\n".join(sorted(places_str))
          print(print_places_str)
          print()
          self._solution_vars.append('Solution ' + str(self._solution_count))
          self._solution_vars.append(print_places_str)
          self._solution_vars.append("")
        self._solution_count += 1

    def solution_count(self):
        return self._solution_count

    def write(self, filename):
        with open(filename, "w") as f:
            f.write("\n".join(self._solution_vars))
