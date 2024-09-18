import os
import streamlit as st
import pandas as pd
from tabula import read_pdf
import functions as f
import grouping_functions


f.header_intro()
f.header_intro_2()

st.subheader("Grouping Page")

if 'pin_table' in st.session_state:
    pin_table = st.session_state['pin_table']

    #st.write("Pin Table:")
    #st.dataframe(pin_table)
    before_grouping_flag, added_empty_grouping_column = grouping_functions.check_excel_format(pin_table)
    #st.text(f"Before Pin Grouping Flag :{before_grouping_flag}")
    #st.dataframe(added_empty_grouping_column)

    mcu = st.checkbox("Use Algorithm (MCU) for grouping")
    power = st.checkbox("Use database for grouping")

    if not mcu and not power:
        st.info("Make a selection")
        pin_grouping_table = pd.DataFrame()

    elif mcu and power:
        st.info("Please only make a single selection")
        pin_grouping_table = pd.DataFrame()

    elif mcu:
        pin_grouping_table = grouping_functions.assigning_grouping_as_per_algorithm(added_empty_grouping_column)
        st.text("After Grouping from Algorithm:")
        st.dataframe(pin_grouping_table)
        no_grouping_assigned = grouping_functions.check_empty_groupings(pin_grouping_table) 
        if no_grouping_assigned.empty:
            st.info("All grouping values are filled.") 
        else:       
            st.info("Please fill in group values for these :")
            edited_df = st.data_editor(no_grouping_assigned)

            if edited_df['Grouping'].isnull().any():
                st.info("Please enter group names for all.")
            else:
                pin_grouping_table.update(edited_df)
                st.text("Final Grouping Table")
                st.dataframe(pin_grouping_table)

    elif power:
        json_file = "Database.json"
        pin_grouping_table = grouping_functions.assigning_grouping_as_per_database(added_empty_grouping_column, json_file)
        st.text("After Grouping from Database:")
        st.dataframe(pin_grouping_table)
        no_grouping_assigned = grouping_functions.check_empty_groupings(pin_grouping_table) 
        if no_grouping_assigned.empty:
            st.info("All grouping values are filled.") 
        else:       
            st.info("Please fill in group values for these :")
            edited_df = st.data_editor(no_grouping_assigned)

            if edited_df['Grouping'].isnull().any():
                st.info("Please enter group names for all.")
            else:
                pin_grouping_table.update(edited_df)
                st.text("Final Grouping Table")
                st.dataframe(pin_grouping_table)

else:
    st.write("No pin table available.")



   

     
   

