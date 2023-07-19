from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from database import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    family = Column(String)
    real_name = Column(String)
    year_birth = Column(String)
    year_death = Column(String)
    gender = Column(String)
    birth_location = Column(String)
    death_location = Column(String)
    texts = relationship('TextBase', back_populates='author')
    variants = relationship('Variant', back_populates='author')
    olds = relationship('Old', back_populates='author')


class Publication(Base):
    __tablename__ = 'publications'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    city = Column(String, nullable=True)
    editor = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    year = Column(String, nullable=True)
    part = Column(String, nullable=True)
    short = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)
    author = relationship('Author')
    textbases = relationship('TextBase', back_populates='publication')
    variants = relationship('Variant', back_populates='publication')


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    texts = relationship('TextBase', back_populates='writing_location')


class TextBase(Base):
    __tablename__ = 'textbases'
    id = Column(Integer, primary_key=True)
    type = Column(String(50))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author')
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    dedication = Column(String, nullable=True)
    author_comment = Column(String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity':'textbase',
        'polymorphic_on':type
    }
    exact_year = Column(Integer, nullable=True)
    exact_month = Column(Integer, nullable=True)
    exact_day = Column(Integer, nullable=True)
    dubious_year = Column(String, nullable=True)
    dubious_month = Column(String, nullable=True)
    dubious_day = Column(String, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    season = Column(String, nullable=True)
    writing_location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    writing_location = relationship('Location', back_populates='texts')
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=True)
    publication = relationship("Publication", back_populates="textbases")
    book_page_start = Column(Integer, nullable=True)
    book_page_end = Column(Integer, nullable=True)


class Text(TextBase):
    __tablename__ = 'texts'
    id = Column(Integer, ForeignKey('textbases.id'), primary_key=True)
    text_id = Column(Integer)  # id from trymysql database
    first_string = Column(String)
    body = Column(String)
    filename = Column(String)
    genre = Column(String)
    n_in_group = Column(Integer)
    group_text_id = Column(Integer, ForeignKey("grouptexts.id"), nullable=True)
    group_text = relationship("GroupText", back_populates="texts", foreign_keys=[group_text_id])
    variants = relationship("Variant", back_populates="variant_of_text", foreign_keys="Variant.variant_of_text_id")
    olds = relationship("Old", back_populates="old_variant_of_text", foreign_keys="Old.old_variant_of_text_id")
    __mapper_args__ = {
        'polymorphic_identity':'text',
    }


class GroupText(TextBase):
    __tablename__ = 'grouptexts'
    id = Column(Integer, ForeignKey('textbases.id'), primary_key=True)
    group_text_id = Column(Integer)
    comment = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    supergroup = Column(String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity':'grouptext',
    }
    texts = relationship("Text", back_populates="group_text", foreign_keys="Text.group_text_id")

class Variant(Base):
    __tablename__ = 'variants'
    id = Column(Integer, primary_key=True)
    first_string = Column(String)
    filename = Column(String)
    body = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author')
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    dedication = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    date = Column(String, nullable=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=True)
    publication = relationship("Publication", back_populates="variants")
    book_page_start = Column(Integer, nullable=True)
    book_page_end = Column(Integer, nullable=True)
    variant_of_text_id = Column(Integer, ForeignKey("texts.id"))
    variant_of_text = relationship("Text", back_populates="variants", foreign_keys=[variant_of_text_id])
    epi_text = Column(String, nullable=True)
    epi_author = Column(String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity':'variant',
    }

class Old(Base):
    __tablename__ = 'olds'
    id = Column(Integer, primary_key=True)
    first_string = Column(String)
    filename = Column(String)
    date = Column(String, nullable=True)
    body = Column(String, nullable=True)
    old_variant_of_text_id = Column(Integer, ForeignKey('texts.id'))
    old_variant_of_text = relationship('Text', back_populates='olds', foreign_keys=[old_variant_of_text_id])
    __mapper_args__ = {
        'polymorphic_identity':'old',
    }
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author')
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    dedication = Column(String, nullable=True)


class Epigraph(Base):
    __tablename__ = 'epigraphs'
    id = Column(Integer, primary_key=True)
    epi_text = Column(String)
    epi_author = Column(String, nullable=True)
    epi_author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)
    epi_author_obj = relationship('Author', back_populates="epigraphs", foreign_keys=[epi_author_id])
    epi_book = Column(String, nullable=True)
    from_text_id = Column(Integer, nullable=True)
    epi_filename = Column(String, nullable=True)
    textbase_id = Column(Integer, ForeignKey('textbases.id'))
    textbase = relationship('TextBase', back_populates='epigraphs')

TextBase.epigraphs = relationship('Epigraph', order_by=Epigraph.id, back_populates='textbase')
Author.epigraphs = relationship('Epigraph', order_by=Epigraph.id, back_populates='epi_author_obj')