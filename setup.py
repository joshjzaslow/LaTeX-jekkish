from distutils.core import setup

setup(
    name = 'jekkish',
    packages = ['jekkish'],
    entry_points = {
      "console_scripts": ['jekkish = jekkish.jekkish:main']
    },
    version = '0.1.8',
    description = 'A template-based pdftex CLI frontend inspired by Jekyll',
    author = 'Josh Zaslow',
    author_email = 'josh.zaslow@gmail.com',
    url = 'https://github.com/joshjzaslow/latex-jekkish',
    download_url = 'https://github.com/joshjzaslow/latex-jekkish/tarball/0.1.8',
    keywords = ['LaTeX'],
    classifiers = [],
    install_requires = ['PyYAML', 'Jinja2'],
)
