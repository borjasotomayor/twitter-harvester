# twitter-harvester

A simple command-line tool to harvest tweets.

## Installing

Clone the repository and run:

    pip3 install .

## Setup

You will need to have Twitter Developer account, and create an App under your account.

Once you do so, create a file named `.twitter-harvester.conf` with the following:

    app_name: NAME_OF_YOUR_APP
    consumer-key: YOUR_CONSUMER_KEY
    consumer-secret: YOUR_CONSUMER SECRET

The consumer key and secret can be found in the "Keys and tokens" tab of your app.

Once you create this file, you will be able to run the `twitter-harvester` command
in the directory that contains the `.twitter-harvester.conf` file.

## Usage

    Usage: twitter-harvester [OPTIONS]

      Harvests tweets from the Twitter public stream, or from a specified list
      of user accounts.

    Options:
      -c, --config FILENAME           Configuration file.
      -n, --num-tweets INTEGER        Number of tweets to harvest. Set to 0 to
                                      keep harvesting until the program is stopped
                                      explicitly.
      -o, --outfile TEXT
      --format [text-only|human-readable|json]
      -u, --user TEXT                 Fetch all the tweets from this user.
      --users-file FILENAME           Only fetch tweets from users specified in
                                      this file (one per line). The number of
                                      tweets per account is specified with the -n
                                      parameter.
      -f, --filter TEXT               Filter stream by keywords (comma-separated
                                      list)
      --filters-file FILENAME         Filter according to the keywords specified
                                      in this file (one per line).

## Examples

Print tweets from the public stream (press Ctrl-C to stop):

    twitter-harvester

Print tweets from the public stream that include the keyword `coffee` (press Ctrl-C to stop):

    twitter-harvester -f coffee

Print ten tweets from the public stream:

    twitter-harvester -n 10

Print 100 tweets from user @borjasotomayor:

    twitter-harvester -n 100 -u borjasotomayor

Same as above, but producing JSON output:

    twitter-harvester -n 100 -u borjasotomayor --format json

Same as above, but saving the output to a file:

    twitter-harvester -n 100 -u borjasotomayor --format json -o tweets.json

