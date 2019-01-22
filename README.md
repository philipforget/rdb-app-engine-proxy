# Archived #

# Readability app-engine content proxy

A simple, memcached based throttling proxy for Readability's content API which can run on google app engine.

This runs on google app engine. It's also easy to run locally. You will need to have the ol' [python app engine](https://developers.google.com/appengine/) runtime installed.

A sample is up at http://sample-rdb-proxy.appspot.com/

There is only one endpoint, `/` , which proxies requests to the readability content parser. There is one required parameter, `url` which must be a nicely encoded url e.g. http%3A%2F%2Fpaulgraham.com%2Fambitious.html%3Fsee_this_is%3Descaped.

The second optional parameter is `callback` which lets you use this across domains using jsonp. Calls will be returned with content-type `application/javascript` if this parameter is passed and content will return like so:

```javascript
callback_value({...})
```

otherwise content will be returned as `application/json`.

## Configuration

Configuration is done in main.py. Two config variables can be set:

* RDB_TOKEN: Your Readability content api token (do not check this into a public repo!)
* MINUTE_LIMIT: The number of requests, per minute, to allow. This is alimit based on the ip of the requesting user.

## Examples
Just proxy the content for one article and return the response: http://sample-rdb-proxy.appspot.com/?url=http://paulgraham.com/ambitious.html

Make a request for jsonp: http://sample-rdb-proxy.appspot.com/?url=http://paulgraham.com/ambitious.html&callback=some_function_name

Make a request with a url that has url params (see how it's escaped?): http://sample-rdb-proxy.appspot.com/?url=http%3A%2F%2Fpaulgraham.com%2Fambitious.html%3Fsorry_for_spamming_your_server_paul
