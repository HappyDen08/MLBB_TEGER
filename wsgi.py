"""WSGI-точка входу для PythonAnywhere.

У вкладці Web → Code → WSGI configuration file пропиши шлях до проєкту
й імпортуй звідси `application`:

    import sys
    path = "/home/<username>/ProjectForLudmila"
    if path not in sys.path:
        sys.path.insert(0, path)
    from wsgi import application
"""
from app.webhook import app as application
