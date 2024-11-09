import click
from cognitopy import CognitoPy
from cognitopy.exceptions import ExceptionAuthCognito
from cognitoctl.commands import init_cognitopy
from cognitopy.enums import MessageAction


@click.command()
@click.option("--username", "-u", required=True, type=str)
@click.option("--password", "-p", required=True, type=str)
@click.option('-c', '--confirm', is_flag=True)
@init_cognitopy
def create(cognitopy: CognitoPy, username: str, password: str, confirm: bool):
    try:
        if confirm:
            cognitopy.admin_create_user(username=username, temporary_password=password, user_attributes={},
                                        message_action=MessageAction.SUPPRESS, force_alias=False,
                                        desired_delivery=[])
        else:
            cognitopy.register(username=username, password=password)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User registered successfully")


@click.command()
@click.option("--username", "-u", required=True, type=str)
@click.option("--code", "-c", required=True, type=str)
@init_cognitopy
def confirm(cognitopy: CognitoPy, username: str):
    try:
        cognitopy.admin_confirm_register(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User confirmed successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def delete(cognitopy: CognitoPy, username: str):
    try:
        cognitopy.admin_delete_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User deleted successfully")


@click.command()
@click.option("--username", "-u", required=True, type=str)
@click.option("--previous", "-r", required=True, type=str)
@click.option("--password", "-p", required=True, type=str)
@init_cognitopy
def change_password(cognitopy: CognitoPy, username: str, previous: str, password: str):
    try:
        tokens = cognitopy.login(username=username, password=previous)
        cognitopy.change_password(previous_password=previous, proposed_password=password,
                                  access_token=tokens["access_token"])
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User deleted successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def enable(cognitopy: CognitoPy, username: str):
    try:
        cognitopy.admin_enable_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User enabled successfully")


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def disable(cognitopy: CognitoPy, username: str):
    try:
        cognitopy.admin_disable_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User disabled successfully")

# Disabled user
# Enable user
# get user
# list users
# List users in group
