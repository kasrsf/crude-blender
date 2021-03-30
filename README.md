# Crude Blender

The Distillation Profile of an oil determines the temperatures (in °C) at which specific percentages of the oil will evaporate. This profile is represented in key-values of percentages and temperatures for given temperatures [ 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99].

The purpose of this package is to approximate the distillation profile of two different oils given their distillation profile.

**Assumption:** I've assumed that the blending of the two oils won't affect the profiles of the oils themselves and the profiles will remain **independent** throughout the blending process. This simplification allows us to be able to model the distillation of the final product as a linear combination of the two oils that are combined proportional to their volumes. 

When mixing oils `vol1` liters of `oil1` and `vol2` liters of `oil2` with distillation profiles represented by `oil1[p]=temp at which p% of oil has evaporated`, the distillation profile of the blended oil `blend` can be modeled by:

```
blend[p] = ((vol1 * oil1[p]) + (vol2 * oil2[p])) / (vol1 + vol2)
```

This model is a simplification of the process as the oils will definitely affect eachother during the blending process based on their chemistery and other properties. Given this point, the code is implemented in a way where we can replace the linear model with more sophisticated models without the change affecting other areas of the code. In order to change the model, we can replace the function `blend_linear_model` in `blend_oils` and given the correct output shape, the rest of code will remain unchanged as I have seperated the model logic from the data processing logic.

## Data

In order to test the implementation, the distillation profiles of 10 crude oils was downloaded using the [Crude Comparison](https://crudemonitor.ca/tools/comp/) tool provided by *crudemonitor.ca*. The exported data used for this example can be observed at `data/crude_comp_raw_export.CSV`.

During the data preprocessing stage, any oils with missing data are removed and for the rest of the data, the values are extracted for the data to be in the shape `oil[p]=temp at which p% of oil has evaporated`.

## Process

The modeling and data processing functions are implemented at `src/crude_blender.py`. There are two main functions:

* `load_from_csv` will read and clean the distillation profile and return the clean data in the form of pandas DataFrames.
(**Assumption:** the data extraction process is implemented based on the assumption that the input data is always the extract of crude monitor crude comparison tool and thus has tailored logic for these extracts. Data from other sources with different sources will require the implementation of custom preprocessing functions.)

* `blend_oils` will output the distillation profile of blending of two oils with any volumes given their distillation profiles. As mentioned above, the output is calculated by using a linear model.

## Usage

The code was implemented and tested in **Python 3.8.5**. The required packages for running the script are listed in the `requirements.txt` file. These requirements can be installed by:

```
pip install -r requirements.txt
```

A sample script `example.py` has been provided which demonstrates the usage of the functions:

```
from src import crude_blender

distil_profiles = crude_blender.load_from_csv()
blend_profile = crude_blender.blend_oils(distil_profiles, 'Mixed Sweet Blend', 2, 'CNRL Light Sweet Synthetic', 4)
```

## Testing

The implementation is tested using unit tests implemented with `pytest`. To rerun the tests run the following command in the root folder of the project:

```
pytest
```

