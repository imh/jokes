#!/bin/bash
bunzip2 -k normalized_jokes.json.bz2
mkdir -p data
mv normalized_jokes.json data
python make_training_data.py
