def scrub_data(df):
    
    import pandas as pd
    
    # Fill missing Z_LOC values with the corresponding negative depth
    df.Z_LOC.fillna(-df.DEPTH_MD, inplace=True)
    
    # Create dictionaries with median X_LOC and Y_LOC for each well
    # Get list of unique wells
    unique_wells = df.WELL.unique()
    
    # Set up dictionaries for median X_LOC and Y_LOC for each well
    X_LOC_medians = {}
    Y_LOC_medians = {}

    # Assign each well as the key and median X_LOC/Y_LOC as value
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
    
    # Fill multiple columns using forward fill
    cols = ['CALI', 'RMED', 'RDEP', 'RHOB', 'DTC', 'DRHO']
    df[cols].fillna(method='ffill', inplace=True)
   
    # Create dummy variables for GROUP and FORMATION
    group_dummies = pd.get_dummies(df.GROUP, prefix='GRP')
    formation_dummies = pd.get_dummies(df.FORMATION, prefix='FM')
    df = pd.concat([df, group_dummies, formation_dummies], axis=1)
    
    # Drop data columns
    df.drop(['SGR', 'RSHA', 'NPHI', 'PEF', 'SP', 'BS', 'ROP', 'DTS',
            'DCAL', 'MUDWEIGHT', 'RMIC', 'ROPA', 'RXO', 'GROUP', 'FORMATION'],
            axis=1, inplace=True)
    
    return df
    