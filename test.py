from freevle import testing
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('configuration', help='Relative path to configuration file', nargs='?')
parser.add_argument('-bp', '--blueprints', metavar='BP', help='Blueprints to be tested.', nargs='*')
args = parser.parse_args()

if __name__ == '__main__':
    testing.run(args.blueprints)
