def scrub_data(df):
    
    # Fill missing Z_LOC values with the corresponding negative depth
    df.Z_LOC.fillna(-df.DEPTH_MD, inplace=True)