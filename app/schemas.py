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


class TextBaseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    """Abstract base class for TextBase and GroupTextBase"""
    author_id: int
    title: str | None = None
    subtitle: str | None = None
    author_comment: str | None = None
    dedication: str | None = None
    exact_year: int | None = None
    exact_month: int | None = None
    exact_day: int | None = None
    dubious_year: str | None = None
    dubious_month: str | None = None
    dubious_day: str | None = None
    start_year: int | None = None
    end_year: int | None = None
    season: str | None = None
    writing_location_id: int | None = None
    publication_id: int | None = None
    book_page_start: str | None = None
    book_page_end: str | None = None


class GroupTextBase(TextBaseBase):
    group_text_id: int | None = None
    supergroup: Optional[str]

class GroupTextCreate(GroupTextBase):
    title: str

class GroupTextUpdate(GroupTextBase):
    pass

class GroupTextInDBBase(GroupTextBase):
    id: int
    text_id: int

    class Config:
        orm_mode = True


class TextBase(TextBaseBase):
    text_id: int
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
    text_id: int

    class Config:
        orm_mode = True

class VariantBase(BaseModel):
    first_string: Optional[str] = None
    filename: Optional[str]
    body: Optional[str] = None
    variant_of_text: Optional[TextBase] = None
    variant_of_text_id: int

class VariantCreate(VariantBase):
    filename: str
    variant_of_text_id: int

class VariantUpdate(VariantBase):
    pass

class VariantInDBBase(VariantBase):
    id: int
    variant_of_text_id: int
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
    old_variant_of_text_id: int

    class Config:
        orm_mode = True


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

    class Config:
        orm_mode = True
