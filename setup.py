import os
import sys
from setuptools import setup, find_packages

version_file = os.path.join(os.path.dirname(__file__), 'VERSION.txt')
with open(version_file, 'r') as f:
    version = f.readline().strip()

readme_file = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(version_file, 'r') as f:
    long_description = f.readline().strip()


setup(
    name = 'django-authority',
    version = version,
    url = 'https://github.com/xuyunj/django-authority',
    author = 'xuyunj',
    download_url='https://github.com/xuyunj/django-authority.git',
    description ="Authorization based on rbac for django.",
    long_description = long_description,
    zip_safe = False,
    packages = find_packages(),
    include_package_data = True,
    license = 'BSD',
    install_requires = [
        'Django >= 1.7',
    ],
    classifiers = ['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Security',
                   'Programming Language :: Python :: 2.7',
    ],
)

