from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name = 'gambitparser',
        version = '0.0.1',
        description ='An efficent gambit parser for simple, perfect information games',
        long_description = long_description,
        long_description_content_type = 'text_markdown',
        author = 'Bailey Morton',
        author_email = 'baileymorton989@gmail.com',
        url = 'https://github.com/baileymorton989/gambitparser',
        license = 'MIT License',
        install_requires = ['gambit >=16.0.1', 'pandas >= 0.24.2',
                            'numpy >=1.16.6','argparse >= 1.1'],
        py_modules = ['gambitparser'],
        package_dir = {'': 'src'},
        classifiers =[
             'Programming Language :: Python :: 3',
             'Programming Language :: Python :: 3.6',
             'Programming Language :: Python :: 3.7',
             'Programming Language :: Python :: 3.8',
             'Programming Language :: Python :: 3.9',
             'License :: OSI Approved :: MIT License',
             'Operating System :: OS Independent',
        ],
        extras_require = {
            'dev': [
                'pytest>3.7',
                ],
            },

    )
