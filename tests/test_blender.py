import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
import pytest

from src import crude_blender

EXPECTED_INDEX_NAME = 'Name'
EXPECTED_COLUMNS = ['5%', '10%', '20%', '30%', '40%', '50%', 
                    '60%', '70%', '80%', '90%', '95%', '99%']


@pytest.fixture(scope='module')
def data():
    """
        Use the crudemonitor sample data to create mock data for testing
    """
    df = pd.DataFrame([
        ['Peace', 43.1, 81.7, 122.8, 165.5, 211.3, 266.7, 323.8, 388.2, 464.5, 582.2, 646.7, 707.1],
        ['Mixed Sweet Blend', 35.9, 75.6, 119.1, 168.1, 225.6, 282.4, 339.7, 402.6, 474.9, 583.0, 652.0, 679.4],
        ['Moose Jaw Tops', 53.3, 98.2, 137.3, 168.7, 240.0, 313.5, 354.0, 384.8, 413.8, 452.1, 481.9, 571.5],
        ['Hardisty Synthetic Crude', 82.2, 140.1, 215.1, 258.9, 293.5, 322.7, 351.3, 381.0, 414.5, 457.8, 495.0, 585.0],
        ['CNRL Light Sweet Synthetic', 111.1, 156.1, 209.6, 250.2, 283.4, 312.5, 341.5, 371.2, 405.3, 444.9, 477.1, 550.3],
        ['Suncor Synthetic H', 159.0, 263.0, 324.2, 352.5, 374.4, 394.8, 413.5, 431.6, 454.7, 489.8, 549.2, 615.7]
    ])
    df = df.set_index(0)
    df.index.name = EXPECTED_INDEX_NAME
    df.columns = EXPECTED_COLUMNS
    
    return df

def test_load_from_csv(data):
    """
        check if the data is correctly loaded from the csv export file
    """
    read_data = crude_blender.load_from_csv()
    assert_frame_equal(read_data, data)
    
def test_blend_linear_model():
    """
        check the correctness of the linear combination
    """
    a = pd.Series([1.0, 3.0, 5.0])
    vol_a = 2
    b = pd.Series([2.0, 4.0, 6.0])
    vol_b = 3
    
    expected_res = pd.Series([1.6, 3.6, 5.6])
    res = crude_blender.blend_linear_model(a, vol_a, b, vol_b)
    print(expected_res)
    assert_series_equal(res, expected_res)
    
def test_blend_oils(data):
    oil_1 = 'Peace'
    vol_1 = 2
    oil_2 = 'Suncor Synthetic H'
    vol_2 = 3
    
    res_df = crude_blender.blend_oils(data, oil_1, vol_1, oil_2, vol_2)
    expected_index = "Peace 2l + Suncor Synthetic H 3l"
    # assert correct columns
    assert list(res_df.columns) == EXPECTED_COLUMNS
    
    # assert index
    assert res_df.index == expected_index
