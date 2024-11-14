import click
from cognitopy import CognitoPy
from cognitopy.exceptions import ExceptionAuthCognito
from cognitoctl.commands import init_cognitopy


@click.command()
@click.option("name", "-n", required=True, type=str)
@click.option("description", "-d", required=True, type=str)
@click.option("precedence", "-p", required=True, type=int)
@click.option("role_arn", "-r", required=True, type=str)
@init_cognitopy
def create(cognitopy: CognitoPy, name: str, description: str, precedence: int, role_arn: str):
    try:
        cognitopy.admin_create_group(group_name=name, description=description, precedence=precedence, role_arn=role_arn)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("Group created successfully")

@click.command()
@click.argument("name", type=str)
@init_cognitopy
def delete(cognitopy: CognitoPy, name: str):
    try:
        cognitopy.admin_delete_group(group_name=name)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("Group deleted successfully")


@click.command()
@click.option("username", "-u", required=True, type=str)
@click.option("group", "-g", required=True, type=str)
@init_cognitopy
def delete_user(cognitopy: CognitoPy, username: str, group: str):
    try:
        cognitopy.admin_remove_user_from_group(group_name=group, username=username)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo(f"User {username} deleted of group {group} successfully")


@click.command()
@click.option("username", "-u", required=True, type=str)
@click.option("group", "-g", required=True, type=str)
@init_cognitopy
def add_user(cognitopy: CognitoPy, username: str, group: str):
    try:
        cognitopy.admin_add_user_to_group(username=username, group_name=group)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("User added to group successfully")


@click.command()
@click.option("--username", "-u", required=False, type=str)
@click.option("--limit", "-l", required=False, type=int)
@init_cognitopy
def list(cognitopy: CognitoPy, username: str, limit: int):
    try:
        if username:
            groups = cognitopy.admin_list_groups_for_user(username=username, limit=limit)
        else:
            groups = cognitopy.list_groups(limit=limit)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for group in groups:
            for key, value in group.items():
                click.echo(f"{key}: {value}")
            click.echo("--------------------------------\n")
        click.echo(f"Total groups: {len(groups)}")


@click.command()
@click.argument("group", type=str)
@init_cognitopy
def get(cognitopy: CognitoPy, group: str):
    try:
        user = cognitopy.get_group(group=group)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        for key, value in user.items():
            click.echo(f"{key}: {value}")


@click.command()
@click.option("--group", "-g", required=True, type=str)
@click.option("--description", "-d", required=False, type=str)
@click.option("--role", "-r", required=False, type=str)
@click.option("--precedence", "-p", required=False, type=int)
@init_cognitopy
def edit(cognitopy: CognitoPy, group:str, description: str, role: str, precedence: int):
    try:
        groups = cognitopy.update_group(group=group, description=description, role=role, precedence=precedence)
    except ExceptionAuthCognito as e:
        click.echo(e)
    else:
        click.echo("Edited group successfully")
