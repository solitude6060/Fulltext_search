# -*- coding: utf-8 -*-

import got3 as got
import json

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)

	# Example 1 - Get tweets by username
	tweetCriteria = got.manager.TweetCriteria().setUsername('barackobama').setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 1 - Get tweets by username [barackobama]", tweet)

	# Example 2 - Get tweets by query search
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('europe refugees').setSince("2015-05-01").setUntil("2015-09-30").setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 2 - Get tweets by query search [europe refugees]", tweet)

	# Example 3 - Get tweets by username and bound dates
	tweetCriteria = got.manager.TweetCriteria().setUsername("barackobama").setSince("2015-09-10").setUntil("2015-09-12").setMaxTweets(1)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]

	printTweet("### Example 3 - Get tweets by username and bound dates [barackobama, '2015-09-10', '2015-09-12']", tweet)

if __name__ == '__main__':
	tweets_list = []

	def toJson(t):
		tweets_dict = {}
		tweets_dict['text'] = t.text
		return tweets_dict


	def printTweet(descr, t):
		print(descr)
		print("ID: %s" % t.id)
		print("Username: %s" % t.username)
		print("Author ID: %s" % t.author_id)
		print("Text: %s" % t.text)
		print("Pictures: {}".format(", ".join(t.pics)))
		print("Mentions: {}".format(", ".join(t.mentions)))
		print("Hashtags: {}".format(" ".join(t.hashtags)))
		print("Urls: {}".format(", ".join(t.urls)))
		print("date: %s" % t.date.strftime('%Y-%m-%d %H:%M:%S'))
		print("formatted_date: {}".format(t.formatted_date))
		print("retweets: {}({})".format(t.retweets, type(t.retweets)))
		print("favorites: {}".format(t.favorites))
		print("geo: {}({})".format(t.geo, type(t.geo)))
		print("author_id: {}".format(t.author_id))

	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#syphilis').setLang('en').setSince("2001-01-01").setUntil("2018-01-01").setMaxTweets(17000)
	tweets = got.manager.TweetManager.getTweets(tweetCriteria)

	print('### Get tweets by query search [#joy lang:en 20161115]')
	for i, tweet in enumerate(tweets):
		tweets_dict = toJson(tweet)
		tweets_list.append(tweets_dict)

	with open('tweet_syphilis.json', 'w') as outfile:
		json.dump(tweets_list, outfile)
		#print(tweets_list)
