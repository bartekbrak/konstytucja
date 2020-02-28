#!/usr/bin/env python3
import argparse
import json
import os
import random
import re


RANDOM = -1
INPUT = 'konstyt_1997.txt'
JSON_CACHE = 'konstyt_1997.json'


def get_article(art, skip_cache=False):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    json_cache = os.path.join(dir_path, JSON_CACHE)

    if os.path.exists(json_cache) and not skip_cache:
        with open(json_cache, 'r') as f:
            rozdziały = json.loads(f.read())
    else:
        with open(INPUT) as f:
            konstyt_1997 = f.read()

        rozdziały = re.compile(r'(Art\.\s*(\d+).*?)(?=Art\.\s*\d+\.|$)', flags=re.DOTALL)
        preambuła = re.match('(KONSTYTUCJA.*?)Rozdział I', konstyt_1997, flags=re.DOTALL).groups()[0]
        rozdziały = {v: k for k, v in rozdziały.findall(konstyt_1997)}
        rozdziały["0"] = preambuła
        with open(json_cache, 'w') as outfile:
            json.dump(rozdziały, outfile)
    if art == RANDOM:
        return random.choice(list(rozdziały.values()))
    return rozdziały[str(art)]


def parse_args():
    p = argparse.ArgumentParser(__doc__)
    p.add_argument('art', nargs='?', default=RANDOM, help='display this article, skip for random')
    return p.parse_args()

def main():
    args = parse_args()
    print(get_article(args.art))

if __name__ == '__main__':
    main()