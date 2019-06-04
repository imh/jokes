with open('data/joke_setups.trn.bpe', 'r') as f:
    setup_words = set(f.read().split())
with open('data/joke_setups.bpe.vocab', 'w') as f:
    f.write('\n'.join(setup_words))
with open('data/joke_punchlines.trn.bpe', 'r') as f:
    setup_words = set(f.read().split())
with open('data/joke_punchlines.bpe.vocab', 'w') as f:
    f.write('\n'.join(setup_words))
with open('data/oneliners.trn.bpe', 'r') as f:
    setup_words = set(f.read().split())
with open('data/oneliners.bpe.vocab', 'w') as f:
    f.write('\n'.join(setup_words))
