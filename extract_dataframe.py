import json
import pandas as pd
import re
from textblob import TextBlob


def read_json(json_file: str) -> list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file

    Returns
    -------
    length of the json file and a list of json
    """

    tweets_data = []
    for tweets in open(json_file, 'r'):
        tweets_data.append(json.loads(tweets))

    return len(tweets_data), tweets_data


class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe

    Return
    ------
    dataframe
    """

    def __init__(self, tweets_list):

        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self) -> list:
        statuses_count = [tweet['user']['statuses_count']
                          for tweet in self.tweets_list]
        return statuses_count

    def find_full_text(self) -> list:

        text = [tweet['text'].replace(',', ' ') for tweet in self.tweets_list]
        return text

    def find_sentiments(self, text) -> list:

        polarity = []
        subjectivity = []
        sentiment = []
        xo = True
        for t in text:
            each_sentiment = TextBlob(t).sentiment
            polarity.append(each_sentiment.polarity)
            subjectivity.append(each_sentiment.subjectivity)
            if each_sentiment.polarity > 0:
                sentiment.append("positive")
            elif each_sentiment.polarity < 0:
                sentiment.append("negative")
            else:
                sentiment.append("neutral")
        self.subjectivity = subjectivity
        return polarity, self.subjectivity, sentiment

    def find_created_time(self) -> list:

        created_at = [tweet['created_at'] for tweet in self.tweets_list]
        return created_at

    def find_source(self) -> list:

        source = [tweet['source'] for tweet in self.tweets_list]

        return source

    def find_screen_name(self) -> list:

        screen_name = [tweet['user']['screen_name'].replace(',', ' ')
                       for tweet in self.tweets_list]
        return screen_name

    def find_followers_count(self) -> list:

        followers_count = [tweet['user']['followers_count']
                           for tweet in self.tweets_list]
        return followers_count

    def find_friends_count(self) -> list:
        friends_count = [tweet['user']['friends_count']
                         for tweet in self.tweets_list]
        return friends_count

    def is_sensitive(self) -> list:
        try:
            is_sensitive = [x['possibly_sensitive']
                            if 'possibly_sensitive' in x else None for x in self.tweets_list]
        except KeyError:
            is_sensitive = []

        return is_sensitive

    def find_favourite_count(self) -> list:
        favourites_count = [tweet['user']['favourites_count']
                            for tweet in self.tweets_list]
        return favourites_count

    def find_retweet_count(self) -> list:
        retweet_count = [tweet['retweet_count'] for tweet in self.tweets_list]
        return retweet_count

    def find_hashtags(self) -> list:
        # hashtags = [tweet['entities']['hashtags']
        # for tweet in self.tweets_list]
        # or if only hashtag text is needed
        hashtags = []
        for tweet in self.tweets_list:
            values = ""
            for hashtag in tweet['entities']['hashtags']:
                if hashtag['text'] != "" or hashtag['text'] != " ":
                    values = values + hashtag['text'].replace(',', ' ') + "___"
            if values == "":
                values = " "
            hashtags.append(values)
        return hashtags

    def find_mentions(self) -> list:
        # mentions = [tweet['entities']['user_mentions']
        # for tweet in self.tweets_list]
        # or if only user mention  screen name or name  is needed
        mentions = []
        for tweet in self.tweets_list:
            values = ""
            for user_mentions in tweet['entities']['user_mentions']:
                if user_mentions['screen_name'] != "" or user_mentions['screen_name'] != " ":
                    values = values + \
                        user_mentions['screen_name'].replace(',', ' ') + "___"
            if values == "":
                values = " "
            mentions.append(values)
        return mentions

    def find_location(self) -> list:

        try:
            location = [tweet['user']['location'] if tweet['user']
                        ['location'] != "" else None for tweet in self.tweets_list]
        except TypeError:
            location = []

        return location

    def find_lang(self) -> list:

        lang = [tweet['lang'] for tweet in self.tweets_list]

        return lang

    def find_clean_text(self) -> list:
        clean_text = [re.sub("[^a-zA-Z0-9#@\s’,_]", "", text)
                      for text in self.find_full_text()]
        clean_text = [re.sub("\s+", " ", text) for text in clean_text]
        return clean_text

    def get_tweet_df(self, save=False) -> pd.DataFrame:
        """required column to be generated you should be creative and add more features"""

        columns = ['created_at', 'source', 'original_text', 'clean_text', 'polarity', 'subjectivity', 'sentiment', 'lang', 'favorite_count', 'retweet_count',
                   'original_author', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place']

        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        clean_text = self.find_clean_text()
        polarity, subjectivity, sentiment = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, clean_text, polarity, subjectivity, sentiment, lang, fav_count, retweet_count,
                   screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('data/processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')

        return df


if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text', 'clean_text', 'sentiment', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count',
               'original_author', 'screen_count', 'followers_count', 'friends_count', 'possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df()

    # use all defined functions to generate a dataframe with the specified columns above
