import setuptools

import async_newtel

setuptools.setup(
    name='simple-newtel',
    version=async_newtel.__version__,
    description='New-tel simple async client based on httpx',
    packages=['simple-sendgrid'],
    install_requires=[
        "httpx>=0.21",
    ],
    author_email='saltytimofey@gmail.com',
)
