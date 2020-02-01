import praw
import requests
import json


def main():
    # init reddit bot from praw.ini
    reddit = praw.Reddit('mycology', user_agent='MycologyBot (by /u/flyelement)')
    subreddit = reddit.subreddit('Mycology')

    # process submission with depp mushroom API
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    # skip post w/o image
    if submission.is_self or not is_valid_image_url(submission.url):
        return

    # skip if post is not tagged with "ID Request"
    if submission.link_flair_text != 'ID request':
        return

    response = requests.get(submission.url)
    if not response.headers["Content-Type"].startswith("image/"):
        return
    data = response.content
    result = get_classify(data)
    reply_post(submission, result)


def get_classify(data):
    # get prediction from Deepmushroom-docker
    response = requests.post('http://107.175.147.28:5000/predict', files={
        'file': ('img.jpg', data, 'image/jpg')
    })
    return json.loads(response.text)


def is_valid_image_url(url):
    return url[-3:] == 'jpg'


def reply_post(submission, result):
    return


if __name__ == "__main__":
    main()