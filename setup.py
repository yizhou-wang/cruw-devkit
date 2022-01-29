import os
from setuptools import setup, find_packages


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def get_requirements(filename='requirements.txt'):
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, filename), 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires


if __name__ == '__main__':
    setup(
        name='cruw-devkit',
        version='1.1',
        description='The official devkit of the CRUW dataset',
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://github.com/yizhou-wang/cruw-devkit',
        author='Yizhou Wang',
        author_email='ywang26@uw.edu',
        classifiers=[
            'License :: Free for non-commercial use',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        packages=find_packages(include=["cruw.*"]),
        # package_dir={'': 'cruw'},
        package_data={'': ['*.json']},
        python_requires='>=3.6',
        install_requires=get_requirements(),
    )
