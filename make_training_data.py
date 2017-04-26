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

def to_newline_separable_toks(nlp, replace_uncommon, sent):
    sent = [word.lower_ for word in nlp(dedup_whitespace(sent))]
    return replace_uncommon(' '.join(sent).replace(u'\n', u'\\n'))

def write_with_punchlines(nlp, replace_uncommon, dot_whatever, jokes_with_punchlines):
    setups, punchlines = zip(*jokes_with_punchlines)
    setups = [to_newline_separable_toks(nlp, replace_uncommon, setup) for setup in setups]
    punchlines = [to_newline_separable_toks(nlp, replace_uncommon, punchline) for punchline in punchlines]
    with open('data/joke_setups'+dot_whatever, 'w') as joke_setup:
        joke_setup.write('\n'.join(setups).encode('utf-8'))
    with open('data/joke_punchlines'+dot_whatever, 'w') as joke_punchline:
        joke_punchline.write('\n'.join(punchlines).encode('utf-8'))

url_strs = ('http://', 'https://', 'imgur.com', 'reddit.com', 'redd.it')
def not_contains_url(punchline):
    for s in url_strs:
        if s in punchline:
            return False
    return True

def write_oneliners(nlp, replace_uncommon, dot_whatever, jokes_without_punchlines):
    oneliners = [to_newline_separable_toks(nlp, replace_uncommon, oneliner) for oneliner in jokes_without_punchlines]
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

dedup_with_punchlines = [j for j in dedup_with_punchlines if not_contains_url(j[1])]

print len(dedup_with_punchlines), 'unique jokes with punchlines not containing certain urls'

random.shuffle(dedup_with_punchlines)
random.shuffle(dedup_without_punchlines)

n_train_punchy = int(len(dedup_with_punchlines)*0.1)
n_train_oneliner = int(len(dedup_without_punchlines)*0.1)

train_with_punchlines = dedup_with_punchlines[n_train_punchy:]
test_with_punchlines = dedup_with_punchlines[:n_train_punchy]
train_without_punchlines = dedup_without_punchlines[n_train_oneliner:]
test_without_punchlines = dedup_without_punchlines[:n_train_oneliner]

n_characters = 100
ctr = Counter((''.join([j[0] + j[1] for j in train_with_punchlines]) + ''.join(train_without_punchlines)).lower())
print len(ctr), 'total distinct characters, filtering to', n_characters+1
common_characters, _ = zip(*ctr.most_common(n_characters))
uncommon_regex = '[^.' + ''.join(map(re.escape,common_characters)) + ']'
replace_uncommon = lambda txt: re.sub(uncommon_regex, 'U', txt)

nlp = spacy.load('en')

print 'tokenizing and writing jokes to train/test files. (this takes a while) ...'
write_oneliners(nlp, replace_uncommon, '.tst', test_without_punchlines)
write_oneliners(nlp, replace_uncommon, '.trn', train_without_punchlines)
write_with_punchlines(nlp, replace_uncommon, '.tst', test_with_punchlines)
write_with_punchlines(nlp, replace_uncommon, '.trn', train_with_punchlines)
print 'complete'