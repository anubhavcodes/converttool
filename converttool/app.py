import click
from converttool import *
from converttool.exceptions import *
from converttool.converter import Converter
import logging


@click.command()
@click.option('--output-name', default='output', help='Name of the output file without extension. `output` by default')
@click.option('--pretty', default=False, is_flag=True, help='Pretty print the output. Disabled by default')
@click.option('--strict', default=False, is_flag=True, help='Set strict validation, tool will stop if data is valid. False by default')
@click.option('--log', default="notset", help='Enable logging for converttool', type=click.Choice(['info', 'debug', 'notset']))
@click.argument('output_format', nargs=-1)
@click.argument('csv', nargs=1)
def main(output_name, pretty, strict, log, output_format, csv):
    try:
        Converter(csv_file=csv, output_format=output_format, output_name=output_name, pretty=pretty, loglevel=log, strict=strict).convert()
    except CSVNotFound:
        click.echo("{} Not Found. Are you in the right directory?".format(csv))

    except FormatterNotFound:
        click.echo("{} is not supported yet. Can you add support to this format?".format(output_format))
    except ConversionError:
        click.echo("There was a problem in converting and writing to the output file.")
        click.echo("This is not good")
        click.echo("I suggest you enable debugging and send the logs to author")
    except ValidationError:
        click.echo("Validation Failed! You might not want to use the --strict flag")
    except Exception as e:
        print e
