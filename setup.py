from setuptools import setup, find_packages

version = '0.0.0'

setup(
    name = 'isotoma.plone.heroku',
    version = version,
    description = "Tooling for running Plone on heroku in a virtualenv",
    long_description = open("README.rst").read() + "\n" + open("CHANGES.txt").read(),
    classifiers = [
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX",
        "License :: OSI Approved :: Apache Software License",
        ],
    keywords = "zope plone virtualenv foreman",
    author = "John Carr",
    author_email = "john.carr@isotoma.com",
    license="Apache Software License",
    packages = find_packages(exclude=['ez_setup']),
    package_data = {
        '': ['README.rst', 'CHANGES.txt'],
        },
    namespace_packages = ['isotoma', 'isotoma.plone'],
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'setuptools',
        'isotoma.recipe.plonetools',
        ],
    entry_points = {
        'console_scripts': [
            'plone = isotoma.plone.heroku.runner:run',
            'migrate = isotoma.plone.heroku.migrate:run',
            'run = isotoma.plone.heroku.other:run',
            'debug = isotoma.plone.heroku.other:debug',
            ]
         },
    )

