from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='jekkish',
    version='0.1.8py3fix',

    description='A template-based pdftex CLI frontend inspired by Jekyll',
    long_description=long_description,

    url='https://github.com/joshjzaslow/latex-jekkish',
    download_url='https://github.com/joshjzaslow/latex-jekkish/tarball/0.1.8py3fix',

    author='Josh Zaslow',
    author_email='josh.zaslow@gmail.com',

    license='MIT',
    packages=['jekkish'],

    keywords=['LaTeX'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Topic :: Text Processing :: Markup :: LaTeX',
    ],

    install_requires=['PyYAML', 'Jinja2'],
    entry_points={
        "console_scripts": ['jekkish=jekkish.jekkish:main']
    },
)
