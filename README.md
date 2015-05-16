# Jekkish


Inspired by the writing workflow of Markdown + YAML used in Jekyll, I wanted a system that would allow me to do something similar for LaTeX files. More often than not, I reuse my LaTeX styles, and import a file of content in the {maincontent} environment.

This system handles content marked-up with LaTeX, with a YAML header.

While this code works (with no guarantees), it definitely needs tests and better error handling and more flexible of code. That said, this is far enough along that it works... so that's pretty awesome! I can also currently build these files from Sublime Text.

Compatible with both Python 2 and 3.

Tested (thus far) on OSX.

## Installation
This package is available on PIP. To install, run '''pip install jekkish'''

If you use SublimeText, you can use place jekkish.sublime-build in your Sublime\ Packages/User

## Other information
I haven't yet included any templates in this package. But these should be placed in ~/.jekkish/

These are referenced by the <template> variable. Jekkish adds the .tex extension

These files are essentially LaTeX files, but with some templating logic.
* ((* *)) is used for enclosing logic
* (((<name>))) is used for where variables will be rendered.
* Everything below the YAML header will be rendered in the (((content))) tag.
* Everything above the YAML header will be ignored.
