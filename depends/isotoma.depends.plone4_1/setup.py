from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name = 'isotoma.depends.plone4_1',
    version = version,
    description = "Running plone in a virtualenv",
    long_description = open("README.rst").read(),
    classifiers = [
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
        ],
    keywords = "zope plone virtualenv",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    zip_safe = False,
    install_requires = open("requirements.txt").read().strip().split("\n"),
    )

