from pydantic import BaseModel, ConfigDict


class EmailSubBase(BaseModel):
    email: str


class EmailSubCreate(EmailSubBase):
    pass


class CheckEmail(EmailSubBase):
    pass


class EmailSubUpdate(EmailSubCreate):
    pass


class EmailSubSchema(EmailSubBase):
    model_config = ConfigDict(from_attributes=True)

    id: int