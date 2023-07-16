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


class DateOfWritingBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    exact_year: Optional[int] = None
    exact_month: Optional[int] = None
    exact_day: Optional[int] = None
    dubious_year: Optional[int] = None
    dubious_month: Optional[int] = None
    dubious_day: Optional[int] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    season: Optional[str] = None

class DateOfWritingCreate(DateOfWritingBase):
    pass


class DateOfWritingUpdate(DateOfWritingBase):
    pass

class DateOfWritingInDBBase(DateOfWritingBase):
    id: int

    class Config:
        orm_mode = True


class TextBaseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    """Abstract base class for TextBase and GroupTextBase"""
    author_id: int
    title: str | None = None
    subtitle: str | None = None
    author_comment: str | None = None
    dedication: str | None = None
    date_of_writing_id: int | None = None
    writing_location_id: int | None = None
    publication_id: int | None = None
    book_page_start: str | None = None
    book_page_end: str | None = None


class GroupTextBase(TextBaseBase):
    supergroup: Optional[str]

class GroupTextCreate(GroupTextBase):
    title: str

class GroupTextUpdate(GroupTextBase):
    pass

class GroupTextInDBBase(GroupTextBase):
    id: int

    class Config:
        orm_mode = True


class TextBase(TextBaseBase):
    first_string: Optional[str] = None
    body: Optional[str] = None
    filename: Optional[str]
    n_in_group: int = None
    group_text_id: int | None = None

class TextCreate(TextBase):
    body: str

class TextUpdate(TextBase):
    pass

class TextInDBBase(TextBase):
    id: int

    class Config:
        orm_mode = True

class VariantBase(TextBaseBase):
    first_string: Optional[str] = None
    filename: Optional[str]
    text_variant_of: Optional[TextBase] = None

class VariantCreate(VariantBase):
    filename: str


class OldBase(TextBaseBase):
    first_string: Optional[str] = None
    filename: Optional[str]
    text_variant_of: Optional[TextBase] = None

class OldSchema(OldBase):
    id: int


class EpigraphBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    epi_text: Optional[str] = None
    epi_author: Optional[str] = None
    epi_book: Optional[str] = None
    epi_filename: Optional[str] = None
    textbase_id: Optional[int] = None

class EpigraphCreate(EpigraphBase):
    epi_text: str

class EpigraphSchema(EpigraphBase):
    id: int


