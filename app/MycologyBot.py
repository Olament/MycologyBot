import praw

def main():
    # init reddit bot from praw.ini
    reddit = praw.Reddit('mycology', user_agent='MycologyBot (by /u/flyelement)')
    subreddit = reddit.subreddit('Mycology')

    # process submission with depp mushroom API
    for submission in subreddit.stream.submissions():
        process_submission(submission)

def process_submission(submission):
    print(submission.title)
    print(submission.url)

if __name__ == "__main__":
    main()