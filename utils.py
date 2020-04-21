import string
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def get_letters():
    return list(string.ascii_lowercase)


def load_countries_file(filename):
    with open(filename, "r") as f:
        countries = yaml.load(f, Loader=Loader)
        return countries
