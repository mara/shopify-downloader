"""
Command line interface for shopify downloader
"""

from functools import partial

import click

from shopify_downloader import config, downloader


def config_option(config_function):
    """Helper decorator that turns an option function into a cli option"""

    return lambda function: \
        click.option('--' + config_function.__name__,
                     help=config_function.__doc__ + '. Example: "' + config_function() + '"') \
            (function)


def apply_options(kwargs):
    """Applies passed cli parameters to config.py"""
    for key, value in kwargs.items():
        if value: setattr(config, key, partial(lambda v: v, value))


@click.command()
@config_option(config.shop_url)
@config_option(config.api_key)
@config_option(config.password)
@config_option(config.data_dir)
@config_option(config.order_status)
def download_data(**kwargs):
    """
    Downloads data.
    When options are not specified, then the defaults from config.py are used.
    """
    apply_options(kwargs)
    downloader.download_data()
