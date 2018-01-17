CONTENT = [
    {'tag': 'h3', 'children': ['Title']},
    {'tag': 'p', 'children': [
        'Paragraph 1 with ',
        {'tag': 'strong', 'children': ['strong']},
        ' and ',
        {'tag': 'a', 'attrs': {'href': '#'}, 'children': ['anchor']},
        '.'
    ]},
]
HTML = """<h3>Title</h3><p>Paragraph 1 with <strong>strong</strong> and <a href="#">anchor</a>.</p>"""