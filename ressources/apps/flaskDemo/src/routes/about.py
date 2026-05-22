from flask import Blueprint

about_bp = Blueprint("about", __name__)


@about_bp.route("/about")
def about():
    return """
    <html>
        <head>
            <title>About</title>
        </head>
        <body>
            <h1>About OpenFactory Flask App</h1>
            <p>This is a demo Flask application.</p>
        </body>
    </html>
    """
