
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

setup(
    name='eicproxy',
    version='0.0.1',
    description='An ssh ProxyCommand utility that integrates AWS "EC2 Instance Connect" with native ssh tools (ssh, rsync, ansible, etc).,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/derekjbernard/ec2-instance-connect-proxy',
    author='Derek J. Bernard',
    author_email='derekjbernard@gmail.com',
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: Proxy Servers',
        'Topic :: Security',
        'Topic :: Software Development',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Networking',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='aws ec2 instance connect ssh rsync scp ansible proxycommand proxy openssh nc',
    packages=[],
    python_requires='>=3.0, <4',
    install_requires=['boto3'],
    scripts=['eicproxy'],
    project_urls={
        'Bug Reports': 'https://github.com/FrederikP/sshaws/issues',
        'Source': 'https://github.com/FrederikP/sshaws',
    },
)