from typing import Annotated

from sqlalchemy.orm import mapped_column


class ShortAnnotated:

    _prymary_key_pk = True

    intpk = Annotated[
        int, mapped_column(
            primary_key=_prymary_key_pk
        )]
