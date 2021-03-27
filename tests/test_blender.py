import pandas as pd
import pytest

EXPECTED_INDEX_NAME = 'Crude'
EXPECTED_COLUMNS = ['5%', '10%', '20%', '30%', '40%', '50%', 
                    '60%', '70%', '80%', '90%', '95%', '99%']


@pytest.fixture(scope='module')
def data():
    """
        Use the crudemonitor sample data to create mock data for testing
    """
    df = pd.DataFrame([
        ['Peace', 43.1, 81.7, 122.8, 165.5, 211.3, 266.7, 323.8, 388.2, 464.5, 582.2, 646.7, 707.1],
        ['Mixed Sweet Blend', 35.9, 75.6, 119.1, 168.1, 225.6, 282.4, 339.7, 402.6, 474.9, 583.0, 652.0, 679.4]
    ])
    df = df.set_index(0)
    df.index.name = EXPECTED_INDEX_NAME
    df.columns = EXPECTED_COLUMNS
    
    return df

def test_test(data):
    assert data.shape[1] == 12