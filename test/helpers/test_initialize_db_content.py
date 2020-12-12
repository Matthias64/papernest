from app.db_models.operator import Operator
from app.db_models.position import Position
from helpers.initialize_db_content import create_position_from_row, get_positions_from_csv, initialize_positions
from helpers.initialize_db_content import initialize_operators

# noinspection PyUnresolvedReferences
from test.test_fixtures import app, db, session


def test_create_position_from_row():
    input_dict = {"Operateur": "20801", "x": 336338, "y": 674330, "2G": 1, "3G": 0, "4G": 1}
    pos = create_position_from_row(input_dict)
    assert pos is not None
    assert pos.operator_code == "20801"
    assert pos.has_2g
    assert not pos.has_3g
    assert pos.has_4g
    assert pos.location == "SRID=4326;POINT(336338 674330)"


def test_get_positions_from_csv():
    positions = get_positions_from_csv("test/resources/sample_mobile_sites.csv")
    assert len(positions) == 3  # removed one duplicate and #N/A row
    assert positions[-1] is not None
    assert positions[-1].has_2g and positions[-1].has_3g and positions[-1].has_4g
    assert positions[-1].location == "SRID=4326;POINT(-5.088008862939317 48.462881615214336)"


def test_initialize_positions(session):
    initialize_operators(session)
    initialize_positions(session, "test/resources/sample_mobile_sites.csv")
    positions = session.query(Position).all()
    assert len(positions) == 3
    assert positions[0].operator_code == 20801
    assert positions[0].location.srid == 4326
    assert positions[0].has_2g and positions[0].has_3g and not positions[0].has_4g


def test_initialize_operators(session):
    initialize_operators(session)
    operators = session.query(Operator).all()
    assert operators
    assert len(operators) == 4
    assert operators[0].mcc_mnc == 20801
    assert operators[0].name == "Orange"
