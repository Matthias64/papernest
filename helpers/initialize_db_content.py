import pandas as pd
import pyproj

from app.db_models.operator import Operator
from app.db_models.position import Position


def initialize_demo_db_content(db):
    """Reset the table contents to default values for testing purposes"""
    Position.query.delete()
    Operator.query.delete()
    db.session.commit()
    initialize_operators(db.session)
    db.session.commit()
    initialize_positions(db.session, "resources/2018_01_Sites_mobiles_2G_3G_4G_France_metropolitaine_L93.csv")
    db.session.commit()


def create_position_from_row(row):
    """Create a Position DB item from a CSV row in dict format"""
    return Position(operator_code=row["Operateur"],
                    location='SRID={};POINT({} {})'.format(Position.SRS_WGS_84, row["x"], row["y"]),
                    has_2g=bool(row["2G"]), has_3g=bool(row["3G"]), has_4g=bool(row["4G"]))


def get_positions_from_csv(csv_path, delimiter=";"):
    """
    Gets a csv file containing x,y coordinates in LAMBERT format, remove duplicates (operateur, x and y)
    and creates Position DB objects with coordinates in GPS format(long, lat)
    :param csv_path: input csv path
    :param delimiter: csv delimiter
    :return: 
    """
    df = pd.read_csv(csv_path, delimiter=delimiter)
    df.dropna(inplace=True)
    df.drop_duplicates(subset=["x", "y", "Operateur"], inplace=True, keep="last")
    lambert_proj = pyproj.Proj('+proj=lcc +lat_1=49 +lat_2=44 +lat_0=46.5 +lon_0=3 '
                               '+x_0=700000 +y_0=6600000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs')
    wgs84_proj = pyproj.Proj('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
    df["x"], df["y"] = pyproj.transform(lambert_proj, wgs84_proj, df["x"], df["y"])
    return df.apply(create_position_from_row, axis=1).tolist()


def initialize_positions(session, csv_path):
    """Add the default positions to the DB for testing purposes"""
    positions = get_positions_from_csv(csv_path)
    session.add_all(positions)


def initialize_operators(session):
    """Add the default French operators to the DB for testing purposes"""
    default_operators = {20801: "Orange", 20810: "SFR", 20815: "Free", 20820: "Bouygues"}
    for mcc_mnc, name in default_operators.items():
        session.add(Operator(mcc_mnc=mcc_mnc, name=name))
