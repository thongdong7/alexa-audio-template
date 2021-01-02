# encoding=utf-8
import json
import logging
import os
import shutil
import subprocess
from functools import partial
from os import getcwd
from os.path import dirname, join, isfile, isdir, exists

import click
import yaml
from jinja2 import Environment, StrictUndefined

logger = logging.getLogger('Build')

repo_dir = dirname(__file__)

copy_files = [
    'lambda/lambda_function.py',
    'lambda/requirements.txt',
    'lambda/utils.py',
    'lambda/alexa',
    'skill-package',
    'deploy.sh',
    'lambda/alexa/data.py',
    'skill-package/interactionModels/custom/en-US.json',
]


def build_jinja2_env(loader=None, undefined=StrictUndefined):
    env = Environment(loader=loader, undefined=undefined)

    env.line_statement_prefix = '##'

    def to_json(value):
        return json.dumps(value, indent=4, sort_keys=True)

    def to_json_no_new_line(value):
        if not value:
            # Try to fix error: TypeError: Object of type Undefined is not JSON serializable
            return None

        try:
            return json.dumps(value, sort_keys=True)
        except Exception as e:
            print('json.dumps() failed for value: %s' % value)
            logger.exception(e)

            return 'COULD_NOT_DUMP_VALUE'

    def format_list(list_, pattern):
        return [pattern % s for s in list_]

    env.filters['tojson'] = to_json
    env.filters['to_json_no_new_line'] = to_json_no_new_line
    env.filters['format_list'] = format_list

    return env


def template_string_render(template, params):
    jinja_template = build_jinja2_env().from_string(template)
    return jinja_template.render(**params)


def template_file_render(path, params):
    return template_string_render(
        template=open(path).read(),
        params=params
    )


def template_file_render_to_file(template_path, params, output_path):
    # logger.debug(f'Render template {template_path} to {output_path}...')
    content = template_file_render(
        path=template_path,
        params=params
    )

    file_write_content(
        path=output_path,
        content=content
    )


def file_create_folder_if_not_exists(file_path):
    file_dir = dirname(file_path)
    if not exists(file_dir):
        os.makedirs(file_dir)


def file_write_content(path, content):
    file_create_folder_if_not_exists(path)

    with open(path, 'wb') as f:
        f.write(content.encode('utf8', errors='ignore'))


@click.command()
@click.option('--src')
def cli(src):
    if not src:
        src = getcwd()

    if src == repo_dir:
        print('Error: Should provide --src parameter or run in the skill folder')
        exit(1)

    params = yaml.safe_load(open(join(src, 'config.yml')))
    render = partial(template_file_render_to_file, params=params)

    for item in copy_files:
        template_path = join(repo_dir, item)
        if isfile(template_path):
            render(
                template_path=template_path,
                output_path=join(src, item)
            )
        elif isdir(template_path):
            shutil.copytree(
                src=template_path,
                dst=join(src, item),
                dirs_exist_ok=True
            )

    subprocess.check_call(['chmod', '+x', join(src, 'deploy.sh')], cwd=src)


if __name__ == '__main__':
    cli()
