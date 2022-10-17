try:
    from .models import Users
    from app import app, database
    from flask import request, jsonify
    from flask_pydantic import validate
    from .validators import FindUserRequest, AddUserRequest, GeneralDataResponse, DataResponse
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

@app.route("/api/users", methods=["GET"])
@validate()
def get_users():
    try:
        users = Users.query.all()

        response = [user.serializer() for user in users]

        try:
            for validate in response:
                _ = GeneralDataResponse(**validate)
                return DataResponse(
                    data=response
                )
        except Exception as ex:
            print(f"Validation error inside data array: {ex}")
            my_error = {
                "msg": "Error en los objetos json dentro de data"
            }
            return jsonify(my_error), 500
    except Exception as ex:
        print(f"The following ERROR occurred in {__file__}: {ex}")
        my_error = {
            "msg": "Internal server error"
        }
        return jsonify(my_error), 500

@app.route("/api/finduser", methods=["GET"])
@validate()
def get_user(query: FindUserRequest):
    try:
        fields = {}

        if "name" in request.args:
            fields["name"] = query.name
        if "last_name" in request.args:
            fields["last_name"] = query.last_name
        if "age" in request.args:
            fields["age"] = query.age
        
        users = Users.query.filter_by(**fields)

        if not users:
            my_error = {
                "msg": "This user doesnt exists"
            }
            return jsonify(my_error), 200
        else:
            response = [user.serializer() for user in users]

            try:
                for validate in response:
                    _ = GeneralDataResponse(**validate)
            except Exception as ex:
                print(f"Validation error inside data array: {ex}")
                my_error = {
                    "msg": "Error en los objetos json dentro de data"
                }
                return jsonify(my_error), 500

            return DataResponse(
                data=response
            )
    except Exception as ex:
        print(f"The following ERROR occurred in {__file__}: {ex}")
        my_error = {
            "msg": "Internal server error"
        }
        return jsonify(my_error), 500

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

        return GeneralDataResponse(
            rowid=response["rowid"],
            name=response["name"],
            last_name=response["last_name"],
            age=response["age"],
            mail=response["mail"]
        )

    except Exception as ex:
        print(f"The following ERROR occurred in {__file__}: {ex}")
        my_error = {
            "msg": "Internal server error"
        }
        return jsonify(my_error), 500