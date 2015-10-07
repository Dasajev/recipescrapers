import requests


def getUrl(url, nocache=False, params=None, headers=None, cookies=None):
    """Gets data, bs and headers for the given url,
    using the internal cache if necessary"""

    browser = """Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11
    (KHTML, like Gecko) Chrome/23.0.1271.95 Safari/537.11"""
    # Common session for all requests
    s = requests.session()
    s.verify = False
    s.stream = True  # Don't fetch content unless asked
    s.headers.update({'User-Agent': browser})
    # Custom headers from requester
    if headers:
        s.headers.update(headers)
    # Custom cookies from requester
    if cookies:
        s.cookies.update(cookies)

    try:
        r = s.get(url, params=params)
    except requests.exceptions.InvalidSchema:
        print("Invalid schema in URI: %s" % url)
        return None
    except requests.exceptions.ConnectionError:
        print("Connection error when connecting to %s" % url)
        return None

    size = int(r.headers.get('Content-Length', 0)) // 1024
    if size > 2048:
        print("Content too large, will not fetch: %skB %s" % (size, url))
        return None

    return r


def split_amounts_and_ingredients(raw_data):
    parsed = []
    for item in raw_data:
        if ')' in item:
            amount, item = item.split(')')
            parsed.append({'ingredient':item.strip(), 'amount':amount+(')').strip()})
        else:
            amount, item = item.split('  ')
            parsed.append({'ingredient':item.strip(), 'amount':amount.strip()})

    return parsed
