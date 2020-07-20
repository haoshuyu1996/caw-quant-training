from crypto_news_api import CryptoControlAPI
import pandas as pd
import requests
import os
import json
import csv

data_dir = './CryptoControl_News'
os.chdir(os.path.dirname(os.path.abspath(__file__)))
path = os.getcwd()
os.mkdir(data_dir)


def save_j(data, name):
    with open(os.path.join(data_dir, name), 'w') as json_file:
        json.dump(data, json_file, indent=4)
        print('successfully saved as json')


def save_csv(data, name):
    data.to_csv(os.path.join(data_dir, name), encoding='utf-8-sig')
    print('successfully saved as csv')


def format_df(data):
    news = pd.DataFrame(data)
    formated_data = pd.DataFrame()
    tweet_index = [
        'publishedAt',
        'username',
        'text',
        'language',
        'retweetCount',
        'hotness',
        'url']
    reddit_index = [
        'publishedAt',
        'subreddit',
        'title',
        'description',
        'comments',
        'hotness',
        'url']
    article_index = [
        'publishedAt',
        'title',
        'words',
        'description',
        'url',
        'primaryCategory']

    try:
        if news.columns[0] == 'retweetCount':
            formated_data = news[tweet_index]

        elif news.columns[0] == 'comments':
            formated_data = news[reddit_index]

        elif news.columns[0] == 'type':
            for t in latest_coin_feed:
                if t['type'] == 'article':
                    news = pd.DataFrame(
                        [t['article']], columns=t['article'].keys())
                    news = news[article_index]
                    formated_data = pd.concat(
                        [formated_data, news], ignore_index=True, axis=0)

                elif t['type'] == 'reddit':
                    news = pd.DataFrame(
                        [t['reddit']], columns=t['reddit'].keys())
                    news = news[reddit_index]
                    formated_data = pd.concat(
                        [formated_data, news], ignore_index=True, axis=0)

                elif t['type'] == 'tweet':
                    news = pd.DataFrame(
                        [t['tweet']], columns=t['tweet'].keys())
                    news = news[tweet_index]
                    formated_data = pd.concat(
                        [formated_data, news], ignore_index=True, axis=0)

        else:
            formated_data = news[article_index]

    except BaseException:
        raise Exception('Data can not be formated')

    return formated_data


with open(os.path.join(path, 'cryptocontrol_api.json'), mode='r') as key_file:
    key = json.loads(key_file.read())['key']

# Connect to the CryptoControl API
api = CryptoControlAPI(key)

# Connect to a self-hosted proxy server (to improve performance) that
# points to cryptocontrol.io
proxyApi = CryptoControlAPI(key, "http://cryptocontrol_proxy/api/v1/public")

# Do not Enable the sentiment datapoints unless you're a premium user,
# because raise exception does not returns you the message of status 405
# but returns the message when status is not '200'

# Get top news
top_news = api.getTopNews()
tn = format_df(top_news)
save_j(top_news, 'top_news.json')
save_csv(tn, 'top_news.csv')

# get top news by category
top_category_news = api.getTopNewsByCategory()
ctn = format_df(top_category_news['analysis'])
save_j(top_category_news, 'top_category_news.json')
save_csv(ctn, 'top_category_news.csv')

# get coin news
top_coin_news = api.getTopNewsByCoin("bitcoin")
cn = format_df(top_coin_news)
save_j(top_coin_news, 'top_coin_news.json')
save_csv(cn, 'top_coin_news.csv')

# get latest news
latest_news = api.getLatestNews()
ln = format_df(latest_news)
save_j(latest_news, 'latest_news.json')
save_csv(ln, 'latest_news.csv')

# get latest news by coin
latest_coin_news = api.getLatestNewsByCoin("bitcoin")
lcn = format_df(latest_coin_news)
save_j(latest_coin_news, 'latest_coin_news.json')
save_csv(lcn, 'latest_coin_news.csv')

# get top news by category for a paticular coin
top_news_coin_category = api.getTopNewsByCoinCategory("bitcoin")
tncc = format_df(top_news_coin_category)
save_j(top_news_coin_category, 'top_news_coin_category.json')
save_csv(tncc, 'top_news_coin_category.csv')

# get top tweets
top_coin_tweets = api.getTopTweetsByCoin("bitcoin")
tct = format_df(top_coin_tweets)
save_j(top_coin_tweets, 'top_coin_tweets.json')
save_csv(tct, 'top_coin_tweets.csv')

# get latest tweets by coin
latest_coin_tweets = api.getLatestTweetsByCoin('bitcoin')
lct = format_df(latest_coin_tweets)
save_j(latest_coin_tweets, 'latest_coin_tweets.json')
save_csv(lct, 'latest_coin_tweets.csv')

# get Get top reddit posts for a particular coin
top_coin_reddits = api.getTopRedditPostsByCoin("bitcoin")
tcr = format_df(top_coin_reddits)
save_j(top_coin_reddits, 'top_coin_reddits.json')
save_csv(tcr, 'top_coin_reddits.csv')

# get latest Ripple reddit posts
latest_coin_posts = api.getLatestRedditPostsByCoin("ripple")
lcp = format_df(latest_coin_posts)
save_j(latest_coin_posts, 'latest_coin_post.json')
save_csv(lcp, 'latest_coin_posts.csv')

# get reddit/tweets/articles in a single combined feed for NEO(sorted by time)
top_coin_feed = api.getTopFeedByCoin("bitcoin")
tcf = format_df(top_coin_feed)
save_j(top_coin_feed, 'top_coin_feed.json')
save_csv(tcf, 'top_coin_feed.csv')

# get a combined feed (reddit/tweets/articles) for a particular coin
# (sorted by relevance)
latest_coin_feed = api.getLatestFeedByCoin('bitcoin')
lcf = format_df(latest_coin_feed)
save_j(latest_coin_feed, 'latest_coin_feed.json')
save_csv(lcf, 'latest_coin_feed.csv')

# get reddit/tweets/articles (seperated) for a particular coin (sorted by time)
top_coin_items = api.getTopItemsByCoin("bitcoin")
tci = format_df(top_coin_items)
save_j(top_coin_items, 'top_coin_items.json')
save_csv(lcf, 'top_coin_items.csv')

# get latest reddit/tweets/articles (seperated) for Litecoin(sorted by
# relevance)
latest_coin_items = api.getLatestItemsByCoin("litecoin")
lci = format_df(latest_coin_items)
save_j(latest_coin_items, 'latest_coin_items.json')
save_csv(lci, 'latest_coin_items.csv')

# get details (subreddits, twitter handles, description, links) for ethereum
coin_details = api.getCoinDetails("ethereum")
save_j(coin_details, 'coin_details.json')
