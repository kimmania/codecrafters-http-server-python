from enum import Enum

class ContentType(Enum):
    NONE = 'none'
    TEXT_PLAIN = 'text/plain'
    TEXT_HTML = 'text/html'
    TEXT_CSS = 'text/css'
    TEXT_JAVASCRIPT = 'text/javascript'
    IMAGE_PNG = 'image/png'
    IMAGE_JPEG = 'image/jpeg'
    IMAGE_GIF = 'image/gif'
    APPLICATION_JSON = 'application/json'
    APPLICATION_XML = 'application/xml'
    APPLICATION_PDF = 'application/pdf'
    APPLICATION_ZIP = 'application/zip'
    APPLICATION_OCTET_STREAM = 'application/octet-stream'
