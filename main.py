import requests

from flask import Flask, request, Response
from google.appengine.api import memcache
from hashlib import sha1

app = Flask(__name__)

RDB_TOKEN = 'ohsnap'
# Number of requests an ip address can hit per minute, not a moving window
MINUTE_LIMIT = 30
# Dont put this in source control! KEEP IT HIDDEN FOREVER
PARSER_URL = 'https://www.readability.com/api/content/v1/parser?token=%s&url={url}' % RDB_TOKEN


@app.route('/')
def proxy_rdb():
    num_hits = memcache.get(request.remote_addr) or 0
    if num_hits > MINUTE_LIMIT:
        return 'Too many requests', 429

    memcache.set(request.remote_addr, num_hits + 1, time=60)

    url = request.args.get('url')
    callback = request.args.get('callback')

    if url is None:
        return 'No `url` to parse', 400

    url_hash = sha1(url).hexdigest()

    content = memcache.get(url_hash)

    if not content:
        response = requests.get(PARSER_URL.format(url=url))
        content = response.content
        memcache.set(url_hash, content)

    mimetype = 'application/json'
    if callback:
        content =  '{callback}({content})'.format(
            callback=callback, content=content)
        mimetype = 'application/javascript'

    return Response(content, mimetype=mimetype, status=200)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error:\n{}'.format(e), 500
