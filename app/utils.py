import pandas as pd
import crud
import schemas


def parse_year(year):
    if isinstance(year, float):
        return year, None, None
    start_year = None
    end_year = None
    if "—" in year:
        start_year = int(year.split("—")[0])
        end_year = int(year.split("—")[1])
    elif "–" in year:
        start_year = int(year.split("–")[0])
        end_year = int(year.split("–")[1])
    elif "-" in year:
        start_year, end_year = year.split("-")
    if start_year:
        year = start_year
    return int(year), start_year, end_year


def parse_to_int(value):
    if not value:
        return None
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        return int(value.strip())
    return value


def get_date(row, db, table_name):
    year = row.get(f'{table_name}.year_writing')
    month = row.get(f'{table_name}.month_writing')
    day = row.get(f'{table_name}.day_writing')
    dyear = row.get(f'{table_name}.dyear_writing')
    dmonth = row.get(f'{table_name}.dmonth_writing')
    dday = row.get(f'{table_name}.dday_writing')
    season = row.get(f'{table_name}.season_writing')
    if table_name == 'group_text':
        year = row["group_text.year_writing"]
    if pd.notna(year) and year != '':
        year, start_year, end_year = parse_year(year)
        date = crud.get_exact_date(
            db=db,
            year=parse_to_int(year),
            month=parse_to_int(month),
            day=parse_to_int(day),
            dubious_year=dyear,
            dubious_month=dmonth,
            dubious_day=dday,
            season=season,
            start_year=start_year,
            end_year=end_year,
        )
        if not date:
            date_data = schemas.TextDateCreate(**{
                "year": parse_to_int(year),
                "month": parse_to_int(month),
                "day": parse_to_int(day),
                "dubious_year": dyear,
                "dubious_month": dmonth,
                "dubious_day": dday,
                "season": season,
                "start_year": start_year,
                "end_year": end_year,
            })
            date = crud.create_date(db=db, date=date_data)
        return date.id
    return None
