import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import requests
from io import StringIO

# Import the convert_to_odata function correctly from the module where it's defined
from src.api.routes import convert_to_odata

# Streamlit frontend
st.title("OData Query Assistant")

# User input for the query
query_input = st.text_area("Enter your query", value="", height=200)

if st.button("Submit"):
    if query_input:
        try:
            # Call the convert_to_odata function and fetch the XML response
            xml_response = convert_to_odata(query_input.text)
            
            # Parse XML and convert it to a Pandas DataFrame
            def parse_xml_to_dataframe(xml_data):
                root = ET.ElementTree(ET.fromstring(xml_data)).getroot()
                all_records = []
                
                # Iterate over each item in the XML structure
                for record in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
                    fields = {}
                    for field in record.findall(".//{http://schemas.microsoft.com/ado/2007/08/dataservices}*"):
                        fields[field.tag.split('}')[1]] = field.text
                    all_records.append(fields)
                
                return pd.DataFrame(all_records)
            
            # Convert the response XML to a dataframe
            dataframe = parse_xml_to_dataframe(xml_response)
            
            # Display the dataframe in the frontend
            st.write("### Query Results")
            st.dataframe(dataframe)

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query.")
