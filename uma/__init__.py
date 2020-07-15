import numpy as np
import pyomo.environ as pyomo
import pandas as pd

__version__ = 0.1
__author__ = "Digvijay Gusain"

def get_df(model):
    """
    Return pyomo results as pandas dataframe
    Usage: 
        df1 = uma.get_df(model.variable)
    """
    df = pd.DataFrame()
    df_dict = {v.name: np.array([v[index].value for index in v]) for v in 
               model.component_objects(pyomo.Var, active=True)}
    max_length = max([len(i) for i in df_dict.values()])
    for i,j in df_dict.items():
        j=list(j)
        while len(j) < max_length:
            j.append(np.NaN)
        df.loc[:, i] = np.asarray(j)
    
    return df

def get_dict(model):
    """
    Return pyomo results as dictionary
    Usage: 
        dict1 = uma.get_dict(model.variable)
    """
    df_dict = {v.name: np.array([v[index].value for index in v]) for v in 
               model.component_objects(pyomo.Var, active=True)}
    return df_dict

def get_value(x):
    '''
    Returns value of a variable.
    Usage: 
        var1 = uma.get_value(model.variable)
    '''
    return np.asarray(list(x.extract_values().values()))