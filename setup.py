from app import create_app
from werkzeug.contrib.fixers import ProxyFix


app = create_app()

if __name__ == '__main__':
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
