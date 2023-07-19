from typing import List
from sqlalchemy.orm import Session
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

def get_publications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Publication).offset(skip).limit(limit).all()

def get_publication_by_title(db: Session, title: str):
    return db.query(models.Publication).filter(models.Publication.title == title).first()

def create_publication(db: Session, publication: schemas.PublicationBase):
    db_publication = models.Publication(**publication.model_dump())
    db.add(db_publication)
    db.commit()
    db.refresh(db_publication)
    return db_publication

# LocationSchema CRUD operations
def get_location(db: Session, location_id: int) -> schemas.LocationInDBBase | None:
    return db.query(models.Location.name).filter(models.Location.id == location_id).first()

def get_location_by_name(db: Session, name: str) -> schemas.LocationInDBBase | None:
    return db.query(models.Location).filter(models.Location.name==name).first()

def get_locations(db: Session, skip: int = 0, limit: int = 100) -> List[tuple]:
    return db.query(models.Location.id, models.Location.name).offset(skip).all()

def create_location(db: Session, location: schemas.LocationBase):
    db_location = models.Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location


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
    return db.query(models.Text).filter(models.Text.text_id == text_id).first()

def get_texts_by_author(db: Session, author_id: int) -> List[models.Text]:
    return db.query(models.Text).filter(models.Text.author_id == author_id).all()

def get_texts_by_author_with_group(db: Session, author_id: int) -> List[dict]:
    results = (
        db.query(
            models.Text.text_id,
            models.Text.title,
            models.Text.first_string,
            models.Text.exact_year,
            models.GroupText.title.label("group_text_title")
        )
        .outerjoin(models.Text.group_text)
        .filter(models.Text.author_id == author_id)
        .all()
    )
    return [
        {
            "id": res.text_id,
            "title": res.title,
            "first_string": res.first_string,
            "exact_year": res.exact_year,
            "group_text_title": res.group_text_title,
        }
        for res in results
    ]

def get_new_text_id_by_old_id(db: Session, old_id: int) -> int | None:
    return db.query(models.Text).filter(models.Text.text_id == old_id).first().id

def get_texts_count_by_author(db: Session, author_id: int) -> int:
    return db.query(models.Text).filter(models.Text.author_id == author_id).count()

def create_text(db: Session, text: schemas.TextBase):
    db_text = models.Text(**text.model_dump())
    db.add(db_text)
    db.commit()
    db.refresh(db_text)
    return db_text

# VariantSchema CRUD operations
def get_variant(db: Session, id) -> models.Variant | None:
    return db.query(models.Variant).filter(models.Variant.id == id).first()

def get_variants_for_text_id(db: Session, text_id: int) -> list:
    res = db.query(models.Variant).filter(models.Variant.variant_of_text_id == text_id).all()
    return db.query(models.Variant).filter(models.Variant.variant_of_text_id == text_id).all()

def create_variant(db: Session, variant: schemas.VariantBase):
    db_variant = models.Variant(**variant.model_dump())
    db.add(db_variant)
    db.commit()
    db.refresh(db_variant)
    return db_variant


# OldSchema CRUD operations
def get_old(db: Session, id) -> models.Old | None:
    return db.query(models.Old).filter(models.Old.id == id).first()

def get_old_for_text(db: Session, text_id: int) -> models.Old | None:
    return db.query(models.Old).filter(models.Old.old_variant_of_text_id == text_id).first()

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
