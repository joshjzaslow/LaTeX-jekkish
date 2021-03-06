import sys
from os.path import expanduser
from os.path import splitext
from os.path import split
from os.path import exists
from os.path import realpath
from os.path import dirname
from os.path import join
from os import remove, stat
import errno
from subprocess import check_call
import yaml
import argparse
from time import sleep

from jinja2 import Environment
from jekkish.texhelpers import escape_tex, TeXLoader

__version__ = "0.3.2"


class Jekkish():

    def __init__(self, target_file, job_name=False):
        self.target_file = target_file
        fullpath, ext = splitext(self.target_file.name)
        path, filename = split(fullpath)
        self.temp_file = filename + '._' + ext[1:]
        self.job_name = job_name if job_name else filename
        self.variables = self.load_variables()
        self.home = expanduser("~")
        self.template_dir = self.home + '/.jekkish'
        if 'xelatex' in self.variables:
            self.engine = 'xelatex'
            self.default_template = 'default-xe'
        else:
            self.engine = 'pdflatex'
            self.default_template = 'default'

        self.command = '{} --jobname={} {}'.format(
            self.engine,
            self.job_name,
            self.temp_file)

    def load_variables(self, division_string="---\n"):
        """ Converts the file to YAML and returns the parsed data.

        Ignores any content above the YAML header (start_yaml),
        Loads everything after the YAML as part of the 'content' variable """

        start_yaml = False
        end_yaml = False
        variables = ""
        content = "content: >"

        for line in self.target_file:
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

        if "template" not in self.variables:
            self.variables["template"] = self.default_template

        template_file = self.template_dir + \
            '/' + self.variables["template"] + '.tex'

        if not exists(template_file):
            template_file = join(
                dirname(realpath(__file__)),
                self.variables["template"] + '.tex')

        template = texenv.get_template(template_file)

        f = open(self.temp_file, "w")
        f.write(template.render(self.variables))
        f.close()

        print("Temporary LaTeX file created ({})\n---".format(self.temp_file))

    def make_pdf(self, clean=True):
        """ Calls pdftex and (optionally) removes temporary files """

        print("Generating PDF\n---")

        check_call(self.command, shell=True)

        if clean:
            for ext in ['aux', 'log', 'out', 'ent']:
                try:
                    remove(self.job_name + '.' + ext)
                except (OSError, IOError) as e:
                    # Use FileNotFoundError when python 2 is dropped
                    if e.errno != errno.ENOENT:
                        raise

    def render(self):
        self.make_file()
        self.make_pdf()

    def watch(self):
        print("---\nJekkish running in watch mode\n")
        print("---\nPerforming initial rendering\n---")

        last_time = False
        while True:
            if last_time != stat(self.target_file.name).st_mtime:
                last_time = stat(self.target_file.name).st_mtime
                sleep(0.1)
                self.target_file = open(self.target_file.name, 'r')
                self.variables = self.load_variables()
                self.make_file()
                sleep(0.1)
                self.render()
                print("---\nWatching {}\n---".format(self.target_file.name))


def main():
    parser = argparse.ArgumentParser(
        prog="Jekkish",
        description="A template-based pdftex CLI frontend inspired by Jekyll"
    )
    parser.add_argument(
        'filename',
        type=argparse.FileType('r'),
        default=sys.stdin,
        help='The file to process'
    )
    parser.add_argument(
        'jobname',
        nargs="?",
        default=False,
        help='Job name for pdftex output'
    )
    parser.add_argument(
        '--watch',
        action='store_const',
        const='watch',
        help='Watch <filename> for changes'
    )
    parser.add_argument(
        '--xelatex',
        action='store_const',
        const=True,
        help='Use xeLaTeX for rendering'
    )
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    args = parser.parse_args()
    new_file = Jekkish(args.filename, args.jobname)

    if args.watch:
        new_file.watch()
    else:
        new_file.render()


if __name__ == "__main__":
    main()
