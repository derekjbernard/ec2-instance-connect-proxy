import codecs
import os.path
import re
import sys
from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='eicproxy',
    version=find_version('eicproxylibs', '__init__.py'),
    description='An ssh ProxyCommand utility that integrates AWS "EC2 Instance Connect" with native ssh tools (ssh, rsync, ansible, etc).',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/derekjbernard/ec2-instance-connect-proxy',
    author='Derek J. Bernard',
    author_email='derekjbernard@gmail.com',
    classifiers=[  
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: File Transfer Protocol (FTP)',
        'Topic :: System :: Systems Administration :: Authentication/Directory'
    ],
    keywords='aws ec2 instance connect ssh rsync scp ansible proxycommand proxy openssh nc',
    packages=find_packages(exclude=['test']),
    package_data={},
    install_requires=['boto3'],
    scripts=['bin/eicproxy'],
    project_urls={
        'Bug Reports': 'https://github.com/FrederikP/sshaws/issues',
        'Source': 'https://github.com/FrederikP/sshaws',
    },
)