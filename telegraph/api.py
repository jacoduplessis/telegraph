import requests
import logging

logger = logging.getLogger('telegraph')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class TelegraphException(Exception):
    pass


class Page:
    def __init__(self, path='', url='', title='', description='', author_name='',
                 author_url='', views='', image_url=None, content=None, can_edit=None):
        self.path = path
        self.url = url
        self.title = title
        self.description = description
        self.author_name = author_name
        self.author_url = author_url
        self.image_url = image_url
        self.content = content
        self.views = views
        self.can_edit = can_edit

    def __str__(self):
        return f"<Telegraph Page: {self.title} ({self.path})"


class Telegraph:
    def __init__(self, token=None):

        self.token = token

    def _request(self, method, **kwargs):

        base_url = 'https://api.telegra.ph/'

        if method != 'createAccount':
            params = {
                'access_token': self.token,
                **kwargs
            }
        else:
            params = kwargs

        url = base_url + method
        logger.debug(f"Making request to {url}, with params f{params}")

        r = requests.post(url, json=params)
        r.raise_for_status()
        response = r.json()
        if not response['ok']:
            raise TelegraphException(response['error'])
        return r.json()

    def create_account(self, short_name, author_name=None, author_url=None):
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        return self._request('createAccount', **params)

    def edit_account_info(self, short_name=None, author_name=None, author_url=None):
        pass

    def get_account_info(self, fields=None):
        if fields is None:
            fields = ['short_name', 'author_name', 'author_url']
        elif fields == 'all':
            fields = ['short_name', 'author_name', 'author_url', 'auth_url', 'page_count']
        params = dict(fields=fields)
        return self._request('getAccountInfo', **params)

    def revoke_access_token(self):
        pass

    def create_page(self, title, content=None, author_name=None, author_url=None, return_content=False):
        params = {
            'title': title,
            'content': content or ['...'],
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        }
        result = self._request('createPage', **params).get('result')
        page = Page(**result)
        return page

    def edit_page(self, path, title, content, author_name=None, author_url=None, return_content=False):
        params = {
            'path': path,
            'title': title,
            'content': content,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        }
        result = self._request('editPage', **params).get('result')
        page = Page(**result)
        return page

    def get_page(self, path, return_content=False):
        params = dict(path=path, return_content=return_content)
        result = self._request('getPage', **params).get('result')
        page = Page(**result)
        return page

    def get_page_list(self, offset=0, limit=50):
        params = dict(offset=offset, limit=limit)
        result = self._request('getPageList', **params).get('result')
        pages = [Page(**page) for page in result['pages']]
        return dict(total_count=result['total_count'], pages=pages)

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        params = {
            'path': path,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        return self._request('getViews', **params).get('result')
