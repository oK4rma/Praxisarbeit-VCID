from flask_apidoc.commands import GenerateApiDoc

def register(app):
    @app.cli.group()
