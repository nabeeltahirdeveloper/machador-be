from flask_jwt_extended import create_access_token


def user_token(email):
    # obj = Admin(user["email"], user["role"])
    access_token = create_access_token( identity={"username": email, "roles": "user"}, expires_delta=False)
    return access_token
