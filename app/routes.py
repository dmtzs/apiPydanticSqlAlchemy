try:
    from .models import Users
    from typing import Optional
    from app import app, database
    from flask_pydantic import validate
    from flask_pydantic.exceptions import ValidationError
    from flask import jsonify, make_response, abort, Response
    from .response_messages import no_users, validation_data_error
    from .validators import GeneralDataResponse, DataResponse, FindUserRequest, UpdateUserRequest
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

def per_error(msg: dict[str, str], status_code: int) -> None:
    print(f"Error: {msg}")
    print(f"satus_code: {status_code}")
    abort(make_response(jsonify(msg), status_code))

# -------------Endpoints-------------
@app.route("/api/users", methods= ["GET"])
@validate()
def get_users() -> Optional[Response]:
    users = Users.query.all()
    users_serialized = [user.serializer() for user in users]
    if len(users_serialized) == 0:
        per_error(no_users, 404)

    try:
        for validate in users_serialized:
            _ = GeneralDataResponse(**validate)
            my_response = DataResponse(data=users_serialized).dict()
            return make_response(jsonify(my_response), 200)
    except ValidationError:
        per_error(validation_data_error, 500)

@app.route("/api/finduser", methods= ["GET"])
@validate()
def find_user(query: FindUserRequest) -> Optional[Response]:
    clean_dict = {key: value for key, value in query.dict().items() if value is not None}
    users = Users.query.filter_by(**clean_dict).all()
    users_serialized = [user.serializer() for user in users]
    if len(users_serialized) == 0:
        per_error(no_users, 404)

    try:
        for validate in users_serialized:
            _ = GeneralDataResponse(**validate)
            my_response = DataResponse(data=users_serialized).dict()
            return make_response(jsonify(my_response), 200)
    except ValidationError:
        per_error(validation_data_error, 500)

@app.route("/api/adduser", methods= ["POST"])
@validate()
def add_user(body: GeneralDataResponse) -> Optional[Response]:
    try:
        response = body.dict()
        user = Users(**response)
        database.session.add(user)
        database.session.commit()
        response["message"] = "User added successfully"
        return make_response(jsonify(response), 201)
    except Exception as ex:
        per_error({"error": f"The following ERROR occurred in {__file__}: {ex}"}, 500)

@app.route("/api/updateuser", methods= ["PUT"])
@validate()
def update_user(body: UpdateUserRequest) -> Optional[Response]:
    try:
        response = body.dict()
        user = Users.query.filter_by(id=response["id"]).first()
        for key, value in response.items():
            if value is not None:
                setattr(user, key, value)
        database.session.commit()
        response["message"] = "User updated successfully"
        return make_response(jsonify(response), 200)
    except Exception as ex:
        per_error({"error": f"The following ERROR occurred in {__file__}: {ex}"}, 500)

@app.route("/api/deleteuser/<id>", methods= ["DELETE"])
@validate()
def delete_user(id: int) -> Optional[Response]:
    try:
        user = Users.query.filter_by(id=id).first()
        database.session.delete(user)
        database.session.commit()
        response = {
            "id": id,
            "message": "User deleted successfully"
        }
        return make_response(jsonify(response), 200)
    except Exception as ex:
        per_error({"error": f"The following ERROR occurred in {__file__}: {ex}"}, 500)