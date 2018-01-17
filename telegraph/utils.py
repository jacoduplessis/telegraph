from xml.dom.minidom import Document

import bleach
from bs4 import BeautifulSoup

ALLOWED_TAGS = [
    'a', 'aside', 'b', 'blockquote', 'br', 'code', 'em', 'figcaption',
    'figure', 'h3', 'h4', 'hr', 'i', 'iframe', 'img', 'li', 'ol', 'p',
    'pre', 's', 'strong', 'u', 'ul', 'video'
]

SOURCES = ['href', 'src']

ALLOWED_ATTRIBUTES = {
    'a': SOURCES,
    'iframe': SOURCES,
    'img': SOURCES,
    'video': SOURCES,
}


def html_to_content(html):
    clean = bleach.clean(html, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRIBUTES, strip=True,
                         strip_comments=True).strip()
    soup = BeautifulSoup(clean, "html.parser")

    def inner(tag):

        if tag.name is None:
            if not tag.string.strip():
                return None
            return tag.string

        node = {
            "tag": tag.name,
        }

        if tag.attrs:
            node["attrs"] = tag.attrs

        children = tag.children

        if children:
            child_list = []
            for child in children:
                result = inner(child)
                if result is not None:
                    child_list.append(result)
            node['children'] = child_list

        return node

    # return the children of the root document as final result
    return inner(soup)['children']


def content_to_html(content):
    document = Document()

    root = document.createElement('div')

    def inner(node):

        if isinstance(node, str):
            return document.createTextNode(node)

        dom_node = document.createElement(node['tag'])

        if 'attrs' in node:
            for name, value in node['attrs'].items():
                dom_node.setAttribute(name, value)

        if 'children' in node:
            for child in node['children']:
                dom_node.appendChild(inner(child))

        return dom_node

    for node in content:
        root.appendChild(inner(node))

    # strip wrapper div
    return root.toxml()[5:-6]
