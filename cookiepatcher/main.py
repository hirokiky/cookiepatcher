import os
import sys
import subprocess

from cookiecutter.config import get_user_config, USER_CONFIG_PATH
from cookiecutter.generate import generate_context
from cookiecutter.main import expand_abbreviations
from cookiecutter.prompt import prompt_for_config
from cookiecutter.vcs import clone

from jinja2 import Template


def cookiepatch():
    template = sys.argv[1]
    diff = sys.argv[2]
    no_input = False

    config_dict = get_user_config(config_file=USER_CONFIG_PATH)
    template = expand_abbreviations(template, config_dict)

    repo_dir = clone(repo_url=template,
                     clone_to_dir=config_dict['cookiecutters_dir'],
                     checkout=None, no_input=no_input)
    patch_bytes = subprocess.check_output(['git', 'diff', diff], cwd=repo_dir)
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

    p = subprocess.Popen(['patch',  '-p1'], stdin=subprocess.PIPE, cwd='..')
    p.communicate(rendered.encode())


if __name__ == '__main__':
    cookiepatch()
