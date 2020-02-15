from io import BytesIO


def convertToJpeg(im):
    with BytesIO() as f:
        im.save(f, format='JPEG')
        return f.getvalue()


def is_valid_image_url(url):
    return url[-3:] == 'jpg'


def is_request(submission):
    return submission.link_flair_text == 'ID request' \
           or 'ID' in submission.title.upper() \
           or 'WHAT' in submission.title.upper()


def is_visited(comments):
    for comment in comments:
        if comment.author == 'Mycology_Bot':
            return True
    return False