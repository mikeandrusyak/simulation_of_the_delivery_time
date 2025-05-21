import os
import pandas as pd
import re

# Data source
# https://www.ecad.eu/indicesextremes/customquerytimeseriesplots.php?optionSelected=index&processtext1=Your+query+is+being+processed.+Please+wait...&countryselect=SWITZERLAND%7Cch&stationselect=All+stations%7C**&categoryselect=All+categories%7C**&indexselect=CWD%3A+Maximum+no+of+consecutive+wet+days+%28RR+%3E%3D+1+mm%29%5B1%5D%7CCWD&seasonselect=ANNUAL%7C0&processtext2=Your+query+is+being+processed.+Please+wait...
base_folder = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "weather_data")
# List for all files
all_data = []

# Pass on each index
for index_folder in os.listdir(base_folder):
    index_path = os.path.join(base_folder, index_folder)
    if os.path.isdir(index_path):
        for filename in os.listdir(index_path):
            if filename.endswith(".txt"):
                filepath = os.path.join(index_path, filename)

                # We read the first 20 lines
                with open(filepath, 'r', encoding='utf-8') as file:
                    header_lines = [next(file) for _ in range(20)]

                # Looking for a line with information about the station
                station_line = [line for line in header_lines if "This is the time series data" in line][0]

                # Extract the name of the station and the Station-ID by regular expression
                match = re.search(r"SWITZERLAND,\s*(.+?)\s*\(Station-ID:\s*(\d+)\)", station_line)
                if match:
                    station_name = match.group(1).strip()
                    station_id = match.group(2).strip()
                else:
                    station_name = "Unknown"
                    station_id = "Unknown"

                # Read the data themselves
                df = pd.read_csv(filepath, skiprows=20, names=["YEAR", "CALC", "MEAN"])
                
                # Filter bad values
                df = df[df["YEAR"] != -999999]
                
                # Add the Index, Station and Station ID columns
                df["INDEX"] = index_folder
                df["STATION_NAME"] = station_name
                df["STATION_ID"] = station_id

                all_data.append(df)

# Combine all the data
final_df = pd.concat(all_data, ignore_index=True)

final_df["YEAR"] = pd.to_numeric(final_df["YEAR"], errors="coerce")
final_df["CALC"] = pd.to_numeric(final_df["CALC"], errors="coerce")
final_df["MEAN"] = pd.to_numeric(final_df["MEAN"], errors="coerce")
final_df["STATION_ID"] = pd.to_numeric(final_df["STATION_ID"], errors="coerce")

# Delete rows with incorrect values ​​in YEAR column
final_df = final_df.dropna(subset=["YEAR"])

# Convert YEAR column into an int type (after NAN removal)
final_df["YEAR"] = final_df["YEAR"].astype(int)

# Filter data from 2000 to 2024 inclusive
final_df = final_df[final_df["YEAR"] == 2023]

final_df["CALC"] = final_df["CALC"] / 100
final_df.to_csv("parsed_weather_data.csv", index=False)
# Calculate the average probability of each index

# We are interested in the following indices
intresting_indices = ['FD', 'FG6BFT','R20MM', 'SD5CM', 'SD50CM']

filtered_data = final_df[final_df['INDEX'].isin(intresting_indices)]
filtered_data = filtered_data[filtered_data['CALC'] != -9999.99]
average_probabilities = filtered_data.groupby('INDEX')['CALC'].mean()
# Convert the average probabilities to daily probabilities
daily_probabilities = average_probabilities / 365
probabilities_dict = daily_probabilities.to_dict()
print(probabilities_dict)