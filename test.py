import argparse

parser = argparse.ArgumentParser()

parser.add_argument(
    '--hi',
    nargs='+'
)

args = parser.parse_args()
print(args)
