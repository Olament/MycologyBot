from io import BytesIO
from PIL import Image

def convert_to_jpg(data):
    with BytesIO() as new_data:
        image = Image.open(BytesIO(data))
        image = image.convert('RGB')
        image.save(new_data, 'jpg')
        return new_data



def is_valid_image_url(url):
    return url[-3:] == 'jpg' or url[-3:] == 'png'


def is_request(submission):
    return submission.link_flair_text == 'ID request' \
           or 'ID' in submission.title.upper() \
           or 'WHAT' in submission.title.upper()


def is_visited(comments):
    for comment in comments:
        if comment.author == 'Mycology_Bot':
            return True
    return False