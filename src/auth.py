from flask import Blueprint

auth = Blueprint("auth",__name__, url_prefix="/api/v1/auth")

#add post logic register
@auth.post('/register')
def register():
    return "user created"

@auth.get('/me')
def me():
    return {"id":1,"name":"John Doe"}