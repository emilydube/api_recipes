#Using the Nuance Automatic Speech Recognition (ASR) System

This sample submits an audio file to the Nuance ASR and then submits the resultant text to the Receptiviti API for analysis. You will need to obtain a Nuance app id and app key from [Nuance's Developer Website](https://developer.nuance.com). Refer to their HTTP platform SDK docs for more details.

This sample is in Python.

##Using the sample

Install the requirements.

```pip install -r requirements.txt```

Copy config.ini.sample to config.ini, and place your Nuance and Receptiviti credentials the config.ini file, then run:-

```python analyse.py <audio clip name> <clip id>```

The clip id is used by Nuance to track audio samples of the same person to improve detection. Use *npr* for the sample clip:-

```python analyse.py NPRWeekly-Roundup-Snippet.wav npr```

You will see output similar to the following:-

```
$ python analyse.py clips/NPRWeekly-Roundup-Snippet.wav npr
Transcribed text:  Today was the Associated Press who most news organizations including NPR follow their guidance on on Dell get official totals called around on pledged delegates and other found enough on pledged delegates you said yes I will be voting for Donald Trump on the first ballot to get Donald Trump over that majority total which is 1237 that's the number we said more than any other member of the podcast this year we thought the trunk would not build to get there until that last day of primaries June 7 which includes California but now because more and more and pledged delegates are saying yeah he's the only guy left is going to be the nominee I'm gonna vote for him he's already there

Profile:  {
    "liwc_scores": {
        "tone": 25.774195, 
        "sixLtr": 0.16233766, 
        "clout": 75.751625, 
        "wps": 123.2, 
        "analytic": 64.60387, 
        "wc": 616, 
        "dic": 0.8133117, 
        "authentic": 39.9905, 
        "categories": {
            "SemiC": 0.0, 
            "relig": 0.0, 
            "compare": 0.040584415, 
            "pronoun": 0.14285715, 
            "QMark": 0.0, 
            "feel": 0.008116883, 
            "money": 0.0, 
            "insight": 0.016233766, 
            "assent": 0.016233766, 
            "number": 0.024350649, 
            "sad": 0.0, 
            "time": 0.073051944, 
            "anger": 0.0, 
            "see": 0.0, 
            "OtherP": 0.0, 
            "female": 0.0, 
            "article": 0.056818184, 
            "negate": 0.008116883, 
            "home": 0.0, 
            "conj": 0.048701297, 
            "sexual": 0.0, 
            "negemo": 0.0, 
            "ppron": 0.07467532, 
            "Dash": 0.0, 
            "differ": 0.040584415, 
            "death": 0.0, 
            "family": 0.0, 
            "adverb": 0.048701297, 
            "space": 0.058441557, 
            "informal": 0.024350649, 
            "anx": 0.0, 
            "Period": 0.0, 
            "achieve": 0.008116883, 
            "focuspresent": 0.12987013, 
            "Apostro": 0.03409091, 
            "netspeak": 0.008116883, 
            "percept": 0.032467533, 
            "quant": 0.056818184, 
            "certain": 0.008116883, 
            "relativ": 0.15584415, 
            "health": 0.0, 
            "nonflu": 0.0, 
            "adj": 0.040584415, 
            "prep": 0.13636364, 
            "friend": 0.008116883, 
            "body": 0.0, 
            "bio": 0.0, 
            "we": 0.016233766, 
            "risk": 0.0, 
            "power": 0.040584415, 
            "interrog": 0.019480519, 
            "discrep": 0.008116883, 
            "function": 0.48863637, 
            "drives": 0.097402595, 
            "leisure": 0.008116883, 
            "you": 0.008116883, 
            "Quote": 0.0, 
            "verb": 0.21103896, 
            "hear": 0.024350649, 
            "focuspast": 0.056818184, 
            "they": 0.008116883, 
            "affect": 0.0, 
            "AllPunc": 0.03409091, 
            "Parenth": 0.0, 
            "Exclam": 0.0, 
            "tentat": 0.016233766, 
            "reward": 0.024350649, 
            "ipron": 0.06818182, 
            "affiliation": 0.024350649, 
            "i": 0.016233766, 
            "cause": 0.008116883, 
            "work": 0.040584415, 
            "cogproc": 0.097402595, 
            "ingest": 0.0, 
            "motion": 0.024350649, 
            "filler": 0.0, 
            "swear": 0.0, 
            "Comma": 0.0, 
            "Colon": 0.0, 
            "focusfuture": 0.024350649, 
            "posemo": 0.0, 
            "auxverb": 0.097402595, 
            "male": 0.03409091, 
            "shehe": 0.025974026, 
            "social": 0.11038961
        }
    }, 
    "receptiviti_scores": {
        "percentiles": {
            "netspeak_focus": 27.787871186440675, 
            "body_focus": 7.323878556392286, 
            "conscientious": 87.1952164549609, 
            "family_oriented": 31.6738847713908, 
            "neuroticism": 2.0332436564051717, 
            "social_skills": 25.241622393412147, 
            "openness": 18.826514203551117, 
            "cold": 7.779753588440925, 
            "sexual_focus": 31.105849582172702, 
            "religion_oriented": 23.085602569473537, 
            "happiness": 87.87990244680657, 
            "food_focus": 15.079053843759723, 
            "adjustment": 96.04276673407449, 
            "achievement_driven": 59.41034799737141, 
            "friend_focus": 73.43631850419085, 
            "extraversion": 13.283375884983796, 
            "depression": 12.001272488093367, 
            "agreeable": 80.45862191372213, 
            "independent": 80.20183143947591, 
            "type_a": 71.21681283512115, 
            "workhorse": 58.0943967943969, 
            "reward_bias": 85.23779485192837, 
            "insecure": 18.22313765673864, 
            "leisure_oriented": 19.286652274035692, 
            "impulsive": 3.2359188265894208, 
            "thinking_style": 69.45281243972019, 
            "persuasive": 92.96436570781887, 
            "power_driven": 81.5336660484351, 
            "money_oriented": 16.467283950617283, 
            "health_oriented": 8.603650525525525, 
            "work_oriented": 81.01293687007973
        }, 
        "raw_scores": {
            "netspeak_focus": 0.8116883, 
            "body_focus": 0.0, 
            "conscientious": 2.229335740464198, 
            "family_oriented": 2.5943478203062496, 
            "neuroticism": 0.959591936823132, 
            "social_skills": 0.7824992409649358, 
            "openness": 0.9471135947654495, 
            "cold": -3.2783453299630354, 
            "sexual_focus": 0.0, 
            "religion_oriented": 0.0, 
            "happiness": 7.7290978878183125, 
            "food_focus": 0.0, 
            "adjustment": -0.42181371302946835, 
            "achievement_driven": 4.628062726198208, 
            "friend_focus": 0.8116883, 
            "extraversion": 1.187836536585366, 
            "depression": -0.8535578438673022, 
            "agreeable": 1.6678526712328767, 
            "independent": -3.3554205052899455, 
            "type_a": 8.597121915125696, 
            "workhorse": -2.171218764876559, 
            "reward_bias": 2.4350649, 
            "insecure": -0.7382207021494056, 
            "leisure_oriented": 0.8116883, 
            "impulsive": -1.5853287109374998, 
            "thinking_style": -0.7067991033311001, 
            "persuasive": 2.2855564395309043, 
            "power_driven": 6.946653081387028, 
            "money_oriented": 0.0, 
            "health_oriented": 0.0, 
            "work_oriented": 2.5
        }
    }, 
    "personality_snapshot": [
        {
            "description": "Tends to be somewhat hopeful and optimistic, often expecting the best. They often have a light sense of humor.", 
            "summary": "Optimistic."
        }, 
        {
            "description": "Tends to make decisions only after carefully weighing all the options. They naturally prefer to study the details of a problem and consider the possible consequences of their actions.", 
            "summary": "High self-control."
        }, 
        {
            "description": "Likely a relatively grounded person. They tend to value friendships, work hard, and have healthy life goals.", 
            "summary": "Well-adjusted."
        }
    ]
}
```
