from pydantic import BaseModel


class GetTodosRequest(BaseModel):
    """request structure for get request to get user data"""
    pageNo: int
    pageSize: int
    status: str


class SetTodosRequest(BaseModel):
    """request structure to set data"""
    task: str
    status: str
