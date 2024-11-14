import click
from cognitopy import CognitoPy
from cognitopy.exceptions import ExceptionAuthCognito
from cognitoctl.commands import init_cognitopy
from cognitopy.enums import MessageAction


@click.command()
@click.option("--username", "-u", required=True, type=str)
@click.option("--password", "-p", required=True, type=str)
@init_cognitopy
def create(cognitopy: CognitoPy, username: str, password: str):
    try:
        cognitopy.register(username=username, password=password)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User registered successfully")


@click.command()
@click.option("--username", "-u", required=True, type=str)
@click.option("--code", "-c", required=False, type=str)
@click.option("--force", "-f", is_flag=True)
@init_cognitopy
def confirm(cognitopy: CognitoPy, username: str, code: str, force: bool):
    try:
        if force:
            cognitopy.admin_confirm_register(username=username)
        else:
            if code:
                cognitopy.confirm_register(username=username, confirmation_code=code)
            else:
                click.echo("Confirmation code is required")
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


@click.command()
@click.argument("username", type=str)
@init_cognitopy
def get(cognitopy: CognitoPy, username: str):
    try:
        user = cognitopy.admin_get_user(username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for key, value in user.items():
            click.echo(f"{key}: {value}")


@click.command()
@click.option("--group", "-g", required=False, type=str)
@click.option("--limit", "-l", required=False, type=int)
@click.option("--filter_attr", "-f",multiple=True , required=False, type=list[str])
@init_cognitopy
def list(cognitopy: CognitoPy, group: str, limit: int, filter_attr: list[str]):
    try:
        click.echo(filter_attr)
        users = cognitopy.list_users(group=group, limit=limit)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for user in users:
            for key, value in user.items():
                click.echo(f"{key}: {value}")
            click.echo("--------------------------------\n")
        click.echo(f"Total users: {len(users)}")
