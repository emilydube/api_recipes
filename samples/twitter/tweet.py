import re

from titlecase import titlecase

MINIMUM_TWEETS = 50


def ends_with_url(tweet):
    urls = sorted(tweet.entities.get('urls', []), key=lambda e: e['indices'][1], reverse=True)
    return len(urls) > 0 and urls[0]['indices'][1] == len(tweet.text)


def is_shared_news_article(tweet):
    return ends_with_url(tweet) and titlecase(tweet.text) == tweet.text


def is_retweet(tweet):
    return tweet.text.startswith("RT")


def is_original_tweet(tweet):
    return not is_retweet(tweet) and not is_shared_news_article(tweet)


def is_english_tweet(tweet):
    return tweet.lang == 'en'


def format_tweet_text(tweet):
    tweet_text = tweet.text
    tweet_text = remove_indices(tweet_text, get_indices(tweet))
    tweet_text = " ".join([word for word in tweet_text.split(' ') if re.search('[a-zA-Z0-9]', word)])
    return tweet_text


def remove_indices(tweet_text, all_indices):
    for indices in sorted(all_indices, key=lambda i: i[0], reverse=True):
        tweet_text = tweet_text[0:indices[0]] + tweet_text[indices[1]:]

    return re.sub('\s+', ' ', tweet_text.strip())


def get_indices(tweet):
    indices = []
    for k, entities in tweet.entities.iteritems():
        for entity in entities:
            indices.append(entity['indices'])

    return indices


def get_tweet_text(tweet):
    if is_original_tweet(tweet) and is_english_tweet(tweet):
        return format_tweet_text(tweet).encode('utf-8')
    return None
