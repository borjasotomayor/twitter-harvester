# -*- coding: utf-8 -*-

import argparse
import twitter
import click
import json
import yaml
import os
import os.path
import signal
import sys
import codecs
import locale

# From https://wiki.python.org/moin/PrintFails
# Otherwise, piping output fails
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout) 

VERSION = "0.9"
RELEASE = "0.9.0"

USER_DIR = os.path.expanduser("~/.twitter-harvester")

CONFIG_FILES = [ "/etc/twitter-harvester.conf",
                USER_DIR + "/config",
                "./.twitter-harvester.conf"]

USER_CREDENTIALS = USER_DIR + "/credentials"

CONFIG_FIELDS = ["app-name",
                 "consumer-key",
                 "consumer-secret"]

outf = None

def error(msg):
    print msg
    sys.exit(1)

def signal_handler(signal, frame):
        global outfile
        if outf != sys.stdout: outf.close()
        print('You pressed Ctrl+C!')
        sys.exit(0)

def load_configuration(config_file):
    '''
    Load configuration options. First, load the values specified in 
    each file in CONFIG_FILES (with values in one file overriding any
    values specified in the previous one). Next, load the values in
    config_file (which could be None)
    '''
    
    config = {}
    
    files = CONFIG_FILES
    if config_file is not None:
        files.append(config_file)
    
    for fname in files:
        if os.path.exists(fname):
            with open(fname) as f:
                fconf = yaml.load(f)
                if not isinstance(fconf, dict):
                    error("File {} is not a valid configuration file".format(fname))
                else:
                    keys = fconf.keys()
                    for k in keys:
                        if k not in CONFIG_FIELDS:
                            error("File {} contains an invalid field: {}".format(fname, k))
                    config.update(fconf)
            
    return config
        

def save_tweet(tweet, f, format):
    # Replace HTML entities
    tweet["text"] = tweet["text"].replace("&gt;", ">").replace("&lt;", "<").replace("&amp;", "&")

    if format == "text-only":
        print >>f, tweet["text"]
    elif format == "human-readable":
        print >>f, u">>> {} (@{}) - {}".format(tweet["user"]["name"], tweet["user"]["screen_name"], tweet["created_at"])
        print >>f, u"{}".format(tweet["text"])
        print >>f, ""        
    elif format == "json":
        print >>f, json.dumps(tweet)


@click.command(name="twitter-harvester")
@click.option('-c', '--config', type=click.File('r'),
              help="Configuration file.")
@click.option('-n', '--num-tweets', type=int, default=0,
              help="Number of tweets to harvest. Set to 0 to keep harvesting until the program is stopped explicitly.")
@click.option('-o', '--outfile', type=str, default="-")
@click.option('--format',  type=click.Choice(['text-only', 'human-readable', 'json']), default="human-readable")
@click.option('-u', '--user', type=str,
              help="Fetch all the tweets from this user.")
@click.option('--users-file', type=click.File('r'),
              help='Only fetch tweets from users specified in this file (one per line). The number of tweets per account is specified with the -n parameter.')
@click.option('-f', '--filter', type=str,
              help='Filter stream by keywords (comma-separated list)')
@click.option('--filters-file', type=click.File('r'),
              help='Filter according to the keywords specified in this file (one per line).')
def cmd(config, num_tweets, outfile, format, user, users_file, filter, filters_file):
    ''' 
    TODO: documentation
    '''
    
    if not os.path.exists(USER_DIR):
        os.mkdir(USER_DIR, 0700)
    
    config = load_configuration(config)

    if not ("app-name" in config and "consumer-key" in config and "consumer-secret" in config):
        error("Configuration files do not have OAuth fields ('app-name', 'consumer-key', 'consumer-secret')")
        
    if not os.path.exists(USER_CREDENTIALS):
        twitter.oauth_dance(config["app-name"], 
                            config["consumer-key"], 
                            config["consumer-secret"], 
                            USER_CREDENTIALS)        
    
    oauth_token, oauth_secret = twitter.read_token_file(USER_CREDENTIALS)
    
    auth = twitter.OAuth(oauth_token, oauth_secret, config["consumer-key"], config["consumer-secret"])
    
    global outf
    if outfile == "-":
        outf = sys.stdout
    else:
        outf = open(outfile, "w")
        
    if num_tweets == 0:
        num_tweets_str = "all"
    else:
        num_tweets_str = `num_tweets`
        
    if user is not None or users_file is not None:
        t = twitter.Twitter(auth=auth)
    
        if user is not None:
            users = [user]
        elif users_file is not None:
            users = users_file.read().strip().replace("@", "").split()
            
        for user in users:
            if outf != sys.stdout: print "Fetching %i tweets from @%s" % (num_tweets_str, user)
            tweets = t.statuses.user_timeline(screen_name=user, count=num_tweets)   
            if outf != sys.stdout: print "  (actually fetched %i)" % len(tweets)    
            for tweet in tweets:
                save_tweet(tweet, outf, format)
    else:
        # Connect to the stream
        twitter_stream = twitter.TwitterStream(auth=auth)
    
        if filter is None and filters_file is None:
            stream = twitter_stream.statuses.sample()
        else:
            if filter is not None:
                track = filter
            elif filters_file is not None:
                track = ",".join(filters_file.read().strip().split())
            
            stream = twitter_stream.statuses.filter(track=track)
    
        # Fetch the tweets
        fetched = 0
    
        if num_tweets > 0:
            if outf != sys.stdout: print "Fetching %i tweets... " % num_tweets
        else:
            signal.signal(signal.SIGINT, signal_handler)
            if outf != sys.stdout: print "Fetching tweets. Press Ctrl+C to stop."
    
        for tweet in stream:
            # The public stream includes tweets, but also other messages, such
            # as deletion notices. We are only interested in the tweets.
            # See: https://dev.twitter.com/streaming/overview/messages-types
            if tweet.has_key("text"):
                # We also only want English tweets
                if tweet["lang"] == "en":
                    save_tweet(tweet, outf, format)
                    fetched += 1
                    if fetched % 100 == 0:
                        if outf != sys.stdout: print "Fetched %i tweets." % fetched
                    if num_tweets > 0 and fetched >= num_tweets:
                        break
    
    if outf != sys.stdout: outfile.close()

