import numpy as np

def calculate_krippendorff_alpha(data, level_of_measurement='interval'):
    """
    Calculate Krippendorff's Alpha.
    
    Args:
        data (np.ndarray or list of lists): Matrix of ratings where rows are units (subjects)
                                            and columns are raters. 
                                            Wait, standard format for Krippendorff is usually
                                            rows=raters, cols=units. 
                                            Let's standardize on: Rows = Subjects, Cols = Raters 
                                            to match our ICC implementation, then transpose internally.
        level_of_measurement (str): 'interval', 'nominal', 'ordinal', 'ratio'.
                                    Currently only 'interval' is implemented.
                                    
    Returns:
        float: The alpha value.
    """
    
    # Convert to numpy array
    # Input: Rows=Subjects, Cols=Raters.
    # Krippendorff standard: Rows=Raters, Cols=Units (Subjects).
    # So we transpose.
    matrix = np.array(data).T
    
    # Check for missing values (np.nan)
    # If no missing values, it's simpler, but this metric is designed for missing data.
    
    n_raters, n_units = matrix.shape
    
    if n_units < 2:
        return np.nan
        
    # Helper to calculate difference function
    def diff_sq(v1, v2):
        return (v1 - v2) ** 2

    # Flatten the reliability matrix to get all values
    values = []
    for r in range(n_raters):
        for u in range(n_units):
            if not np.isnan(matrix[r, u]):
                values.append(matrix[r, u])
    
    values = np.array(values)
    unique_values = np.unique(values)
    
    # Total number of pairable values
    # For interval metric:
    # Do = observed disagreement
    # De = expected disagreement
    
    # Do calculation
    total_disagreement = 0.0
    total_pairs = 0.0
    
    # Iterate over columns (units)
    for u in range(n_units):
        # Get valid ratings for this unit
        unit_ratings = matrix[:, u]
        unit_ratings = unit_ratings[~np.isnan(unit_ratings)]
        
        m_u = len(unit_ratings)
        if m_u < 2:
            continue
            
        # Sum of squared differences for all pairs in this unit
        for i in range(m_u):
            for j in range(i + 1, m_u):
                total_disagreement += diff_sq(unit_ratings[i], unit_ratings[j])
                total_pairs += 1
                
        # Weight adjustment for Do: 1 / (m_u - 1) is already implicit if we average?
        # Standard formula: Do = (1/n) * sum( sum( metric(c, k) ) / (m_u - 1) )
        # Here we just summed metric(c, k). We need to normalize.
        
    # Let's use the coincidence matrix approach or the direct formula.
    # Direct formula for interval data:
    # Do = (1 / Sum(m_u (m_u - 1))) * Sum_u Sum_i Sum_j diff(c_ui, c_uj)
    # De = (1 / (Sum(m_u) (Sum(m_u) - 1))) * Sum_u Sum_v diff(c_u, c_v)
    
    # Calculate N (total number of pairable values)
    # But wait, standard formula N is sum of m_u.
    
    # 1. Observed Disagreement (Do)
    numerator_do = 0.0
    N_total = 0 # sum of m_u
    
    for u in range(n_units):
        unit_ratings = matrix[:, u]
        unit_ratings = unit_ratings[~np.isnan(unit_ratings)]
        m_u = len(unit_ratings)
        
        if m_u > 0:
            N_total += m_u
            
        if m_u > 1:
            # Sum of differences
            sum_diffs = 0.0
            for i in range(m_u):
                for j in range(m_u):
                    if i != j:
                        sum_diffs += diff_sq(unit_ratings[i], unit_ratings[j])
            
            numerator_do += sum_diffs / (m_u - 1)
            
    Do = numerator_do / N_total
    
    # 2. Expected Disagreement (De)
    if N_total <= 1:
        return np.nan

    numerator_de = 0.0
    
    # We need all values flattened to compare every value with every other value
    # But for efficiency with interval data, we can use variance formula?
    # De = 2 * Variance(all values) * (N / (N-1)) ?
    # Let's stick to pair definition to be safe.
    
    # Flatten again
    all_valid_ratings = []
    for r in range(n_raters):
        for u in range(n_units):
            if not np.isnan(matrix[r, u]):
                all_valid_ratings.append(matrix[r, u])
    
    # Sum of diffs between all pairs of values in the dataset
    sum_diffs_de = 0.0
    for i in range(len(all_valid_ratings)):
        for j in range(len(all_valid_ratings)):
            if i != j:
                 sum_diffs_de += diff_sq(all_valid_ratings[i], all_valid_ratings[j])
                 
    De = sum_diffs_de / (N_total * (N_total - 1))
    
    if De == 0:
        return 1.0 if Do == 0 else 0.0
        
    alpha = 1 - (Do / De)
    return alpha
