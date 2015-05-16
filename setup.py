from distutils.core import setup

setup(
    name = 'jekkish',
    packages = ['jekkish'],
    entry_points = {
      "console_scripts": ['jekkish = jekkish.jekkish:main']
    },
    version = '0.1.5',
    description = 'A template-based LaTeX renderer inspired by Jekyll',
    author = 'Josh Zaslow',
    author_email = 'josh.zaslow@gmail.com',
    url = 'https://github.com/joshjzaslow/latex-jekkish',
    download_url = 'https://github.com/joshjzaslow/latex-jekkish/tarball/0.1.5',
    keywords = ['LaTeX'],
    classifiers = [],
    install_requires = ['PyYAML', 'Jinja2'],
)
