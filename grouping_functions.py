import pandas as pd
import json
from pandas import *

def check_excel_format(df):
  
  try:
    #df = pd.read_excel(excel_path)
    required_columns = ['Pin Designator', 'Pin Display Name', 'Electrical Type', 'Pin Alternate Name', 'Grouping']

    if set(required_columns) == set(df.columns):
      return True, df
    elif set(required_columns[:-1]) == set(df.columns):  # Check for missing 'Grouping' column
      df['Grouping'] = ' '
      #df.to_excel(excel_path, index=False)
      return True, df
    else:
      print("Incorrect extraction format.")
      return False, df
  except Exception as e:
    print(f"Error reading Excel file: {e}")
    return False, df 
  

def assigning_grouping_as_per_database(old_df, json_path):
  df = old_df.copy()
  try:
    with open(json_path, 'r') as f:
      label_map = json.load(f) 

    def get_label(name):
        name = name.strip()
        for label, names in label_map.items():
            if name in [item.strip() for item in names]:
                return label
        print(f"Warning: Could not find a matching label for {name}. Assigning 'Unknown'.")    
        return None

    df['Grouping'] = df['Pin Display Name'].apply(get_label)
    print("Labels assigned to Grouping column successfully.")

  except Exception as e:
    print(f"Error processing files: {e}")    
  return df  

def group_port_pins(value):
    if value.startswith('P'):
        if len(value) == 3:
            if value[1] in '0123456789':
                return f'Port {value[1]}'
            elif value[1] in 'ABCDEFGH':
                return f'Port {value[1]}'
        elif value[1:3] in '101112131415':
            return f'Port {value[1:3]}'
    return None 


# grouping i/o Pins - GPIO's together- I/o
# SDA and SCL have to be placed together

def group_power_pins(row):
    
    power_prefixes = ['EVS', 'VSS', 'VCC', 'EVD', 'REG', 'Epa', 'AVS', 'AVC', 'CVC', 'VDD']
    power_suffixes = ['REFL', 'REFH']

    if row['Electrical Type'] == 'Power' and row['Pin Display Name'].startswith(tuple(power_prefixes)):
        prefix = row['Pin Display Name'][:3]
        suffix = row['Pin Display Name'][3:7]
        if suffix in power_suffixes:
            return f'P{prefix[1]} {suffix}'  # Handle power suffixes
        else:
            return f'P{prefix[1]}'  # Handle power prefixes
    return None  # Handle cases that don't match the pattern

    # !st step - VDD-P+Digital
    # 2nd step - GND - P- 


def group_output_pins(row):

    if row['Electrical Type'] == "Output" and row['Pin Display Name'].startswith("COM"):
        return "Common Output" if row['Pin Display Name'].startswith("COM") else "System"
    return None

def group_input_pins(row):

    if row['Electrical Type'] == "Input":
        if row['Pin Display Name'].startswith(("XT", "\R", "EX", "\S", "MD", "NM", "Vr", "FW", "OS", "X1", "X2")):
            return {
                "XT": "SOSC",
                "\R": "System",
                "EX": "Clock1",
                "\S": "System",
                "MD": "Mode",
                "NM": "Interrupt",
                "Vr": "P+ Analog",
                "FW": "System",
                "OS": "Clock2",
                "X1": "MOSC",
                "X2": "MOSC"
            }[row['Pin Display Name'][:2]]
    return None
# Chipseclect will always be input CS - Input 

def assigning_grouping_as_per_algorithm(df):
    df['Grouping'] = df['Pin Display Name'].apply(group_port_pins)
    #df['Grouping'] = df.apply(group_power_pin, axis=1)
    mask = df['Grouping'].isna()  # Create a mask for NaN values in 'Grouping'
    df.loc[mask, 'Grouping'] = df[mask].apply(group_power_pins, axis=1)  # Apply group_power_pin only to NaN rows
    mask = df['Grouping'].isna()
    df.loc[mask, 'Grouping'] = df[mask].apply(group_output_pins, axis=1)
    mask = df['Grouping'].isna()
    df.loc[mask, 'Grouping'] = df[mask].apply(group_input_pins, axis=1)

    return df

def check_empty_groupings(df):
    empty_groupings = df[df['Grouping'].isna()]
    return empty_groupings