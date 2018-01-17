from unittest import TestCase, main
from telegraph.utils import content_to_html, html_to_content
from fixtures import CONTENT, HTML


class TestUtils(TestCase):

    def test_content_to_html(self):
        html = content_to_html(CONTENT)
        self.assertEqual(html, HTML)

    def test_html_to_content(self):
        content = html_to_content(HTML)
        self.assertEqual(content, CONTENT)


if __name__ == '__main__':
    main()
