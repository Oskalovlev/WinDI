from pydantic import BaseModel


class PydanticBaseSchema(BaseModel):

    pass


class PydanticIntIDSchema(BaseModel):

    id: int
