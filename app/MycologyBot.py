import praw
import requests
import json
import logging
import time
from datetime import datetime, timedelta

from utils import utils, imgur

logger = logging.getLogger()  # global logger
imgurURL = imgur.ImgurURL() # parser that convert imgur url to image link


def main():
    # init reddit bot from praw.ini
    reddit = praw.Reddit('mycology', user_agent='MycologyBot by /u/flyelement')
    subreddit = reddit.subreddit('Mycology')

    # init logging
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)-8s] %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # submission, comment, and own_comment stream
    # comment_stream = subreddit.stream.comments(pause_after=-1)
    submission_stream = subreddit.stream.submissions(pause_after=-1, skip_existing=True)

    while True:
        logger.info('**** START check submission stream ****')
        for submission in submission_stream:
            if submission is None:
                break
            process_submission(submission)
        logger.info('**** END check submission stream ****')

        logger.info('**** START check bot own comment ****')
        for comment in reddit.user.me().comments.new(limit=20):
            check_own_comment(comment)
        logger.info('**** END check bot own comment ****')

        time.sleep(60) # idie

    # submission = reddit.submission(url='https://www.reddit.com/r/test/comments/ex8ly2/id/')
    # process_submission(submission)


def process_submission(submission):
    logger.info('[{}] New post title: {}'.format(submission.id, submission.title))
    logger.info('[{}] post link: {}'.format(submission.id, submission.permalink))
    logger.info('[{}] url link: {}'.format(submission.id, submission.url))

    # retrieve image url
    image_url = ""
    logger.info("[{}] Attempt to retrieve image url".format(submission.id))
    if utils.is_valid_image_url(submission.url):
        image_url = submission.url
        logger.info("[{}] Retrieved regular post image url".format(submission.id))
    elif 'imgur' in submission.url:
        try:
            image_url = imgurURL.get_imgur_urls(submission.url)[0] # only get the first pictures
            logger.info("[{}] Retrieved imgur post image url".format(submission.id))
        except Exception as e:
            logger.exception("[{}] Failed to parse imgur url".format(submission.id))
            return
    else:
        logger.info('[{}] Skip the post since it does not contain image'.format(submission.id))
        return
    logger.info("[{}] image link: {}".format(submission.id, image_url))

    # skip if post is not tagged with "ID Request"
    if not utils.is_request(submission):
        logger.info('[{}] Skip the post since it is not an ID request'.format(submission.id))
        return

    # skip if visited this post before
    if utils.is_visited(submission.comments):
        logger.info('[{}] Skip the post since replied before'.format(submission.id))
        return

    response = requests.get(image_url)
    if not response.headers["Content-Type"].startswith("image/"):
        logging.warning('[{}] Cannot retrieve image from url'.format(submission.id))
        return
    data = response.content
    logger.info('[{}] Image retrieved!'.format(submission.id))

    data = utils.convert_to_jpg(data)  # convert png to jpg since png crash the server

    result = get_classify(data)
    if result:
        logger.info('[{}] Prediction: '.format(submission.id) + str(result))
        reply_post(submission, result)
    else:
        logger.error('[{}] Failed to retrieve prediction from server'.format(submission.id))


def check_own_comment(comment):
    # delete the comment if it has negative score and has been some time
    if comment.score <= -1 and datetime.utcfromtimestamp(comment.created_utc) < datetime.utcnow() - timedelta(hours=1):
        logger.info("[{}] Delete comment since low score".format(comment.id))
        logger.info("[{}] Delete from post: {}".format(comment.id, comment.submission.permalink))
        logger.info("[{}] Deleted content: {}".format(comment.id, comment.body.replace('\n', ' ')))
        comment.delete()


def get_classify(data):
    # get prediction from Deepmushroom-docker
    response = requests.post('http://107.175.147.28:5000/predict', files={
        'file': ('img.jpg', data, 'image/jpg')
    })

    # error handling
    if response.status_code != 200:
        return None

    return json.loads(response.text)


def reply_post(submission, result):
    # no need to reply with low confident prediction
    if float(result[0]['probability']) < 0.40:
        logger.info('[{}] Do not reply due to low prediction confidence'.format(submission.id))
        return

    comment = "These are the Top-5 predictions given by AI.\n\n"
    comment += "Species | Probability\n:--|:--\n"
    for res in result:
        comment += "*{}*|{}\n".format(res['class_name'], res['probability'])

    comment += "\nDisclaimer: This bot is not in any way affiliated with r/mycology or the mod team. The prediction given by this bot **is not 100% accurate** and you should not use this information to determine the edibility of mushroom.\n"
    comment += "\n***\n"
    comment += "^^MycologyBot{0}power{0}by{0}[DeepMushroom](https://github.com/Olament/DeepMushroom){0}API{0}|{0}[GitHub](https://github.com/Olament/MycologyBot)\n\n".format("&#32;")

    try:
        submission.reply(comment)
    except Exception as e:
        logger.error(traceback.format_exc())
        return

    logger.info("[{}] Comment submitted!".format(submission.id))


if __name__ == "__main__":
    main()
