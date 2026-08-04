from urllib.parse import urlparse # разбивает URL на составляющие
from rest_framework.validators import ValidationError

VALID_YOUTUBE_NETLOC = ["youtube.com", "www.youtube.com", "youtu.be", "www.youtu.be"]

class YouTubeValidateVideoURL:
    """ Класс валидации прикрепляемых ссылок на видео уроков. """

    def __call__(self, value):
        """ Метод отвечающий за логику при вызове класса. """
        url = urlparse(value)

        if url.netloc not in VALID_YOUTUBE_NETLOC:
            raise ValidationError("Разрешены ссылки только на YouTube.")


