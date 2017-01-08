# Telegraph

[![Documentation Status](https://readthedocs.org/projects/telegraph/badge/?version=latest)](http://telegraph.readthedocs.io/en/latest/?badge=latest)

### Python wrapper for the Telegraph blogging service provided by Telegram

Requires Python 3.

### Documentation

The docs are hosted on [RTD](http://telegraph.readthedocs.io/en/latest/).

### Usage

```python
from telegraph import Telegraph

telegraph = Telegraph('<access_token>')

# Get Pages
pages = telegraph.get_page_list()

# Create Page
page = telegraph.create_page(title="New Page", content=['Lorem Ipsum'])
```