from pybooru.pybooru import _Pybooru

class _Altbooru(_Pybooru):
    def __init__(self, site_name='', site_url='', username=''):
        super(_Altbooru, self).__init__(site_name, site_url, username)

    def post_list(self, **params):
        return self._get('post', params)

    def _build_url(self):
        return "{0}/index.php?page=dapi&s=post&q=index".format(self.site_url)

    def get_image_url(self, post):
        return ""

    def _get(self, api_method, params, method='GET'):
        url = self._build_url()
        params['json'] = 1
        if 'page' in params:
            params['pid'] = params.pop('page', None)

        request_args = {'params': params}

        # Do call
        return self._request(url, api_method, request_args, method)

class Gelbooru(_Altbooru):
    def __init__(self, username=''):
        super(Gelbooru, self).__init__('', 'http://gelbooru.com', username)

    def get_image_url(self, post):
        return post["file_url"]

class Safebooru(_Altbooru):
    def __init__(self, username=''):
        super(Safebooru, self).__init__('', 'http://safebooru.org', username)

    def get_image_url(self, post):
        return "{0}/images/{1}/{2}".format(self.site_url, post["directory"], post["image"])