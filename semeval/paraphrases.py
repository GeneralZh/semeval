from argparse import ArgumentParser
import logging
from ConfigParser import ConfigParser
import os

from read_and_enrich import ReadAndEnrich
from align_and_penalize import AlignAndPenalize
from sentence import SentencePair
from resources import Resources


def parse_args():
    p = ArgumentParser()
    p.add_argument('-c', '--conf', help='config file', default='config', type=str)
    return p.parse_args()


def read_config():
    args = parse_args()
    conf = ConfigParser(
        {"4langpath": os.environ["FOURLANGPATH"]})
    conf.read(args.conf)
    return conf


def main():
    conf = read_config()
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s : " +
        "%(module)s (%(lineno)s) - %(levelname)s - %(message)s")

    Resources.set_config(conf)
    reader = ReadAndEnrich(conf)
    pairs = reader.read_sentences()
    aligner = AlignAndPenalize(conf)
    for i, (s1, s2) in enumerate(pairs):
        if i % 1000 == 0:
            logging.info('{0} pairs'.format(i))
        pair = SentencePair(s1, s2)
        print(aligner.align(pair))

if __name__ == '__main__':
    import cProfile
    cProfile.run('main()', 'stats.cprofile')
    #main()
