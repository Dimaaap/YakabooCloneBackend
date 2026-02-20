from pydantic import BaseModel, ConfigDict

from datetime import datetime

class EmailSubs(BaseModel):
    email: str
    date_sub: datetime


class EmailSubsForAdminList(EmailSubs):
    model_config = ConfigDict(from_attributes=True)

    id: int