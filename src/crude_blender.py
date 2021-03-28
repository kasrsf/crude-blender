import numpy as np
import pandas as pd
from pathlib import Path

SAMPLE_DATA_PATH = Path(__file__).parent / "../data/crude_comp_raw_export.CSV"
# the exported csv from crudemonitor has empty rows after
# the first 12 rows which contain the distillation profile
# set a parameter to only read the rows including valid data
CRUDEMONITOR_EXPORT_NUM_ROWS_TO_READ = 12
CRUDEMONITOR_EXPORT_HEADER_ROW = 1
CRUDEMONITOR_EXPORT_NA_VAL = '-'
# the first column in the crudemonitor export has the keys for the
# distillation profile of each crude. This column will be the index
# in the data read which will later be transposed so that the profile
# keys become the columns in the final dataframe
CRUDEMONITOR_EXPORT_INDEX_COL = 0

DISTILLATION_DF_COLUMNS = ['5%', '10%', '20%', '30%', '40%', '50%',
                           '60%', '70%', '80%', '90%', '95%', '99%']
DISTILLATION_DF_INDEX_NAME = 'Name'

def extract_mean_from_confidence_interval(ci):
    """
        Given a string containing the confidence interval for a value (i.e. '1.3 +/- 0.5')
        extract the first value in the string which is the mean and return as a float
        
        Parameters
        ----------
        ci
            string containing the confidence interval
            
        Returns
        -------
        float
            mean value corresponding to the inpput ci
    """
    # if the value is already a mean, return without any changes
    # otherwise extract the first value in the string and cast it as a float
    if type(ci) is float:
       mean = ci
    else:
        mean = float(ci.split()[0])
    return mean
            

def load_from_csv(filepath=SAMPLE_DATA_PATH):
    """
        Given a csv file (which is assumed to be exported from crudemonitor.ca 
        Crude Comparison tool) return a dataframe containing the distillation 
        profiles of the exported crudes. 
        The output dataframe will have the 12 percentage values [ 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
        in the columns and the crude name as the index of the rows.
        Any incomplete profile (e.g. missing values) will be omitted from the output
        
        Parameters
        ----------
        filepath
            location of the csv file to be read
            
        Returns
        -------
        pd.DataFrame
            Dataframe containing the distillation profile of the crudes in the csv file
    """
    data_df = pd.read_csv(filepath, 
                          header=CRUDEMONITOR_EXPORT_HEADER_ROW, 
                          index_col=CRUDEMONITOR_EXPORT_INDEX_COL,
                          nrows=CRUDEMONITOR_EXPORT_NUM_ROWS_TO_READ,
                          na_values=CRUDEMONITOR_EXPORT_NA_VAL)
    # transpose the dataframe so that the crude profiles are the rows
    data_df = data_df.T
    data_df.columns = DISTILLATION_DF_COLUMNS
    data_df.index.name = DISTILLATION_DF_INDEX_NAME
    
    # remove incomplete rows
    data_df = data_df.dropna()
    
    # extract the mean value from the confidence intervals
    data_df = data_df.apply(np.vectorize(extract_mean_from_confidence_interval))
    
    return data_df
