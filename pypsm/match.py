import pandas as pd

from pypsm import matcher as m

def match(data, treatment_column, is_csv=False, output_csv=None):
    """
    Wrapper function that returns propensity score matched data.

    This function takes in data as a csv file or pandas dataframe and 
    returns a pandas dataframe of propensity score matched data according
    to the treatment column. 
    -------
    Inputs:
    - data = pandas dataframe or csv file (depending on is_csv param) 
             with fully cleaned data (see demo or README)
    - treatment_column = string of column corresponding to treatment group,
                         values should be binary with 1 representing
                         minority treatment group
    - is_csv = boolean flag indicating that is True when data is csv
    - ouput_csv = directory where to output matched dataframe, None 
                  representing no csv output (default None)

    Outputs:
    - matched_data = pandas dataframe of treatment group and matched 
                     control group
    """

    if is_csv:
        data = pd.read_csv(data)
    
    matcher = m.Matcher(data, treatment_column)
    matched_data = matcher.compute_matched_data()

    if output_csv is not None:
        matched_data.to_csv(output_csv,index_label='index')

    return matched_data

    