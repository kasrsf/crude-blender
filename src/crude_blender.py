#%%
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


def blend_linear_model(first_crude_profile,
                       first_volume,
                       second_crude_profile,
                       second_volume):
    """
        Given two series which contain the distillation profiles for the crudes
        to be combined and their respective volumes in the blend, calculate the
        estimated distillation profile of the blend using a linear model
        
        Parameters
        ----------
        first_crude_profile
            the distillation profile corresponding to the first crude in the mix
        first_volume
            the volume of the first oil that's being added to the mix
        second_crude_profile
            the distillation profile corresponding to the second crude in the mix
        second_volume
            the volume of the second oil that's being added to the mix
    
        Returns
        -------
        pd.Series
            the linear combination of the two profiles with the volumes
    """
    assert len(first_crude_profile) == len(second_crude_profile), "the two series should have the same length"
    total_volume = first_volume + second_volume
    linear_blend_profile = (
        (first_crude_profile * first_volume + second_crude_profile * second_volume)
        / total_volume
    )
    # round the results to two decimals
    return round(linear_blend_profile, 2)
    
def blend_oils(distillation_profiles, oil_1, vol_1, oil_2, vol_2):
    """
        Given the distillation profiles and the two oils to be blended,
        output a dataframe containing information about the combination
        and its distillation profile
        
        Parameters
        ----------
        distillation_profiles
            Pandas DataFrame containing the distillation profiles available for the oils
        oil_1
            name of the first oil to be mixed
        vol_1
            volume of the first oil in the blend (in liters)
        oil_2
            name of the second oil to be mixed
        vol_2
            volume of the second oil in the blend (in liters)
            
        Returns
        -------
        pd.DataFrame
            a DataFrame with columns indicating the distillation profile
    """
    assert oil_1 in distillation_profiles.index, f"distillation profile for {oil_1} not present in data"
    assert oil_2 in distillation_profiles.index, f"distillation profile for {oil_2} not present in data"
    oil_1_profile, oil_2_profile = distillation_profiles.loc[oil_1], distillation_profiles.loc[oil_2]
    
    blend_profile = blend_linear_model(oil_1_profile, vol_1, oil_2_profile, vol_2)
    blend_profile.name = f"{oil_1} {vol_1}l + {oil_2} {vol_2}l"
    blend_profile_pd = pd.DataFrame(blend_profile).T
    blend_profile_pd.index.name = DISTILLATION_DF_INDEX_NAME
    return blend_profile_pd
