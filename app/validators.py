try:
    from typing import Optional
    from pydantic import BaseModel
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

class FindUserRequest(BaseModel):
    name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None

class AddUserRequest(BaseModel):
    name: str
    last_name: str
    age: int
    mail: str

class GeneralDataResponse(BaseModel):
    rowid: int
    name: str
    last_name: str
    age: int
    mail: str

class DataResponse(BaseModel):
    data: list[dict]