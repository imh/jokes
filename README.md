About 0.5M jokes scraped from reddit.
They have scores based on votes and normalized scores to attempt to control for different subreddits with different voting patterns that change over time.

Many NSFW.
Dataset isn't super clean (not just in the NSFW sense).
Some posts aren't jokes, and many have "(edit: OMG front page!!)" and "I heard this one from my dad..." in addition to the joke.
Data is a bunch of self explanatory JSON objects, one per line.

Example JSON object:
```
{
  "edited": false,
  "name": "t3_3k3tno",
  "author": "v_cleaner",
  "url": "https://www.reddit.com/r/puns/comments/3k3tno/a_mexican_magician_tells_the_audience_he_will/",
  "num_comments": 9,
  "downs": 0,
  "title": "A Mexican magician tells the audience he will disappear on the count of 3. He says \"uno, dos, ...\" *POOF!*",
  "created_utc": "1441727095",
  "subreddit": "puns",
  "selftext": "He disappeared without a tres.\n\n(I'll see myself out)",
  "retrieved_on": 1450810995,
  "over_18": false,
  "gilded": 0,
  "score": 362,
  "normalized_score": 99.86541049798116,
  "ups": 362
}
```

Run `./explore.py` to poke around.
