from typing import List, Union
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
import models
import schemas

# AuthorSchema CRUD operations
def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()

def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Author).offset(skip).limit(limit).all()

def create_author(db: Session, author: schemas.AuthorBase):
    db_author = models.Author(**author.model_dump())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

# PublicationSchema CRUD operations
def get_publication(db: Session, publication_id: int):
    return db.query(models.Publication).filter(models.Publication.id == publication_id).first()

def get_publication_by_title(db: Session, title: str):
    return db.query(models.Publication).filter(models.Publication.title == title).first()

def create_publication(db: Session, publication: schemas.PublicationBase):
    db_publication = models.Publication(**publication.model_dump())
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication

# LocationSchema CRUD operations
def get_location(db: Session, location_id: int):
    return db.query(models.Location).filter(models.Location.id == location_id).first()

def get_location_by_name(db: Session, name: str):
    return db.query(models.Location).filter(models.Location.name == name).first()

def create_location(db: Session, location: schemas.LocationBase):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def get_date(db: Session, date_id: int):
    return db.query(models.DateOfWriting).filter(models.DateOfWriting.exact_year == date_id).first()

def create_date(db: Session, date: schemas.DateOfWritingBase):
    db_date = models.DateOfWriting(**date.model_dump())
    db.add(db_date)
    db.commit()
    db.refresh(db_date)
    return db_date

# GroupTextSchema CRUD operations
def get_grouptext(db: Session, grouptext_id: int):
    return db.query(models.GroupText).filter(models.GroupText.id == grouptext_id).first()

def get_grouptexts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GroupText).offset(skip).limit(limit).all()

def create_grouptext(db: Session, grouptext: schemas.GroupTextCreate):
    db_grouptext = models.GroupText(**grouptext.__dict__)
    db.add(db_grouptext)
    db.commit()
    db.refresh(db_grouptext)
    return db_grouptext

# TextSchema CRUD operations
def get_text(db: Session, text_id: int) -> models.Text | None:
    return db.query(models.Text).filter(models.Text.id == text_id).first()

def get_texts_by_author(db: Session, author_id: int) -> List[dict]:
    results = db.query(
        models.Text.id,
        models.Text.title,
        models.Text.first_string,
        models.DateOfWriting.exact_year
    ).join(
        models.DateOfWriting, models.Text.date_of_writing_id == models.DateOfWriting.id
    ).filter(
        models.Text.author_id == author_id
    ).all()

    # Convert the results to a list of dictionaries
    texts = [{"id": id, "title": title, "first_string": first_string, "year": year} for id, title, first_string, year in results]

    return texts



def get_texts_count_by_author(db: Session, author_id: int) -> int:
    return db.query(models.Text).filter(models.Text.author_id == author_id).count()

def create_text(db: Session, text: schemas.TextBase):
    db_text = models.Text(**text.model_dump())
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text

# VariantSchema CRUD operations
def get_variant(db: Session, variant_id: int):
    return db.query(models.Variant).filter(models.Variant.id == variant_id).first()

def create_variant(db: Session, variant: schemas.VariantBase):
    db_variant = models.Variant(**variant.model_dump())
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant

# OldSchema CRUD operations
def get_old(db: Session, old_id: int):
    return db.query(models.Old).filter(models.Old.id == old_id).first()

def create_old(db: Session, old: schemas.OldBase):
    db_old = models.Old(**old.model_dump())
    db.add(db_old)
    db.commit()
    db.refresh(db_old)
    return db_old

# EpigraphSchema CRUD operations
def get_epigraph(db: Session, epigraph_id: int):
    return db.query(models.Epigraph).filter(models.Epigraph.id == epigraph_id).first()

def create_epigraph(db: Session, epigraph: schemas.EpigraphBase):
    db_epigraph = models.Epigraph(**epigraph.model_dump())
    db.add(db_epigraph)
    db.commit()
    db.refresh(db_epigraph)
    return db_epigraph
