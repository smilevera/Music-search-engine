import json
import logging
import urllib
import urllib2
import logging
import os.path
import sys

import StringIO
import gzip



logger = logging.getLogger('listenone.' + __name__)
def caesar(location):
    num = int(location[0])
    avg_len = int(len(location[1:]) / num)
    remainder = int(len(location[1:]) % num)
    result = [
        location[i * (avg_len + 1) + 1: (i + 1) * (avg_len + 1) + 1]
        for i in range(remainder)]
    result.extend(
        [
            location[(avg_len + 1) * remainder:]
            [i * avg_len + 1: (i + 1) * avg_len + 1]
            for i in range(num - remainder)])
    url = urllib.unquote(
        ''.join([
            ''.join([result[j][i] for j in range(num)])
            for i in range(avg_len)
        ]) +
        ''.join([result[r][-1] for r in range(remainder)])).replace('^', '0')
    return url
def h(
        url, v=None, progress=False, extra_headers={},
        post_handler=None, return_post=False):
    '''
    base http request
    progress: show progress information
    need_auth: need douban account login
    '''
    logger.debug('fetching url:' + url)
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) ' + \
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86' + \
        ' Safari/537.36'
    headers = {'User-Agent': user_agent}
    headers.update(extra_headers)

    data = urllib.urlencode(v) if v else None
    req = urllib2.Request(url, data, headers)
    response = urllib2.urlopen(req)
    if progress:
        result = chunk_read(response, report_hook=chunk_report)
    else:
        result = response.read()
    if response.info().get('Content-Encoding') == 'gzip':
        buf = StringIO.StringIO(result)
        f = gzip.GzipFile(fileobj=buf)
        result = f.read()
    if post_handler:
        post_result = post_handler(response, result)
        if return_post:
            return post_result
    return result

song_id=3381901
url = 'http://www.xiami.com/song/playlist/id/%s' % song_id + \
        '/object_name/default/object_id/0/cat/json'
response = h(url)
secret = json.loads(response)['data']['trackList'][0]['location']
ourl = caesar(secret)
print(ourl)
