# Jekkish

* jekkish.py -- symbolically linked to a location in path (this system is not yet ready for proper distribution, after all).
* jekkish.sublime-build -- goes in Sublime\ Packages/User

Inspired by the writing workflow of Markdown + YAML used in Jekyll, I wanted a system that would allow me to do something similar for LaTeX files. More often than not, I reuse my LaTeX styles, and import a file of content in the {maincontent} environment.

This system handles content marked-up with LaTeX, with a YAML header.

While this code works* (with no guarantees), it definitely needs tests and better error handling and more flexible of code. That said, this is far enough along that it works... so that's pretty awesome! I can also currently build these files from Sublime Text.

Compatible with both Python 2 and 3.

Tested (thus far) on OSX.
