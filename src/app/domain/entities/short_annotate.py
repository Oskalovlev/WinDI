from typing import Annotated

from sqlalchemy import Integer
from sqlalchemy.orm import mapped_column


class ShortAnnotated:

    _prymary_key_pk = True
    _autoincrement = True
    _index = False

    intpk = Annotated[
        int, mapped_column(
            Integer,
            primary_key=_prymary_key_pk,
            autoincrement=_autoincrement,
            index=_index
        )]
