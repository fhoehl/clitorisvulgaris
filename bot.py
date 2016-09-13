#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Twitter bot"""

import argparse
from os import environ
from sys import stderr

from twython import Twython

try:
    CONSUMER_KEY = environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = environ['TWITTER_CONSUMER_SECRET']
    ACCESS_TOKEN = environ['TWITTER_ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = environ['TWITTER_ACCESS_TOKEN_SECRET']
except KeyError:
    print('Please set the environment variables for connecting to Twitter:',
          'TWITTER_CONSUMER_KEY', 'TWITTER_CONSUMER_SECRET',
          'TWITTER_ACCESS_TOKEN', 'TWITTER_ACCESS_TOKEN_SECRET',
          file=stderr)
    exit(1)


twitter_client = Twython(app_key=CONSUMER_KEY,
                         app_secret=CONSUMER_SECRET,
                         oauth_token=ACCESS_TOKEN,
                         oauth_token_secret=ACCESS_TOKEN_SECRET)


def get_adjective():
    """Returns an adjective from the words.txt list."""

    with open("latin_adjectives.txt", "r") as words_file:
        words = words_file.readlines()
        count = 0

        try:
            count_file = open(".tweetcount", "r+")
            try:
                count = int(count_file.read().strip()) + 1
            except ValueError:
                pass
        except FileNotFoundError:
            count_file = open(".tweetcount", "w")

        adjective = words[count % len(words)]

        count_file.seek(0)
        count_file.write(str(count))
        count_file.close()

        return adjective


def upload_image(image_path):
    """Upload image at image_path"""

    with open(image_path, 'rb') as image_file:
        response = twitter_client.upload_media(media=image_file)
        return response['media_id_string']
    return None


def tweet(status, image_path):
    """Tweet!"""

    media_id = upload_image(image_path)

    response = twitter_client.update_status(status=status,
                                            media_ids=[media_id])

    return response


def main():
    """Main"""

    parser = argparse.ArgumentParser(description="Tweet a clitoris")
    parser.add_argument('image_path', help='Image file path')
    args = parser.parse_args()

    name_of_the_day = "Clitoris %s" % get_adjective()

    tweet(name_of_the_day, args.image_path)


if __name__ == "__main__":
    main()
