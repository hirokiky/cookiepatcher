import argparse
import json
import os
import subprocess
from distutils.version import LooseVersion

from cookiecutter.config import get_user_config, USER_CONFIG_PATH
from cookiecutter.generate import generate_context
from cookiecutter.main import expand_abbreviations
from cookiecutter.prompt import prompt_for_config
from cookiecutter.vcs import clone

if LooseVersion("1.5") <= LooseVersion(cookiecutter.__version__):
    from cookiecutter.repository import expand_abbreviations
else:
    from cookiecutter.main import expand_abbreviations

from jinja2 import Template


CONF_PATH = './cookiepatcher.json'


def cookiepatch():
    parser = argparse.ArgumentParser(description='Tool to apply / create patch from '
                                                 'cookiecutter templates')
    parser.add_argument('--template', type=str,
                        help='an integer for the accumulator')
    parser.add_argument('--diff', type=str, nargs='+',
                        help='versions passed for git diff')
    parser.add_argument('--show', action='store_true',
                        help='Just print diff')

    args = parser.parse_args()

    conf_file = None
    if os.path.exists(CONF_PATH):
        with open(CONF_PATH) as f:
            conf_file = json.load(f)

    if args.template:
        template = args.template
    elif conf_file and 'template' in conf_file:
        template = conf_file['template']
    else:
        template = input('Input template repository url: ')

    if args.diff:
        diff = args.diff
    elif conf_file and 'revision' in conf_file:
        diff = [conf_file['revision']]
    else:
        cur = input('Input template version applied currently: ')
        to = input('Input version to follow [master]: ') or 'master'
        diff = [cur, to]

    no_input = False

    config_dict = get_user_config(config_file=USER_CONFIG_PATH)
    parsed_template = expand_abbreviations(template, config_dict)

    repo_dir = clone(repo_url=parsed_template,
                     clone_to_dir=config_dict['cookiecutters_dir'],
                     checkout=None, no_input=no_input)
    patch_bytes = subprocess.check_output(['git', 'diff'] +
                                          diff +
                                          ['--', '{{cookiecutter.repo_name}}'],
                                          cwd=repo_dir)
    patch_str = patch_bytes.decode()

    context_file = os.path.join(repo_dir, 'cookiecutter.json')
    context = generate_context(
        context_file=context_file,
        default_context=config_dict['default_context'],
        extra_context={},
    )
    if conf_file:
        context['cookiecutter'] = conf_file['variables']
    else:
        # prompt the user to manually configure at the command line.
        # except when 'no-input' flag is set
        context['cookiecutter'] = prompt_for_config(context, no_input)

    rendered = Template(patch_str).render(**context)

    if args.show:
        print(rendered)
        return

    p = subprocess.Popen(['patch',  '-Np1', '--no-backup-if-mismatch'], stdin=subprocess.PIPE,
                         cwd='..')
    p.communicate(rendered.encode())

    # Generate cookiepatcher JSON
    if len(diff) == 1:
        rev = 'HEAD'
    else:
        rev = diff[-1]
    revision_bytes = subprocess.check_output(['git', 'rev-parse'] + [rev],
                                             cwd=repo_dir)
    revision_str = revision_bytes.decode().rstrip('\n')
    json_content = {
        'revision': revision_str,
        'variables': context['cookiecutter'],
        'template': template
    }
    with open(CONF_PATH, 'w') as f:
        json.dump(json_content, f, ensure_ascii=False, indent=2, sort_keys=True)


if __name__ == '__main__':
    cookiepatch()
