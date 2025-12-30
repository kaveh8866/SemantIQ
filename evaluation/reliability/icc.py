import numpy as np
import pandas as pd

def calculate_icc(data, icc_type='icc2k'):
    """
    Calculate Intraclass Correlation Coefficient.
    
    Args:
        data (pd.DataFrame): A dataframe where rows are subjects and columns are raters.
                             Values are the ratings.
        icc_type (str): 'icc2' (single rater) or 'icc2k' (average of k raters).
                        Model 2: Random effects for both subjects and raters.
                        
    Returns:
        float: The ICC value.
    """
    # Remove rows with missing data for standard ICC
    df_clean = data.dropna()
    
    n, k = df_clean.shape
    if n < 2 or k < 2:
        return np.nan
        
    # Grand mean
    grand_mean = df_clean.values.mean()
    
    # Sum of squares
    SST = ((df_clean.values - grand_mean) ** 2).sum()
    
    # Between-subjects sum of squares
    row_means = df_clean.mean(axis=1)
    SSR = k * ((row_means - grand_mean) ** 2).sum()
    
    # Between-raters sum of squares
    col_means = df_clean.mean(axis=0)
    SSC = n * ((col_means - grand_mean) ** 2).sum()
    
    # Residual sum of squares
    SSE = SST - SSR - SSC
    
    # Mean squares
    MSR = SSR / (n - 1)
    MSC = SSC / (k - 1)
    MSE = SSE / ((n - 1) * (k - 1))
    
    if icc_type == 'icc2':
        # ICC(2,1): Single random rater, absolute agreement
        # Formula: (MSR - MSE) / (MSR + (k-1)MSE + k(MSC-MSE)/n)
        numerator = MSR - MSE
        denominator = MSR + (k - 1) * MSE + (k * (MSC - MSE) / n)
        return numerator / denominator
        
    elif icc_type == 'icc2k':
        # ICC(2,k): Average of k random raters, absolute agreement
        # Formula: (MSR - MSE) / (MSR + (MSC - MSE)/n)
        numerator = MSR - MSE
        denominator = MSR + (MSC - MSE) / n
        return numerator / denominator
        
    else:
        raise ValueError(f"Unsupported ICC type: {icc_type}")
