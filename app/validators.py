try:
    from typing import Optional
    from pydantic import BaseModel
except ImportError as e_imp:
    print(f"The following import ERROR occurred in {__file__}: {e_imp}")

class GeneralDataResponse(BaseModel):
    id: int
    username: str
    password: str
    last_name: str
    age: int

class DataResponse(BaseModel):
    data: list[dict]

class FindUserRequest(BaseModel):
    username: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None

class UpdateUserRequest(BaseModel):
    id: int
    username: Optional[str] = None
    password: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None