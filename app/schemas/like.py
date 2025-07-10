
from pydantic import  BaseModel,ConfigDict, conint


class Like(BaseModel):
    dir:conint(ge=0,le=1)

class LikeResponse(BaseModel):
    message: str

    model_config = ConfigDict(from_attributes=True)