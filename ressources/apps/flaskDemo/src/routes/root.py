from flask import Blueprint, url_for

root_bp = Blueprint("root", __name__)


@root_bp.route("/")
def root():
    return f"""
    <html>
        <head>
            <title>OpenFactory Flask App</title>
        </head>
        <body>
            <h1>Hello World</h1>
            <p>Welcome to OpenFactory Flask App</p>
            <a href="{url_for('about.about')}">About</a>
        </body>
    </html>
    """
