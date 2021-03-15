from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('year')
parser.add_argument('-d', '--data')
args = parser.parse_args()
