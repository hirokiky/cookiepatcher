import argparse
import os
import subprocess

from cookiecutter.config import get_user_config, USER_CONFIG_PATH
from cookiecutter.generate import generate_context
from cookiecutter.main import expand_abbreviations
from cookiecutter.prompt import prompt_for_config
from cookiecutter.vcs import clone

from jinja2 import Template


def cookiepatch():
    parser = argparse.ArgumentParser(description='Tool to apply / create patch from '
                                                 'cookiecutter templates')
    parser.add_argument('template', type=str,
                        help='an integer for the accumulator')
    parser.add_argument('diff', type=str, nargs='+',
                        help='versions passed for git diff')
    parser.add_argument('--show', action='store_true',
                        help='Just print diff')

    args = parser.parse_args()

    no_input = False

    config_dict = get_user_config(config_file=USER_CONFIG_PATH)
    template = expand_abbreviations(args.template, config_dict)

    repo_dir = clone(repo_url=template,
                     clone_to_dir=config_dict['cookiecutters_dir'],
                     checkout=None, no_input=no_input)
    patch_bytes = subprocess.check_output(['git', 'diff'] +
                                          args.diff +
                                          ['--', '{{cookiecutter.repo_name}}'],
                                          cwd=repo_dir)
    patch_str = patch_bytes.decode()

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    context = generate_context(
        context_file=context_file,
        default_context=config_dict['default_context'],
        extra_context={},
    )
    # prompt the user to manually configure at the command line.
    # except when 'no-input' flag is set
    context['cookiecutter'] = prompt_for_config(context, no_input)

    rendered = Template(patch_str).render(**context)

    if args.show:
        print(rendered)
        return

    p = subprocess.Popen(['patch',  '-Np1', '--no-backup-if-mismatch'], stdin=subprocess.PIPE, cwd='..')
    p.communicate(rendered.encode())


if __name__ == '__main__':
    cookiepatch()
