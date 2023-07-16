import pandas as pd
import crud, schemas

def get_date(row, db):
    year = row['text1.year_writing']
    year_from_db = None
    if pd.notna(year) and year != '':
        year_from_db = crud.get_date(db=db, date_id=year)
        if not year_from_db:
            if isinstance(year, float):
                year = str(int(year))
                date_data = schemas.DateOfWritingCreate(**{"exact_year": year})
            elif "—" in year:
                date_data = schemas.DateOfWritingCreate(**{
                    "start_year": int(year.split("—")[0]),
                    "end_year": int(year.split("—")[1]),
                })
            elif "–" in year:
                date_data = schemas.DateOfWritingCreate(**{
                    "start_year": int(year.split("–")[0]),
                    "end_year": int(year.split("–")[1]),
                })
            elif "-" in year:
                start_year, end_year = year.split("-")
                date_data = schemas.DateOfWritingCreate(**{
                    "start_year": int(start_year),
                    "end_year": int(end_year),
                })
            else:
                date_data = schemas.DateOfWritingCreate(**{"exact_year": year})
            year_from_db = crud.create_date(db=db, date=date_data)
        if year_from_db:
            year_from_db = year_from_db.id
    return year_from_db