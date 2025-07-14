from datetime import datetime

from pydantic import  BaseModel,ConfigDict, conint


class CommentInput(BaseModel):
    content: str

class CommentResponse(BaseModel):
    comment_id: int
    content: str
    created_at: datetime
    user_id: int
    recipe_id: int

    model_config = ConfigDict(from_attributes=True)