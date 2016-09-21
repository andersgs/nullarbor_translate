'''
A package to transform Nullarbor Reports to format using Jinja2 templates

The package creates a NullarborObj with all the information in the Nullarbor
Reports folder. The object has the data that can be accessed to render
templates.
'''

import click
import jinja2
import pkg_resources
import os

from NullarborObj import NullarborObj
from ConfigReader import ConfigReader

@click.command()
@click.option("--template_file", help="Path to a template file in Jinja2 format", default="mdu_lims.json")
@click.option("--config_file", help="Path to a configuration file to obtain general parameters", default='mdu_config.yaml')
@click.option("--nullarbor_report", help="Path to Nullarbor report folder", default='.')
@click.option("--job_id", help='Job number', default='UNKNOWN')
def main(template_file, config_file, nullarbor_report, job_id):
    # Sorting out the config
    if config_file == 'mdu_config.yaml':
        config_file = os.path.join(pkg_resources.resource_filename(__name__, "config_file"), "mdu_config.yaml")
    config = ConfigReader()
    config.read_config(config_file)
    config.add_sops()
    config.add_filenames()
    # Reading in the template
    if template_file == 'mdu_lims.json':
        template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(pkg_resources.resource_filename(__name__, "templates")))
    else:
        template_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(template)))
    template = template_env.get_template(template_file)
    #Creating the NullarborObj
    if nullarbor_report == '.':
        nullarbor_report = os.getcwd()
    nullarbor = NullarborObj(nullarbor_report, job_id)
    nullarbor.add_mlst(config.filenames['mlst'])
    nullarbor.add_resistome(config.filenames['resistome'])
    nullarbor.add_sops(config.sops)
    nullarbor.render_template(template)

if __name__ == '__main__':
    main()
