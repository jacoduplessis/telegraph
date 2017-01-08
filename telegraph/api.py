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
        return "<Telegraph Page: {} ({})".format(self.title, self.path)


class Telegraph:
    def __init__(self, token=None):

        self.token = token

    def _request(self, method, **kwargs):

        base_url = 'https://api.telegra.ph/'

        if method != 'createAccount':
            kwargs.update({'access_token': self.token})

        url = base_url + method
        logger.debug("Making request to {}, with params {}".format(url, kwargs))

        r = requests.post(url, json=kwargs)
        r.raise_for_status()
        response = r.json()
        if not response['ok']:
            raise TelegraphException(response['error'])
        return r.json()

    def create_account(self, short_name, author_name=None, author_url=None):
        """
        Use this method to create a new Telegraph account.

        See `<http://telegra.ph/api#getPageList>`_.

        :param short_name: Required. Account name, helps users with several accounts remember
            which they are currently using. Displayed to the user above the "Edit/Publish" button on Telegra.ph,
            other users don't see this name.
        :param author_name: Default author name used when creating new articles.
        :param author_url: Default profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :return: Dict containing account fields as well as ``access_token``.
        """
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }
        return self._request('createAccount', **params)

    def edit_account_info(self, short_name=None, author_name=None, author_url=None):
        """
        Use this method to get information about a Telegraph account.

        See `<http://telegra.ph/api#editAccountInfo>`_.

        :param short_name: New account name.
        :param author_name: New default author name used when creating new articles.
        :param author_url: New default profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :return: A dict representing an Account with the default fields.
        """
        pass

    def get_account_info(self, fields=None):
        """
        Use this method to get information about a Telegraph account.

        See `<http://telegra.ph/api#editAccountInfo>`_.

        :param fields: List of account fields to return.
            Available fields: ``short_name``, ``author_name``, ``author_url``, ``auth_url``, ``page_count``.
            Default is ``["short_name", "author_name", "author_url"]``.
        :return: A dict with the Account info.
        """
        if fields is None:
            fields = ['short_name', 'author_name', 'author_url']
        elif fields == 'all':
            fields = ['short_name', 'author_name', 'author_url', 'auth_url', 'page_count']
        params = dict(fields=fields)
        return self._request('getAccountInfo', **params)

    def revoke_access_token(self):
        """
        Use this method to revoke access_token and generate a new one, for example,
            if the user would like to reset all connected sessions,
            or you have reasons to believe the token was compromised.

        See `<http://telegra.ph/api#revokeAccessToken>`_.

        :return:
        """
        pass

    def create_page(self, title, content=None, author_name=None, author_url=None, return_content=False):
        """
        Use this method to create a new Telegraph page.

        See `<http://telegra.ph/api#createPage>`_.

        :param title: Required. Page title.
        :param content: Required. Content of the page.
        :param author_name: Author name, displayed below the article's title.
        :param author_url: Profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :param return_content: If true, a content field will be returned in the Page object.
        :return: A Page object.
        """
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
        """
        Use this method to edit an existing Telegraph page.

        See `<http://telegra.ph/api#editPage>`_.

        :param path: Required. Path to the page.
        :param title: Required. Page title.
        :param content: Required. Content of the page.
        :param author_name: Author name, displayed below the article's title.
        :param author_url: Profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :param return_content: If true, a content field will be returned in the Page object.
        :return: A Page object.
        """
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
        """
        Use this method to get a Telegraph page.

        See `<http://telegra.ph/api#getPage>`_.

        :param path: Required. Path to the Telegraph page (in the format Title-12-31,
            i.e. everything that comes after http://telegra.ph/).
        :param return_content: If true, content field will be returned in Page object. Default is ``False``.
        :return: A Page object.
        """
        params = dict(path=path, return_content=return_content)
        result = self._request('getPage', **params).get('result')
        page = Page(**result)
        return page

    def get_page_list(self, offset=0, limit=50):
        """
        Use this method to get a list of pages belonging to a Telegraph account.

        See `<http://telegra.ph/api#getPageList>`_.

        :param offset: Sequential number of the first page to be returned. Default is 0.
        :param limit: Limits the number of pages to be retrieved. Default is 50.
        :return: Dict with two keys: ``total_count`` with the total number of pages beloning to the account,
            and ``pages`` that is a list of ``Page`` objects.
        """
        params = dict(offset=offset, limit=limit)
        result = self._request('getPageList', **params).get('result')
        pages = [Page(**page) for page in result['pages']]
        return dict(total_count=result['total_count'], pages=pages)

    def get_views(self, path, year=None, month=None, day=None, hour=None):
        """
        Use this method to get the number of views for a Telegraph article.

        See `<http://telegra.ph/api#getViews>`_.

        :param path: Required. Path to the Telegraph page
            (in the format ``Title-12-31``, where 12 is the month and 31 the day the article was first published).
        :param year: Required if month is passed.
            If passed, the number of page views for the requested year will be returned.
        :param month: Required if day is passed.
            If passed, the number of page views for the requested month will be returned.
        :param day: Required if hour is passed.
            If passed, the number of page views for the requested day will be returned.
        :param hour: If passed, the number of page views for the requested hour will be returned.
        :return: Dict with a single ``views`` key and an integer value.
            By default, the total number of page views will be returned.
        """
        params = {
            'path': path,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        return self._request('getViews', **params).get('result')
