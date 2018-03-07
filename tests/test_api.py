from unittest import TestCase, main

from telegraph import Telegraph
from fixtures import CONTENT


class TestAPI(TestCase):

    def setUp(self):
        self.t = Telegraph('d676e590b0c6bac0ea58cfcdd350272691ea9fb10b2aeb33edcf68dbb20d')

    def tearDown(self):
        self.t.close()

    def test_get_page(self):
        page = self.t.get_page('api')
        self.assertEqual(page.title, 'Telegraph API')

    def test_create_page(self):
        page = self.t.create_page(
            title="Test Page",
            return_content=True,
            content=CONTENT
        )
        self.assertEqual(page.content, CONTENT)


if __name__ == '__main__':
    main()