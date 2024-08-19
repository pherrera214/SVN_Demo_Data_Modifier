import streamlit as st
import xml.etree.ElementTree as ET
import sqlite3
import time
import pandas as pd
from PIL import Image
from io import BytesIO
from datetime import datetime, timedelta
from usage_class import usage_class
from concurrent_class import concurrent_class
from denial_class import denial_class

 

sidebar_bg_img = """
    
    <style>

    #MainBg
    .st-emotion-cache-1r4qj8v {
    position: absolute;
    background: #FFFAFA;
    color: rgb(49, 51, 63);
    inset: 0px;
    color-scheme: light;
    overflow: hidden;
    }

    h1 {
    font-family: "Font Awesome 6 Pro", sans-serif;
    font-weight: 800;
    font-variant: small-caps;
    background: linear-gradient(to top, #032C41, #02506B);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
    padding: 0rem 0px 1rem;
    margin: 0px;
    line-height: 1;
    }

    /*Image Title*/
    .st-emotion-cache-1v0mbdj {
    display: block;
    margin-left: auto;
    margin-right: auto;
    display: flex;
    flex-direction: column;
    -webkit-box-align: stretch;
    align-items: stretch;
    width: auto;
    -webkit-box-flex: 0;
    flex-grow: 0;
    margin-bottom: 1rem;
    margin-top: 0rem;
    }

    .st-emotion-cache-1jicfl2 {
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* header violet*/
    h2{
    background-color: #920113;
    color: white;
    font-variant-caps: all-small-caps;
    text-align: center;
    border-radius: 10px;
    }

    h2 {
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 600;
    letter-spacing: -0.005em;
    padding: 0.25rem 0px;
    margin: 0px;
    line-height: 1.2;
    }
    
    h4{
    color: #920113;
    }
    
    [data-testid= "stThumbValue"]{
    color: #920113;
    }

    /*Logo*/
    .st-emotion-cache-5drf04 {
    height: 7rem;
    max-width: 20rem;
    margin: 0.25rem 0.5rem 0.25rem 0px;
    z-index: 999990;
    }

    /*sidebar heading-demodata xml*/
    .st-emotion-cache-1gwvy71 {
    padding: 0px 1.5rem 6rem;
    }

    .st-emotion-cache-1gwvy71 h1 {
    font-family: "League Spartan", sans-serif;
    color: #ffffff;
    background-color: #032C41;
    font-size: 23px;
    }

     /*sidebar gap */
    .st-emotion-cache-1dfdf75 {
    width: 282px;
    position: relative;
    display: flex;
    flex: 0.5 0.5 0%;
    flex-direction: column;
    gap: 0.5rem;
    flex-wrap: nowrap;
    }

    /*date expander gap*/
    .st-emotion-cache-phzz4j {
    width: 248px;
    position: relative;
    /* display: flex; */
    flex: 0.5 0.5 0%;
    flex-direction: column;
    gap: 0.25rem;
    }

    .st-emotion-cache-1mi2ry5 {
    display: flex;
    -webkit-box-pack: justify;
    justify-content: space-between;
    -webkit-box-align: start;
    align-items: start;
    padding:  0.5rem 0.5rem 0.25rem ;
    }

    /*Sidebar Components*/
    .st-emotion-cache-ue6h4q {
    font-size: 14px;
    color: rgb(49, 51, 63);
    display: flex;
    visibility: visible;
    margin-bottom: 0.5rem;
    height: auto;
    min-height: 1.5rem;
    vertical-align: middle;
    flex-direction: row;
    -webkit-box-align: center;
    align-items: center;
    }


    [data-testid="stSidebar"]{
    background-color: #E6EDF1;    
    width: 15%;
    }

    [data-testid= "stHeader"]{
    background-color: #920113;
    color: #ffffff;
    padding: 1rem;
    }

    [data-testid= "stSidebarUserContent"]{
    background-color: #6d0b17;
    height: 1px;
    }

    [data-testid= "stSidebarHeader"]{
    background-color: #6d0b17;
    }

    /*side bar subhead*/
    .st-emotion-cache-1whx7iy p{
    font-weight: bold;
    font-size: 20px;
    }

    /*new date value*/
    .st-emotion-cache-1gwvy71 h3 {
    font-size: 20px;
    font-weight: bold;
    }   

    .st-emotion-cache-1ag92y2{
    background-color: #E6EDF1; 
    }
    
    /*for paragraph*/
    p, ol, ul, dl {
        font-size: 1rem;
        font-weight: 400;
    }

    /*expander margin*/
    .st-emotion-cache-p5msec {
        position: relative;
        display: flex;
        width: 100%;
        font-size: 14px;
        padding: 0px 1rem;
        list-style-type: none;
        background-color:#E6EDF1; 
    }

    </style>                 
            
"""

def upload_xml(db_path, table_name, xml_column, xml_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
   
    # Create table if it does not exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {xml_column} BLOB
        )
    ''')
 
    # Read XML file
    with open(xml_file_path, 'rb') as file:
        xml_data = file.read()
 
    # Insert XML data into the database
    cursor.execute(f'''
        INSERT INTO {table_name} ({xml_column}) VALUES (?)
    ''', (xml_data,))
   
    # Commit and close the connection
    conn.commit()
    conn.close()
    print(f"XML file {xml_file_path} uploaded to database.")
 
def retrieve_xml(db_path, table_name, xml_column, record_id, output_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
   
    try:
        # Query to fetch XML data
        cursor.execute(f'''
            SELECT {xml_column} FROM {table_name} WHERE id = ?
        ''', (record_id,))
       
        # Fetch the data
        xml_data = cursor.fetchone()[0]
 
        # Check if data was retrieved
        if xml_data:
            #Save XML data to a file
            with open(output_file_path, 'wb') as file:
                file.write(xml_data)
            print(f"XML data saved to {output_file_path}.")
            return xml_data
        else:
            print("No data found.")
    except sqlite3.Error as e:
        print(f"Error retrieving XML data: {e}")
    finally:
        # Close the connection
        conn.close()

# Example usage for uploading XML
db_path = 'my_database.db'
table_name = 'xml_table'
xml_column = 'xml_data'
 
xml_file_path = 'C:/Users/vince.durante/Documents/samp_eng_app_denial.xml'
#upload_xml(db_path, table_name, xml_column, xml_file_path)
 
# Example usage for retrieving XML
xml_files = []
record_id = 1
output_file_path = 'output_file.xml'
xml_data = retrieve_xml(db_path, table_name, xml_column, record_id, output_file_path)

record_id = 3
xml_data1 = retrieve_xml(db_path, table_name, xml_column, record_id, output_file_path)
 
record_id = 4
xml_data2 = retrieve_xml(db_path, table_name, xml_column, record_id, output_file_path)

#Function for writing the XML file
def save_modified_xml(file_name, tree):
    modified_xml = BytesIO()
    tree.write(modified_xml, encoding='utf-8', xml_declaration=True)
    modified_xml.seek(0)
    return modified_xml

#Main Function 
def main():
   
    #st.image("XML_TitleHeader.png")
    #st.title("ServiceNow ENGINEERING DEMO DATA MODIFIER")
    #st.divider()
    placeholder = st.empty()
    placeholder1 = st.empty()

    progress_text = "Operation in progress. Please wait."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.01)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()

    # Sidebar for file selection and source update
    st.sidebar.title("ServiceNow ENGINEERING DEMO DATA MODIFIER")
    st.sidebar.divider()
    with st.sidebar.expander(f"#### UPLOADED FILES"):
        uploaded_files = st.file_uploader("Choose XML files", accept_multiple_files=True, type=["xml"])

    if uploaded_files:

        file_names = [file.name for file in uploaded_files]
        selected_file_name = st.sidebar.selectbox("Select a file to focus on", file_names)

        
        selected_file = None
        for uploaded_file in uploaded_files:
            if uploaded_file.name == selected_file_name:
                selected_file = uploaded_file
                break
    else:
        file_name = output_file_path
        selected_file = xml_data
        

    if selected_file:
        
        # Load and parse the XML file
        if uploaded_files:
            tree = ET.parse(selected_file)
            root = tree.getroot()

            file_name = selected_file.name

            #Remove the prefix, file extension, and underscores, then convert to proper case
            display_file_name = file_name.replace("samp_eng_app_", "").replace("_", " ").rsplit('.', 1)[0].title()
        else:
            tree = ET.ElementTree(ET.fromstring(selected_file))
            root = tree.getroot()
            display_file_name = "Default File"


        st.header(f"Update {display_file_name}")
        usage_elements = None
        usage = root.find('.//samp_eng_app_usage_summary[@action="INSERT_OR_UPDATE"]')
        concurrent = root.find('.//samp_eng_app_concurrent_usage[@action="INSERT_OR_UPDATE"]')
        denial = root.find('.//samp_eng_app_denial[@action="INSERT_OR_UPDATE"]')
        
        # Find all <samp_eng_app_concurrent_usage> elements with the specified action attribute
        if usage:
            usage_elements = root.findall('.//samp_eng_app_usage_summary[@action="INSERT_OR_UPDATE"]')
            
        elif concurrent:
            usage_elements = root.findall('.//samp_eng_app_concurrent_usage[@action="INSERT_OR_UPDATE"]')

        elif denial:
            usage_elements = root.findall('.//samp_eng_app_denial[@action="INSERT_OR_UPDATE"]')
            
            # Count the elements
        count = len(usage_elements)

        min_range, max_range = st.sidebar.slider("Select Range",min_value=1, max_value=count,value=(1,count),key="select_range")
        # Fields that are always visible
        with st.sidebar.expander(f"#### Edit Source Value"):
            st.markdown("")
            new_source = st.text_input("New Source Value", "")
        
        st.sidebar.subheader("New Date Value", "")

        # Determine the appropriate label [EDITED  ]
        if denial:
            label = "Update Denial Date"
        else:
            label = "Update Usage Date"

        # Display the date input with the corresponding label
        with st.sidebar.expander(f"#### {label}"):
            st.markdown("")
            new_date = st.date_input("Enter Start Date",value=None)

        if usage:
            with st.sidebar.expander(f"#### {"Update Idle Duration"}"):
                st.markdown("")
                idle_dur_date = st.date_input("Enter Idle Duration (Date)",value=None)
                idle_dur_time = st.time_input("Enter Idle Duration (Time)",value=None,step=60)
                
            with st.sidebar.expander(f"#### {"Session Duration"}"):
                st.markdown("")
                session_dur_date = st.date_input("Enter Session Duration (Date)",value=None)
                session_dur_time = st.time_input("Enter Session Duration (Time)",value=None,step=60)
            #condition to not update if there is one none in either idle_dur_date or idle_dur time
            if((idle_dur_date is not None) and (idle_dur_time is not None)):
                total_idle_dur = datetime.combine(idle_dur_date,idle_dur_time)
            else:
                total_idle_dur = None 
            #condition to not update if there is one none in either session_dur_date or session_dur_time
            if((session_dur_date is not None) and (session_dur_time is not None) ):        
                total_session_dur = datetime.combine(session_dur_date,session_dur_time)
            else:
                total_session_dur = None

        update_button = st.sidebar.button("Update All Fields")
        st.sidebar.divider()

    
        if usage:
            usg = usage_class()
            usg.set_tree(tree)
            usg.set_root(root)
            usg.set_min(min_range)
            usg.set_max(max_range)
            usg.set_new_source(new_source if update_button else None)
            usg.set_new_date(new_date if update_button else None)
            usg.set_total_idle_dur(total_idle_dur if update_button else None)
            usg.set_total_session_dur(total_session_dur if update_button else None)
            error, tree = usg.update_usage()
            
        elif concurrent:

            conc = concurrent_class()
            conc.set_tree(tree)
            conc.set_root(root)
            conc.set_min(min_range)
            conc.set_max(max_range)
            conc.set_new_source(new_source if update_button else None)
            conc.set_new_date(new_date if update_button else None)
            error, tree = conc.update_concurrent()
    
        elif denial:
            print(type(uploaded_files))
            deny = denial_class()
            deny.set_tree(tree)
            deny.set_root(root)
            deny.set_min(min_range)
            deny.set_max(max_range)
            deny.set_new_source(new_source if update_button else None)
            deny.set_new_date(new_date if update_button else None)
            error,tree = deny.update_denial()
            
            placeholder1.dataframe(deny.display_data())
            
        else:
            st.write(f"Unknown file type: {file_name}")
            return
        
        if update_button:
                modified_xml = save_modified_xml(file_name, tree)
                st.sidebar.download_button(
                label="Download Modified XML",
                data = modified_xml,    
                file_name=file_name,
                mime='application/xml',
                type="primary"
                )
                if error: placeholder.error(":x: Not Updated!")
                else: placeholder.success(":white_check_mark: All fields updated successfully!")

if __name__ == "__main__":
    DDMIcon= Image.open("DDM_Icon.ico")
    st.set_page_config(
        page_title="ServiceNow Engineering Demo Data Modifier",
        layout="wide",
        page_icon=DDMIcon)
    
    st.markdown(sidebar_bg_img, unsafe_allow_html=True)
    st.logo("logoSN.png")
    main()
