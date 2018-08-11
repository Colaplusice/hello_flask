from flask.cli import cli


@cli.commands()
def hello_cli():
    print('wtf,so amazing')