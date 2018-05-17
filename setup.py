from app import create_app
from werkzeug.contrib.fixers import ProxyFix


if __name__ == '__main__':
    app = create_app()
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
