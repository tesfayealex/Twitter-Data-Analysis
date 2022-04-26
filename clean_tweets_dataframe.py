import pandas as pd
from datetime import datetime


class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """

    def __init__(self, df: pd.DataFrame):
        self.df = pd.DataFrame(data=df)
        print('Automation in Action...!!!')

    def drop_unwanted_column(self) -> pd.DataFrame:  # , df: pd.DataFrame
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        df = self.df
        unwanted_rows = df[df['retweet_count'] == 'retweet_count'].index
        df.drop(unwanted_rows, inplace=True)
        df = df[df['polarity'] != 'polarity']
        #self.df = df
        return df

    def drop_duplicate(self) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        df = self.df.drop_duplicates()

        #self.df = df

        return df

    def convert_to_datetime(self) -> pd.DataFrame:
        """
        convert column to datetime
        """
        df = self.df
        df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')

        df = df[df['created_at'] >= '2020-12-31']

        # self.df = df

        return df

    def convert_to_numbers(self) -> pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """
        df = self.df
        df['polarity'] = pd.to_numeric(df['polarity'], errors='coerce')
        df['subjectivity'] = pd.to_numeric(df['subjectivity'], errors='coerce')
        df['retweet_count'] = pd.to_numeric(
            df['retweet_count'], errors='coerce')
        df['favorite_count'] = pd.to_numeric(
            df['favorite_count'], errors='coerce')
        df['followers_count'] = pd.to_numeric(
            df['followers_count'], errors='coerce')

        #self.df = df
        return df

    def remove_non_english_tweets(self) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """
        df = self.df
        df = df.query("lang == 'en' ")
        #self.df = df
        return df
