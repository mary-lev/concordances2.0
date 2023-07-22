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
    texts = relationship('Text', back_populates='author', foreign_keys='Text.author_id')
    group_texts = relationship('GroupText', back_populates='author', foreign_keys='GroupText.author_id')
    variants = relationship('Variant', back_populates='author', foreign_keys='Variant.author_id')
    olds = relationship('Old', back_populates='author', foreign_keys='Old.author_id')


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
    texts = relationship('Text', back_populates='publication',
                         foreign_keys='Text.publication_id')
    variants = relationship(
        'Variant', back_populates='publication', foreign_keys='Variant.publication_id')


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    country = Column(String, nullable=True)
    city = Column(String, nullable=True)
    address = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    texts = relationship('Text', back_populates='location', foreign_keys='Text.location_id')
    variants = relationship('Variant', back_populates='location', foreign_keys='Variant.location_id')
    group_texts = relationship('GroupText', back_populates='location', foreign_keys='GroupText.location_id')

class TextDate(Base):
    __tablename__ = 'textdates'
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)
    dubious_year = Column(String, nullable=True)
    dubious_month = Column(String, nullable=True)
    dubious_day = Column(String, nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)
    season = Column(String, nullable=True)
    comment = Column(String, nullable=True)
    texts = relationship('Text', back_populates='text_date', foreign_keys='Text.text_date_id')
    variants = relationship('Variant', back_populates='text_date', foreign_keys='Variant.text_date_id')
    group_texts = relationship('GroupText', back_populates='text_date', foreign_keys='GroupText.text_date_id')



class Text(Base):
    __tablename__ = 'texts'
    id = Column(Integer, primary_key=True)
    text_id = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    body = Column(String)
    filename = Column(String)
    first_string = Column(String)
    source = Column(String, nullable=True)
    genre = Column(String)
    dedication = Column(String, nullable=True)
    author_comment = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=True)
    author = relationship('Author', back_populates='texts', foreign_keys=[author_id])
    n_in_group = Column(Integer)
    group_text_id = Column(Integer, ForeignKey("grouptexts.id"), nullable=True)
    group_text = relationship("GroupText", back_populates="texts", foreign_keys=[group_text_id])
    variants = relationship("Variant", back_populates="variant_of_text", foreign_keys="Variant.variant_of_text_id")
    olds = relationship("Old", back_populates="old_variant_of_text", foreign_keys="Old.old_variant_of_text_id")
    __mapper_args__ = {
        'polymorphic_identity': 'text',
    }
    publication_id = Column(Integer, ForeignKey("publications.id"), nullable=True)
    publication = relationship("Publication", back_populates="texts", foreign_keys=[publication_id])
    book_page_start = Column(Integer, nullable=True)
    book_page_end = Column(Integer, nullable=True)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    location = relationship('Location', back_populates='texts', foreign_keys=[location_id])
    epigraphs = relationship("Epigraph", back_populates="text", foreign_keys="Epigraph.text_id")
    text_date_id = Column(Integer, ForeignKey('textdates.id'), nullable=True)
    text_date = relationship('TextDate', back_populates='texts', foreign_keys=[text_date_id])


class GroupText(Base):
    __tablename__ = 'grouptexts'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    filename = Column(String)
    genre = Column(String)
    dedication = Column(String, nullable=True)
    author_comment = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('Author', back_populates="group_texts", foreign_keys=[author_id])
    comment = Column(String, nullable=True)
    supergroup = Column(String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'grouptext',
    }
    texts = relationship("Text", back_populates="group_text", foreign_keys="Text.group_text_id")
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    location = relationship('Location', back_populates='group_texts', foreign_keys=[location_id])
    text_date_id = Column(Integer, ForeignKey('textdates.id'), nullable=True)
    text_date = relationship('TextDate', back_populates='group_texts', foreign_keys=[text_date_id])


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
    publication = relationship("Publication", back_populates="variants", foreign_keys=[publication_id])
    book_page_start = Column(Integer, nullable=True)
    book_page_end = Column(Integer, nullable=True)
    variant_of_text_id = Column(Integer, ForeignKey("texts.id"))
    variant_of_text = relationship("Text", back_populates="variants", foreign_keys=[variant_of_text_id])
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=True)
    location = relationship(
        'Location', back_populates='variants', foreign_keys=[location_id])
    epi_text = Column(String, nullable=True)
    epi_author = Column(String, nullable=True)
    __mapper_args__ = {
        'polymorphic_identity': 'variant',
    }
    text_date_id = Column(Integer, ForeignKey('textdates.id'), nullable=True)
    text_date = relationship('TextDate', back_populates='variants', foreign_keys=[text_date_id])


class Old(Base):
    __tablename__ = 'olds'
    id = Column(Integer, primary_key=True)
    first_string = Column(String)
    filename = Column(String)
    date = Column(String, nullable=True)
    body = Column(String, nullable=True)
    old_variant_of_text_id = Column(Integer, ForeignKey('texts.id'))
    old_variant_of_text = relationship(
        'Text', back_populates='olds', foreign_keys=[old_variant_of_text_id])
    __mapper_args__ = {
        'polymorphic_identity': 'old',
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
    epi_author_obj = relationship(
        'Author', back_populates="epigraphs", foreign_keys=[epi_author_id])
    epi_book = Column(String, nullable=True)
    from_text_id = Column(Integer, nullable=True)
    epi_filename = Column(String, nullable=True)
    text_id = Column(Integer, ForeignKey('texts.id'))
    text = relationship('Text', back_populates='epigraphs',
                        foreign_keys=[text_id])


Text.epigraphs = relationship(
    'Epigraph', order_by=Epigraph.id, back_populates='text')
Author.epigraphs = relationship(
    'Epigraph', order_by=Epigraph.id, back_populates='epi_author_obj')
