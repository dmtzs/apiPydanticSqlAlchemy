try:
    from .models import Users
    from typing import Optional
    from app import app, database    
    from flask_pydantic import validate
    from flask import jsonify, make_response, abort, Response
    from .validators import FindUserRequest, AddUserRequest, GeneralDataResponse, DataResponse, DeleteUserRequest
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

def per_error(msg: dict, status_code: int) -> None:
    abort(make_response(jsonify(msg), status_code))

# -------------Endpoints-------------
@app.route("/api/users", methods= ["GET"])
@validate()
def get_users() -> Optional[Response]:
    try:
        users = Users.query.all()
        users_serialized = [user.serializer() for user in users]

        try:
            for validate in users_serialized:
                _ = GeneralDataResponse(**validate)
                my_response = DataResponse(data=users_serialized).dict()
                return make_response(jsonify(my_response), 200)
        except Exception as ex:
            per_error({"error": "Validation error inside data array"}, 500)
    except Exception as ex:
        per_error({"error": f"The following ERROR occurred in {__file__}: {ex}"}, 500)

@app.route("/api/finduser", methods= ["GET"])
@validate()
def find_user(query: FindUserRequest) -> Optional[Response]:
    try:
        clean_dict = {key: value for key, value in query.dict().items() if value is not None}
        users = Users.query.filter_by(**clean_dict).all()
        users_serialized = [user.serializer() for user in users]

        try:
            for validate in users_serialized:
                _ = GeneralDataResponse(**validate)
                my_response = DataResponse(data=users_serialized).dict()
                return make_response(jsonify(my_response), 200)
        except Exception as ex:
            per_error({"error": "Validation error inside data array"}, 500)
    except Exception as ex:
        per_error({"error": f"The following ERROR occurred in {__file__}: {ex}"}, 500)

@app.route("/api/adduser", methods=["POST"])
@validate()
def add_user(body: AddUserRequest):
    try:
        name = body.name
        last_name = body.last_name
        age = body.age
        mail = body.mail

        add_user = Users(name, last_name, age, mail)
        database.session.add(add_user)
        database.session.commit()

        response = add_user.serializer()
        response = GeneralDataResponse(
            rowid=response["rowid"],
            name=response["name"],
            last_name=response["last_name"],
            age=response["age"],
            mail=response["mail"]
        ).dict()

        return make_response(jsonify(response), 200)

    except Exception as ex:
        print(f"The following ERROR occurred in {__file__}: {ex}")
        my_error = {
            "msg": "Internal server error"
        }
        return make_response(jsonify(my_error), 500)

@app.route("/api/deleteuser", methods=["DELETE"])
@validate()
def delete_user(body: DeleteUserRequest):
    try:
        rowid = body.rowid

        single_user = Users.query.filter_by(rowid=rowid).first()
        result = single_user.serializer()

        if not single_user:
            my_error = {
                "msg": "This user doesnt exists"
            }
            return make_response(jsonify(my_error), 404)
        else:
            database.session.delete(single_user)
            database.session.commit()
            response = GeneralDataResponse(
                rowid=result["rowid"],
                name=result["name"],
                last_name=result["last_name"],
                age=result["age"],
                mail=result["mail"],
                message="User deleted"
            ).dict()

            return make_response(jsonify(response), 200)
    except Exception as ex:
        print(f"The following ERROR occurred in {__file__}: {ex}")
        my_error = {
            "msg": "Internal server error"
        }
        return make_response(jsonify(my_error), 500)