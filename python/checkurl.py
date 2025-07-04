"""
A Python test assignment
"""

import csv
import requests
import click

@click.command(
        context_settings={"help_option_names": ("-h", "--help")},
        help="Prints out website responses from a csv file. \n " \
        "Returns website name, status code and time elapsed." )
@click.option("-i", "--input_file", type=click.Path(exists=True), help="Path to a csv file.")
@click.option("-t", "--timeout", default=3, help="URL requests timeout threshold in seconds.")

def check_url_from_file(input_file: str, timeout: int):
    """
    Prints out website responses from a csv file, line by line.

    Args:
        input_file (string): Takes csv file as input.
        timeout (int): A number that is used for the request timeout limit. Default number is 3.

    """
    # function reference
    check_line = line_parse
    with open(input_file, "r", encoding="utf-8") as file:
        try:
            text_line = csv.reader(file)
            for line in text_line:
                result = check_line(current_line=line, time_out=timeout)
                click.echo(result)
        except IOError as e:
            click.echo(f"File error: {e}")
        except csv.Error as e:
            click.echo(f"CSV error: {e}")
        except Exception as e:
            click.echo(f"Unexpected error: {e}")

def line_parse(current_line: list, time_out: int) -> str:
    """
    Reads a line from a csv file.

    Splits up name and url from the current line and 
    checks the response status code and time elaspsed.

    Returns string with name, status code and time elapsed.

    Args:
        current_line (list): Current line as a list.
        time_out (int): A number that is used for the request timeout limit. 

    """
    decimal_places = 2
    try:
        name, url = "".join(current_line).split("|")
        response = requests.get(url, timeout=time_out)
        response_time = round(response.elapsed.total_seconds(), decimal_places)
        if response_time > time_out:
            return f'"Skipping {url}"'
        return f'"{name}", HTTP {response.status_code}, {response_time} seconds'
    except requests.exceptions.ConnectTimeout as e:
        return f"Connection Timeout error: {e}"
    except Exception as e:
        return f'"Line parse error: {e}"'

if __name__ == '__main__':
    check_url_from_file()
