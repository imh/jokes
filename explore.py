#!/usr/bin/env python
import json
import bz2
import os.path

def parse_and_sort(lines):
    jokes = map(json.loads, lines)
    return sorted(jokes, key=lambda j: j['normalized_score'], reverse=True)

if os.path.isfile('data/normalized_jokes.json'):
    with open('data/normalized_jokes.json', 'r') as f:
        jokes = parse_and_sort(f.readlines())
elif os.path.isfile('normalized_jokes.json.bz2'):
    with bz2.BZ2File('normalized_jokes.json.bz2', 'r') as f:
        jokes = parse_and_sort(f.readlines())
else:
    raise Exception('The jokes file seems to be missing :(')

print 'WARNING: MANY OF THESE JOKES ARE NSFW, OFFENSIVE, OR JUST BAD TASTE'

for j in jokes:
    raw_input('---- HIT ENTER FOR NEXT ---')
    print j['title']
    print j['selftext']

