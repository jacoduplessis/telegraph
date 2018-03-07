import requests
from typing import List, Dict, Union

from .types import Account, Page, PageViews, PageList


class TelegraphException(Exception):
    pass


class Telegraph:
    def __init__(self, token=None):

        self.token = token
        self.session = requests.Session()

    def _request(self, method, **kwargs):

        base_url = 'https://api.telegra.ph/'

        if method != 'createAccount':
            if not self.token:
                raise TelegraphException("No Access Token provided for Telegraph instance.")
            kwargs.update({'access_token': self.token})

        url = base_url + method
        try:
            r = self.session.post(url, json=kwargs, timeout=5)
            r.raise_for_status()
        except requests.RequestException as e:
            raise Telegraph(f'Connection Error: {e}')
        response = r.json()
        if not response['ok']:
            raise TelegraphException(f'API Error: {response["error"]}')
        return response.get('result')

    def create_account(self, short_name, author_name=None, author_url=None, use=True):
        """
        Use this method to create a new Telegraph account.

        See `<http://telegra.ph/api#getPageList>`_.

        :param short_name: Required. Account name, helps users with several accounts remember
            which they are currently using. Displayed to the user above the "Edit/Publish" button on Telegra.ph,
            other users don't see this name.
        :param author_name: Default author name used when creating new articles.
        :param author_url: Default profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :param use: Whether to set the access token of the current instance to the new account. Default: True
        :return: An Account object.
        :rtype: Account
        """
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }

        data = self._request('createAccount', **params)
        account = Account(**data)
        if use:
            self.token = account.access_token
        return account

    def edit_account_info(self,
                          short_name=None,
                          author_name=None,
                          author_url=None) -> Account:
        """
        Use this method to get information about a Telegraph account.

        See `<http://telegra.ph/api#editAccountInfo>`_.

        :param short_name: New account name.
        :param author_name: New default author name used when creating new articles.
        :param author_url: New default profile link, opened when users click on the author's name below the title.
            Can be any link, not necessarily to a Telegram profile or channel.
        :return: An Account object.
        :rtype: Account
        """
        params = {
            'short_name': short_name,
            'author_name': author_name,
            'author_url': author_url
        }

        data = self._request('editAccountInfo', **params)
        account = Account(**data)
        return account

    def get_account_info(self,
                         fields: List[str] = None) -> Account:
        """
        Use this method to get information about a Telegraph account.

        See `<http://telegra.ph/api#editAccountInfo>`_.

        :param fields: List of account fields to return.
            Available fields: ``short_name``, ``author_name``, ``author_url``, ``auth_url``, ``page_count``.
            Default is ``["short_name", "author_name", "author_url"]``.
        :return: An Account object.
        :rtype: Account
        """
        if fields is None:
            fields = ['short_name', 'author_name', 'author_url']
        elif fields == 'all':
            fields = ['short_name', 'author_name', 'author_url', 'auth_url', 'page_count']
        params = dict(fields=fields)
        data = self._request('getAccountInfo', **params)
        account = Account(**data)
        return account

    def revoke_access_token(self) -> Account:
        """
        Use this method to revoke access_token and generate a new one, for example,
            if the user would like to reset all connected sessions,
            or you have reasons to believe the token was compromised.

        See `<http://telegra.ph/api#revokeAccessToken>`_.

        :return: An Account object with new ``access_token`` and ``auth_url`` fields.
        :rtype: Account
        """
        data = self._request('revokeAccessToken')
        account = Account(**data)
        return account

    def create_page(self,
                    title: str,
                    content: List[Union[Dict, str]] = None,
                    author_name: str = None,
                    author_url: str = None,
                    return_content: bool = False) -> Page:
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
        :rtype: Page
        """
        params = {
            'title': title,
            'content': content,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        }
        data = self._request('createPage', **params)
        page = Page(**data)
        return page

    def edit_page(self,
                  path: str,
                  title: str,
                  content: List[Union[Dict, str]],
                  author_name: str = None,
                  author_url: str = None,
                  return_content: bool = False) -> Page:
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
        :rtype: Page
        """
        params = {
            'path': path,
            'title': title,
            'content': content,
            'author_name': author_name,
            'author_url': author_url,
            'return_content': return_content
        }
        data = self._request('editPage', **params)
        page = Page(**data)
        return page

    def get_page(self,
                 path: str,
                 return_content=False) -> Page:
        """
        Use this method to get a Telegraph page.

        See `<http://telegra.ph/api#getPage>`_.

        :param path: Required. Path to the Telegraph page (in the format Title-12-31,
            i.e. everything that comes after ``http://telegra.ph/``).
        :param return_content: If true, content field will be returned in Page object. Default is ``False``.
        :return: A Page object.
        :rtype: Page
        """
        params = dict(path=path, return_content=return_content)
        data = self._request('getPage', **params)
        page = Page(**data)
        return page

    def get_page_list(self,
                      offset: int = 0,
                      limit: int = 50):
        """
        Use this method to get a list of pages belonging to a Telegraph account.

        See `<http://telegra.ph/api#getPageList>`_.

        :param offset: Sequential number of the first page to be returned. Default is 0.
        :param limit: Limits the number of pages to be retrieved. Default is 50.
        :return: A PageList object.
        :rtype: PageList
        """
        params = dict(offset=offset, limit=limit)
        data = self._request('getPageList', **params)
        total_count = data['total_count']
        pages = [Page(**page) for page in data['pages']]
        return PageList(pages=pages, total_count=total_count)

    def get_views(self,
                  path: str,
                  year: int = None,
                  month: int = None,
                  day: int = None,
                  hour: int = None) -> PageViews:
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
        :return: A PageViews object.
        :rtype: PageViews
        """
        params = {
            'path': path,
            'year': year,
            'month': month,
            'day': day,
            'hour': hour
        }
        data = self._request('getViews', **params)
        return PageViews(**data)

    def close(self):
        self.session.close()
