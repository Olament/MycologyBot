import praw
import requests
import json
import logging
import traceback

logger = logging.getLogger()

def main():
    # init reddit bot from praw.ini
    reddit = praw.Reddit('mycology', user_agent='MycologyBot by /u/flyelement')
    subreddit = reddit.subreddit('Mycology')

    # init logging
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # submission = reddit.submission(url='https://www.reddit.com/r/mycology/comments/ex3kpv/can_anyone_help_me_id_qld_australia/')
    # process_submission(submission)

    # process submission with depp mushroom API
    for submission in subreddit.stream.submissions():
        process_submission(submission)


def process_submission(submission):
    logger.info('New post title: {}'.format(submission.title))
    logger.info('post url: {}'.format(submission.url))

    # skip post w/o image
    if submission.is_self or not is_valid_image_url(submission.url):
        logger.info('Skip the post since it does not contain image')
        return

    # skip if post is not tagged with "ID Request"
    if submission.link_flair_text != 'ID request':
        logger.info('Skip the post since it does not have \'ID Request\' flair')
        return

    response = requests.get(submission.url)
    if not response.headers["Content-Type"].startswith("image/"):
        logging.warning('Cannot retrieve image from url')
        return
    data = response.content
    logger.info('Image retrieved!')
    result = get_classify(data)
    logger.info('Prediction: ' + str(result))
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
    # no need to reply with low confident prediction
    if float(result[0]['probability']) < 0.20:
        logger.info('Do not reply due to low prediction confidence')
        return

    comment = "These are the Top-5 predictions given by AI.\n\n"
    comment += "Species | Probability\n:--|:--\n"
    for res in result:
        comment += "*{}*|{}\n".format(res['class_name'], res['probability'])

    comment += "\n***\n"
    comment += "^^MycologyBot{0}empowered{0}by{0}[DeepMushroom](https://github.com/Olament/DeepMushroom){0}API{0}|{0}[GitHub](https://github.com/Olament/MycologyBot)\n\n".format("&#32;")

    # try:
    #     submission.reply(comment)
    # except Exception as e::
    #     logger.error(traceback.format_exc())


if __name__ == "__main__":
    main()