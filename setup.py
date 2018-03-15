from setuptools import setup

github = 'https://github.com/jacoduplessis/telegraph'
docs = 'http://telegraph.readthedocs.io/en/latest/'

setup(
    name='telegraph_client',
    author='Jaco du Plessis',
    author_email='jaco@jacoduplessis.co.za',
    description='Client and utilities for the Telegraph blogging service provided by Telegram.',
    long_description=f'Read the docs: {docs}.',
    url=github,
    keywords='telegraph client telegram',
    project_urls={
        'Documentation': docs,
        'Source': github,
        'Tracker': f'{github}/issues',
    },
    version='0.1.0',
    packages=['telegraph'],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
