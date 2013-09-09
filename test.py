from freevle import testing
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('configuration', help='Relative path to configuration file', nargs='?')
parser.add_argument('-bp', '--blueprints', metavar='BP', help='Blueprints to be tested.', nargs='*')
parser.add_argument('-ex', '--exclude', metavar='BP', help='Blueprints to be excluded.', nargs='*')
args = parser.parse_args()

if __name__ == '__main__':
    testing.run(args.blueprints, args.exclude or [])
