import json
import random
import spacy
import re
from collections import Counter

def has_deleted_punchline(j):
    return j['selftext'] in ('[deleted]', '[removed]')

def has_extant_punchline(j):
    return len(j['selftext']) > 0 and not has_deleted_punchline(j)

def never_had_punchline(j):
    return len(j['selftext']) == 0

def dedup_whitespace(txt):
    txt = re.sub(r'\n\s*|\s*\n', '\n', txt)
    txt = re.sub(r'\r\s*|\s*\r', '\n', txt)
    txt = re.sub(r'\t\s*|\s*\t', ' ', txt)
    txt = re.sub(r'\s\s+', ' ', txt)
    txt = re.sub(r' +', ' ', txt)
    return txt

def to_newline_separable_toks(nlp, sent):
    sent = [word.lower_ for word in nlp(dedup_whitespace(sent))]
    return ' '.join(sent).replace(u'\n', u'\\n')

def write_with_punchlines(nlp, dot_whatever, jokes_with_punchlines):
    setups, punchlines = zip(*jokes_with_punchlines)
    setups = [to_newline_separable_toks(nlp, setup) for setup in setups]
    punchlines = [to_newline_separable_toks(nlp, punchline) for punchline in punchlines]
    with open('data/joke_setups'+dot_whatever, 'w') as joke_setup:
        joke_setup.write('\n'.join(setups).encode('utf-8'))
    with open('data/joke_punchlines'+dot_whatever, 'w') as joke_punchline:
        joke_punchline.write('\n'.join(punchlines).encode('utf-8'))

def write_oneliners(nlp, dot_whatever, jokes_without_punchlines):
    oneliners = [to_newline_separable_toks(nlp, oneliner) for oneliner in jokes_without_punchlines]
    with open('data/oneliners'+dot_whatever, 'w') as joke_oneliner:
        joke_oneliner.write('\n'.join(oneliners).encode('utf-8'))

with open('data/normalized_jokes.json', 'r') as f:
    jokes = map(json.loads, f.readlines())

jokes_with_punchline = filter(has_extant_punchline, jokes)
jokes_without_punchline = filter(never_had_punchline, jokes)

print len(jokes_with_punchline), 'jokes with punchlines'
print len(jokes_without_punchline), 'one liners'

dedup_with_punchlines = list(set([(j['title'], j['selftext']) for j in jokes_with_punchline]))
dedup_without_punchlines = list(set([j['title'] for j in jokes_without_punchline]))

print len(dedup_with_punchlines), 'unique jokes with punchlines'
print len(dedup_without_punchlines), 'unique oneliners'

random.shuffle(dedup_with_punchlines)
random.shuffle(dedup_without_punchlines)

train_with_punchlines = dedup_with_punchlines[2048:]
test_with_punchlines = dedup_with_punchlines[:2048]
train_without_punchlines = dedup_without_punchlines[2048:]
test_without_punchlines = dedup_without_punchlines[:2048]

nlp = spacy.load('en_core_web_md')

print 'tokenizing and writing jokes to train/test files. (this takes a while) ...'
write_oneliners(nlp, '.tst', test_without_punchlines)
write_oneliners(nlp, '.trn', train_without_punchlines)
write_with_punchlines(nlp, '.tst', test_with_punchlines)
write_with_punchlines(nlp, '.trn', train_with_punchlines)
print 'complete'