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


class YammTex():

    def __init__(self, target_file):
        self.target_file = target_file
        self.output_file = target_file.replace('.yd', '.tex')
        self.variables = self.load_variables()
        self.home = expanduser("~")
        self.template_dir = self.home + '/.yammTeX'
        self.default_template = self.template_dir + '/default._tex'

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
                        content += "  " + line

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
            template_file = self.template_dir + '/' + self.variables["template"] + '._tex'
        else:
            template_file = default

        #6. Run through the template
        template = texenv.get_template(template_file)
        # template = Template('Hello {{ name }}\n\n{{ content }}!')

        f = open(self.output_file, "w")  #opens file with name of "test.txt"
        f.write(template.render(self.variables))
        f.close()

        print("LaTeX file written\n---")

    def make_pdf(self):
        print("Generating PDF\n---")
        call(["pdflatex", "", self.output_file])

    def render(self):
        # self.make_file()
        # self.make_pdf()
        pass


def main(target_file, output_file="", watch=False):
    new_file = YammTex(target_file)

    if watch:
        print("---\nPerforming initial rendering\n---")

        last_time = False
        while True:
            if last_time != os.stat(target_file).st_mtime:
                last_time = os.stat(target_file).st_mtime
                new_file.render()
                print("---\nWatching {}\n---").format(target_file)
    else:
        new_file.render()


# This should be properly updated to use argparse
if __name__ == "__main__":

    if len(sys.argv) >= 2 and sys.argv[1] == "watch":
        print("watch mode!")
        if len(sys.argv) >= 3:
            target_file = sys.argv[2]
        else:
            raise Exception

        if len(sys.argv) >= 4:
            output_file = sys.argv[3]

        main(target_file, watch=True)
    else:
        if len(sys.argv) >= 2:
            target_file = sys.argv[1]
        else:
            raise Exception

        if len(sys.argv) >= 3:
            output_file = sys.argv[2]

        main(target_file)
