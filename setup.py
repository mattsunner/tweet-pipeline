from distutils.core import setup
import re

with open('README.md') as fp:
    long_description = fp.read()


def find_version():
    with open('pipeline-app/__init__.py') as fp:
        for line in fp:
            match = re.search(r"__version__\s*=\s*'([^']+)'", line)
            if match:
                return match.group(1)
    assert False, 'cannot find version'


setup(
    name='tweet-pipeline',
    version=find_version(),
    author='Matthew Sunner',
    author_email='matt@mattsunner.com',
    license='LICENSE.txt',
    description='Tweet Pipeline',
    long_description=long_description,
    packages=['pipeline-app']
)
