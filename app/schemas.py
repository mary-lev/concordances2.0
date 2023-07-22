from typing import Optional
from pydantic import BaseModel, ConfigDict
from typing import List

class AuthorBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    surname: Optional[str] = None
    family: Optional[str] = None
    real_name: Optional[str] = None
    year_birth: Optional[str] = None
    year_death: Optional[str] = None
    gender: Optional[str] = None
    birth_location: Optional[str] = None
    death_location: Optional[str] = None

class AuthorCreate(AuthorBase):
    name: str

class AuthorUpdate(AuthorBase):
    pass

class AuthorInDBBase(AuthorBase):
    id: int

    class Config:
        orm_mode = True

class PublicationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: Optional[str]
    city: Optional[str] = None
    editor: Optional[str] = None
    publisher: Optional[str] = None
    year: Optional[str] = None
    part: Optional[str] = None
    short: Optional[str] = None
    author_id: Optional[int] = None


class PublicationCreate(PublicationBase):
    title: str

class PublicationUpdate(PublicationBase):
    pass

class PublicationInDBBase(PublicationBase):
    id: int
    title: str

    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class LocationCreate(LocationBase):
    name: str

class LocationUpdate(LocationBase):
    pass

class LocationInDBBase(LocationBase):
    id: int

    class Config:
        orm_mode = True

class TextDateBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    year: Optional[int] = None
    month: Optional[int] = None
    day: Optional[int] = None
    dubious_year: Optional[str] = None
    dubious_month: Optional[str] = None
    dubious_day: Optional[str] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    season: Optional[str] = None
    comment: Optional[str] = None


class TextDateCreate(TextDateBase):
    pass

class TextDateUpdate(TextDateBase):
    pass

class TextDateInDBBase(TextDateBase):
    id: int
    year: int
    month: int
    day: int
    dubious_day: str
    dubious_month: str
    dubious_year: str
    start_year: int
    end_year: int
    season: str

    class Config:
        orm_mode = True


class GroupTextBase(BaseModel):
    supergroup: Optional[str]
    location_id: Optional[int] = None
    location: Optional[LocationBase] = None
    author_id: int
    title: str | None = None
    dedication: str | None = None
    subtitle: str | None = None
    author_comment: str | None = None
    text_date_id: int | None = None
    location_id: int | None = None


class GroupTextCreate(GroupTextBase):
    title: str

class GroupTextUpdate(GroupTextBase):
    pass

class GroupTextInDBBase(GroupTextBase):
    id: int

    class Config:
        orm_mode = True


class TextBase(BaseModel):
    text_id: int
    title: str | None = None
    subtitle: str | None = None
    first_string: Optional[str] = None
    body: Optional[str] = None
    filename: Optional[str]
    n_in_group: int = None
    author: Optional[AuthorBase] = None
    author_id: int
    author_comment: str | None = None
    dedication: str | None = None
    group_text_id: Optional[int] = None
    group_text: Optional[GroupTextBase] = None
    publication_id: Optional[int] = None
    publication: Optional[PublicationBase] = None
    location_id: Optional[int] = None
    location: Optional[LocationBase] = None
    text_date_id: Optional[int] = None
    text_date: Optional[TextDateBase] = None


class TextCreate(TextBase):
    body: str

class TextUpdate(TextBase):
    pass

class TextInDBBase(TextBase):
    id: int
    text_id: int
    publication: Optional[PublicationBase] = None
    publication_id: Optional[int] = None

    class Config:
        orm_mode = True


class EpigraphBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    epi_text: Optional[str] = None
    epi_author: Optional[str] = None
    epi_book: Optional[str] = None
    epi_filename: Optional[str] = None
    text_id: Optional[int] = None

class EpigraphCreate(EpigraphBase):
    epi_text: str

class EpigraphSchema(EpigraphBase):
    id: int

    class Config:
        orm_mode = True

class VariantBase(BaseModel):
    first_string: Optional[str] = None
    filename: Optional[str] = None
    body: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    author_comment: Optional[str] = None
    dedication: Optional[str] = None
    year: Optional[str|int] = None
    date: Optional[str] = None
    publication_id: Optional[int] = None
    publication: Optional[PublicationBase] = None
    location_id: Optional[int] = None
    location: Optional[LocationBase] = None
    book_page_start: Optional[int] = None
    book_page_end: Optional[int] = None
    variant_of_text: Optional[TextBase] = None
    variant_of_text_id: int
    epi_text: Optional[str] = None
    epigraph: Optional[EpigraphBase] = None
    epi_author: Optional[str] = None
    author: Optional[AuthorBase] = None
    author_id: int
    text_date_id: Optional[int] = None
    text_date: Optional[TextDateBase] = None

class VariantCreate(VariantBase):
    filename: str
    variant_of_text_id: int

class VariantUpdate(VariantBase):
    pass

class VariantInDBBase(VariantBase):
    id: int

    class Config:
        orm_mode = True


class OldBase(BaseModel):
    first_string: Optional[str] = None
    filename: Optional[str]
    date: Optional[str] = None
    body: Optional[str] = None
    old_variant_of_text: Optional[TextBase] = None
    old_variant_of_text_id: int


class OldCreate(OldBase):
    filename: str

class OldUpdate(OldBase):
    pass

class OldInDBBase(OldBase):
    id: int

    class Config:
        orm_mode = True


