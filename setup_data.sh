#!/bin/bash
bunzip2 -k normalized_jokes.json.bz2
mkdir -p data
mv normalized_jokes.json data
python make_training_data.py
[[ -d subword-nmt ]] || git clone git@github.com:rsennrich/subword-nmt.git
cd subword-nmt
cat ../data/joke_setups.trn ../data/joke_punchlines.trn ../data/oneliners.trn | ./subword_nmt/learn_bpe.py -s 10000 > ../data/codes.bpe
./subword_nmt/apply_bpe.py -c ../data/codes.bpe < ../data/joke_setups.trn > ../data/joke_setups.trn.bpe
./subword_nmt/apply_bpe.py -c ../data/codes.bpe < ../data/joke_punchlines.trn > ../data/joke_punchlines.trn.bpe
./subword_nmt/apply_bpe.py -c ../data/codes.bpe < ../data/joke_setups.tst > ../data/joke_setups.tst.bpe
./subword_nmt/apply_bpe.py -c ../data/codes.bpe < ../data/joke_punchlines.tst > ../data/joke_punchlines.tst.bpe
./subword_nmt/apply_bpe.py -c ../data/codes.bpe < ../data/oneliners.trn > ../data/oneliners.trn.bpe
./subword_nmt/apply_bpe.py -c ../data/codes.bpe < ../data/oneliners.tst > ../data/oneliners.tst.bpe
cd ..
python make_vocabs.py
