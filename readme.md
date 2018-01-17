# Telegraph

[![Documentation Status](https://readthedocs.org/projects/telegraph/badge/?version=latest)](http://telegraph.readthedocs.io/en/latest/?badge=latest)

### Python wrapper for the Telegraph blogging service provided by Telegram

Requires Python 3.

### Documentation

The docs are hosted on [RTD](http://telegraph.readthedocs.io/en/latest/).

### Install

`pip install git+https://github.com/jacoduplessis/telegraph`

### Usage

```python
from telegraph import Telegraph

telegraph = Telegraph('<access_token>')

# Get Pages
pages = telegraph.get_page_list()

# Create Page
page = telegraph.create_page(title="New Page", content=['Lorem Ipsum'])
```

### Utilities

Two helper functions are included to render page content and serialize html into the required format.

First install the required dependencies:

`pip install beautifulsoup4 bleach`

```python
from telegraph import Telegraph
from telegraph.utils import content_to_html, html_to_content

telegraph = Telegraph('<access_token>')

# rendering page content as html
page = telegraph.get_page('path')
html = content_to_html(page.content)

# creating a page from html string
html_string = '<p>Hallo, World!</p>'
content = html_to_content(html_string)
telegraph.create_page(title="Test", content=content)

```

### Tests

`python -m unittest discover tests`
