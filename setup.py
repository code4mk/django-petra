from setuptools import setup, find_packages
import os
import re
import shutil
import sys

def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


version = get_version('django_petra')

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist bdist_wheel")
    if os.system("twine check dist/*"):
        print("twine check failed. Packages might be outdated.")
        print("Try using `pip install -U twine wheel`.\nExiting.")
        sys.exit()
    os.system("twine upload dist/*")
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    shutil.rmtree('dist')
    shutil.rmtree('build')
    shutil.rmtree('django_petra.egg-info')
    sys.exit()
    
def read(f):
    with open(f, 'r', encoding='utf-8') as file:
        return file.read()
    
setup(
    # Package metadata
    name='django-petra',
    version=version,
    url='https://django-petra.code4mk.org/',
    author='Mostafa Kamal',
    author_email='hiremostafa@gmail.com',
    description='A utility package for Django that makes API development easier for developers.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords=['django', 'drf', 'django-rest-framework', 'django-rest-api', 'django-petra', 'code4mk'],
    
    # Package configuration
    packages=find_packages(exclude=['tests*']),
    python_requires='>=3.6',
    
    # Dependencies
    install_requires=[
        "redis",
        "boto3",
        "psycopg2-binary",
        "djangorestframework",
        "python-dotenv",
        "celery",
        "beautifulsoup4",
        "premailer",
        "celery-redbeat",
    ],

    # Classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Source': 'https://github.com/code4mk/django-petra',
        'Changelog': 'https://github.com/code4mk/django-petra/blob/main/CHANGELOG.md',
    },
)
