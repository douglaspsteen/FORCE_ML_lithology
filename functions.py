def scrub_data(df):
    
    import pandas as pd
    
    # Fill missing Z_LOC values with the corresponding negative depth
    df.Z_LOC.fillna(-df.DEPTH_MD, inplace=True)
    
    # Create dictionaries with median X_LOC and Y_LOC for each well
    unique_wells = df.WELL.unique()
    
    X_LOC_medians = {}
    Y_LOC_medians = {}

    for well in unique_wells:
        X_LOC_medians[well] = df.loc[df['WELL']==well]['X_LOC'].median()
        Y_LOC_medians[well] = df.loc[df['WELL']==well]['Y_LOC'].median()

    # Replace X_LOC and Y_LOC values with previously determined values for 
    # that well, filling null values in the process.
    for k, v in X_LOC_medians.items():
        df.loc[df.WELL == k, 'X_LOC'] = v
        
    for k, v in Y_LOC_medians.items():
        df.loc[df.WELL == k, 'Y_LOC'] = v
        
        
    # Fill missing GROUP and FORMATION values with unknown
    df.loc[df.GROUP.isna(), 'GROUP'] = 'Unknown'
    df.loc[df.FORMATION.isna(), 'FORMATION'] = 'Unknown'
    
    # Fill Caliper values using forward fill
    df.CALI.fillna(method='ffill', inplace=True)
    
    # Fill missing medium resistivity data using forward fill
    df.RMED.fillna(method='ffill', inplace=True)
    
    # Fill missing deep resistivity data using forward fill
    df.RDEP.fillna(method='ffill', inplace=True)
    
    # Fill missing bulk density data using forward fill
    df.RHOB.fillna(method='ffill', inplace=True)

    # Fill missing compressional slowness data using forward fill
    df.DTC.fillna(method='ffill', inplace=True)

    # Fill missing density correction log data with 0
    df.DRHO.fillna(0, inplace=True)
   
    # Fill missing confidence values with "1", the most common value
    df.FORCE_2020_LITHOFACIES_CONFIDENCE.fillna(1, inplace=True)
    
    # Create dummy variables for GROUP and FORMATION
    group_dummies = pd.get_dummies(df.GROUP, prefix='GRP')
    formation_dummies = pd.get_dummies(df.FORMATION, prefix='FM')
    df = pd.concat([df, group_dummies, formation_dummies], axis=1)
    
    # Drop data columns
    df.drop(['SGR', 'RSHA', 'NPHI', 'PEF', 'SP', 'BS', 'ROP', 'DTS',
            'DCAL', 'MUDWEIGHT', 'RMIC', 'ROPA', 'RXO', 'GROUP', 'FORMATION'],
            axis=1, inplace=True)
    
    return df
    