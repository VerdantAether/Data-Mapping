# -*- coding: utf-8 -*-
"""
Created on Fri Jan 9 20:49:53 2026
@author: Raleigh W. Mann

Data From https://data-henrico.opendata.arcgis.com/datasets/f9788d5c10c64ed1a1d13e93feff21e3_0/explore

Purpose: To filter a list of all properties in Henrico County into useable leads for mortgages. 

"""

#Imports
import pandas as pd

# --------------------------------------------------
# Load dataset
# --------------------------------------------------

file_path = "Data\Tax_Parcels_and_CAMA_Data_External.csv"
df = pd.read_csv(file_path)

# --------------------------------------------------
# Columns needed
# --------------------------------------------------

cols = [
    "FULL_ADDRESS",
    "ZIP_CODE",
    "LAND_VALUE_CURRENT",
    "IMPROVEMENTS_VALUE_CURRENT",
    "LAST_SALE_DATE",
    "RESIDENTIAL_COMMERCIAL"
]

df = df[cols]

# Ensure numeric values
df["LAND_VALUE_CURRENT"] = pd.to_numeric(df["LAND_VALUE_CURRENT"], errors="coerce").fillna(0)
df["IMPROVEMENTS_VALUE_CURRENT"] = pd.to_numeric(df["IMPROVEMENTS_VALUE_CURRENT"], errors="coerce").fillna(0)

# Compute total assessed value
df["TOTAL_ASSESSED_VALUE"] = (
    df["LAND_VALUE_CURRENT"] + df["IMPROVEMENTS_VALUE_CURRENT"]
)

# Normalize category values
df["RESIDENTIAL_COMMERCIAL"] = (
    df["RESIDENTIAL_COMMERCIAL"]
    .str.strip()
    .str.upper()
)

# Split datasets
residential = df[
    (df["RESIDENTIAL_COMMERCIAL"] == "R") &
    (df["TOTAL_ASSESSED_VALUE"] > 500_000) #Can be changed to select different Asset Classes
]

commercial = df[
    (df["RESIDENTIAL_COMMERCIAL"] == "C") &
    (df["TOTAL_ASSESSED_VALUE"] > 1_000_000) #Can be changed to select different Asset Classes
]
# --------------------------------------------------
#IMPORTANT! This is the missing piece. If given a list of what Truist already manages, we can filter to only new leads.
# --------------------------------------------------
comparison_path = "Data/Truist_Property_List.csv"
truist_df = pd.read_csv(comparison_path)

# Normalize address formatting for reliable matching
def normalize_address(series):
    return (
        series
        .str.upper()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

truist_df["FULL_ADDRESS"] = normalize_address(truist_df["FULL_ADDRESS"])
residential["FULL_ADDRESS"] = normalize_address(residential["FULL_ADDRESS"])
commercial["FULL_ADDRESS"] = normalize_address(commercial["FULL_ADDRESS"])

# Convert comparison list to a set for fast lookup
truist_addresses = set(truist_df["FULL_ADDRESS"])

# --------------------------------------------------
# SPLIT RESIDENTIAL
# --------------------------------------------------

truist_owned_residential = residential[
    residential["FULL_ADDRESS"].isin(truist_addresses)
]

truist_unowned_residential = residential[
    ~residential["FULL_ADDRESS"].isin(truist_addresses)
]

# --------------------------------------------------
# SPLIT COMMERCIAL
# --------------------------------------------------

truist_owned_commercial = commercial[
    commercial["FULL_ADDRESS"].isin(truist_addresses)
]

truist_unowned_commercial = commercial[
    ~commercial["FULL_ADDRESS"].isin(truist_addresses)
]

# --------------------------------------------------
# EXPORT RESULTS
# --------------------------------------------------

truist_owned_residential.to_csv(
    "Truist_Owned_Residential.csv", index=False
)
truist_unowned_residential.to_csv(
    "Truist_Unowned_Residential.csv", index=False
)

truist_owned_commercial.to_csv(
    "Truist_Owned_Commercial.csv", index=False
)
truist_unowned_commercial.to_csv(
    "Truist_Unowned_Commercial.csv", index=False
)

# --------------------------------------------------
# ZIP-CODE FILTERED UNOWNED RESIDENTIAL
# --------------------------------------------------


#Filters by Zipcode, can be used for branch / area specific leads. 
target_zips = {"23059", "23060", "23233"}

truist_unowned_residential_zip_filtered = truist_unowned_residential[
    truist_unowned_residential["ZIP_CODE"]
    .astype(str)
    .str.zfill(5)
    .isin(target_zips)
]

# Export
truist_unowned_residential_zip_filtered.to_csv(
    "Truist_Unowned_Residential_Wyndham.csv",
    index=False
)


residential.to_csv("henrico_residential_over_500k.csv", index=False)
commercial.to_csv("henrico_commercial_over_1M.csv", index=False)


