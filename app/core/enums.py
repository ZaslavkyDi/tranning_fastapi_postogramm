from enum import Enum


class EmailMimeTypeEnum(str, Enum):
    plain = 'plain'
    html = 'html'
