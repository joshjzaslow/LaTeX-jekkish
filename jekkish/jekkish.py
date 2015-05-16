#!/usr/bin/env python
import sys, os
from os.path import join, exists, getmtime
from os.path import expanduser
from subprocess import call
import re
import yaml

from jinja2 import Environment
from jinja2 import BaseLoader, TemplateNotFound


def escape_tex(value):
    """ This function allows us to redefine the jinja environment \
     to handle LaTeX environments """
    # This code, and the code that call this is courtesy of Clemens Kaposi
    # http://flask.pocoo.org/snippets/55/

    LATEX_SUBS = (
        (re.compile(r'\\'), r'\\textbackslash'),
        (re.compile(r'([{}_#%&$])'), r'\\\1'),
        (re.compile(r'~'), r'\~{}'),
        (re.compile(r'\^'), r'\^{}'),
        (re.compile(r'"'), r"''"),
        (re.compile(r'\.\.\.+'), r'\\ldots'),
    )

    newval = value
    for pattern, replacement in LATEX_SUBS:
        newval = pattern.sub(replacement, newval)
    return newval


class TeXLoader(BaseLoader):
    """ This environment loader allows us to readily customize \
    the Jinja2 BaseLoader class for our purposes """

    def __init__(self, path):
        self.path = path

    def get_source(self, environment, template):
        path = join(self.path, template)
        if not exists(path):
            raise TemplateNotFound(template)
        mtime = getmtime(path)
        with open(path) as f:
            if sys.version_info[0] < 3:
                source = f.read().decode('utf-8')  # Python 2
            else:
                source = f.read()  # Python 3
        return source, path, lambda: mtime == getmtime(path)


class Jekkish():

    def __init__(self, target_file, output_file=False):
        self.target_file = target_file
        filename, ext = os.path.splitext(target_file)
        self.temp_file = filename + '._' + ext[1:]
        self.output_file = output_file
        self.variables = self.load_variables()
        self.home = expanduser("~")
        self.template_dir = self.home + '/.jekkish'
        self.default_template = self.template_dir + '/default.tex'

    def load_variables(self, division_string="---\n"):
        """ Converts the file to YAML and returns the parsed data.

        Ignores any content above the YAML header (start_yaml),
        Loads everything after the YAML as part of the 'content' variable """

        try:
            stream = open(self.target_file, 'r')
        except (IOError):
            print("File not found.")
            exit()

        start_yaml = False
        end_yaml = False
        variables = ""
        content = "content: >"

        for line in stream:
            if str(line) == division_string:
                if start_yaml:
                    end_yaml = True
                else:
                    start_yaml = True
            else:
                if start_yaml:
                    if not end_yaml:
                        variables += line
                    else:
                        if line == "\n":
                            content += "  {}".format(line)
                        else:
                            content += "  {}\n".format(line)

        variables += content
        return yaml.load(variables)

    def make_file(self):
        texenv = Environment(loader=TeXLoader(self.home))
        texenv.block_start_string = '((*'
        texenv.block_end_string = '*))'
        texenv.variable_start_string = '((('
        texenv.variable_end_string = ')))'
        texenv.comment_start_string = '((='
        texenv.comment_end_string = '=))'
        texenv.filters['escape_tex'] = escape_tex

        if self.variables["template"]:
            template_file = self.template_dir + \
                '/' + self.variables["template"] + '.tex'
        else:
            template_file = self.template_dir + \
                '/' + self.default

        template = texenv.get_template(template_file)

        f = open(self.temp_file, "w")
        f.write(template.render(self.variables))
        f.close()

        print("Temporary LaTeX file created ({})\n---".format(self.temp_file))

    def make_pdf(self):
        print("Generating PDF\n---")
        if self.output_file:
            command = '-jobname={}'.format(self.output_file)
            call(["pdflatex", command, self.temp_file])
        else:
            call(["pdflatex", self.temp_file])

    def render(self):
        self.make_file()
        self.make_pdf()


def watch(target_file, output_file=False):

    print("---\nJekkish running in watch mode\n")

    if output_file:
        new_file = Jekkish(target_file, output_file)
    else:
        new_file = Jekkish(target_file)

    print("---\nPerforming initial rendering\n---")

    last_time = False
    while True:
        if last_time != os.stat(target_file).st_mtime:
            last_time = os.stat(target_file).st_mtime
            new_file.render()
            print("---\nWatching {}\n---").format(target_file)


def main(args):

    if len(args) >= 1 and args[0] == "watch":
        if len(args) >= 2:
            target_file = args[1]
            output_file = False
        else:
            raise Exception

        if len(args) >= 3:
            output_file = args[2]

        watch(target_file, output_file)
    else:
        if len(args) >= 1:
            target_file = args[0]
            output_file = False
        else:
            raise Exception

        if len(args) >= 2:
            output_file = args[1]

    new_file = Jekkish(target_file, output_file)
    new_file.render()


if __name__ == "__main__":
    main(sys.argv[1:])
