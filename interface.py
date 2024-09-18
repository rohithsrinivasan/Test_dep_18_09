from os import read
import streamlit as st
import pandas as pd
from tabula import read_pdf
import functions as f

st.set_page_config(page_icon= 'dados/image1.png', page_title= "PDF Extractor", )

st.page_link("interface.py", label="Extraction")
st.page_link("pages/grouping.py", label="Grouping")

f.header_intro() 
f.header_intro_2()

#st.subheader('Upload your PDF by clicking on "Browse Files"')
input_buffer = st.file_uploader("Upload a file", type=("PDF"))
input_part_number = st.text_input("Enter a valid Part Number")
input_loaded = False

#st.subheader("Extraction Page") 
if input_buffer:
    if input_part_number:
        part_number, number_of_pins, package_type, package_code = f.part_number_details(input_part_number, input_buffer)
        pin_table = f.extracting_pin_tables(input_buffer, part_number, number_of_pins, package_type, package_code)
        st.session_state['pin_table'] = pin_table
        if "page" in st.session_state and st.session_state["page"] == "grouping":
            st.page_link("pages/grouping.py",label="Grouping")            
        else:
            st.write("Pin table displayed")        

    else:
        st.warning("Please enter a valid Part Number.")
else:
    st.info("Please upload a PDF file.")
    
