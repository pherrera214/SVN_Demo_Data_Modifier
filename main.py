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
    /* Your CSS here */
    </style>
"""

def upload_xml(db_path, xml_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS default_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            xml_files BLOB
        )
    ''')

    # Read XML file
    with open(xml_file_path, 'rb') as file:
        xml_data = file.read()

    # Insert XML data into the database
    cursor.execute(f''' SELECT COUNT(*) FROM default_files''')
    rows = cursor.fetchone()[0]

    if rows < 3:
        cursor.execute(f'''
            INSERT INTO default_files (xml_files) VALUES (?)
        ''', (xml_data,))
        # Commit and close the connection
        conn.commit()
        conn.close()
        print(f"XML file {xml_file_path} uploaded to database.")

def retrieve_xml(db_path, record_id, output_file_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Query to fetch XML data
        cursor.execute(f'''
            SELECT xml_files FROM default_files WHERE id = ?
        ''', (record_id,))

        # Fetch the data
        xml_data = cursor.fetchone()[0]

        # Check if data was retrieved
        if xml_data:
            # Save XML data to a file
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

# Function for writing the XML file
def save_modified_xml(file_name, tree):
    modified_xml = BytesIO()
    tree.write(modified_xml, encoding='utf-8', xml_declaration=True)
    modified_xml.seek(0)
    return modified_xml

def time_to_decimal_hours(time_str):
    dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
    hours = dt.hour
    minutes = dt.minute
    decimal_hours = hours + minutes / 60      # Convert time to decimal hours
    return decimal_hours

# Function to update unload_date to the current timestamp
def update_unload_date(root):
    """Update the unload_date element to the current timestamp."""
    unload_date_elements = root.findall(".//*[@unload_date]")
    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for elem in unload_date_elements:
        elem.set("unload_date", current_timestamp)
    print(f"Unload date updated to {current_timestamp}.")

# Main Function 
def main():
    # Initialize session state variables
    if 'previous_file_index' not in st.session_state:
        st.session_state.previous_file_index = None

    file_changed = False
    error = False
    def_file = False
    selected_file = None
    uploaded_files = None

    # Progress bar (if needed)
    st.image("XML_TitleHeader.png")
    placeholder = st.empty()
    placeholder1 = st.empty()
    placeholder2 = st.empty()
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
    st.sidebar.subheader("Choose file to modify")

    # Initialize session state variables if not already set
    if 'show_uploader' not in st.session_state:
        st.session_state.show_uploader = False  # Hide uploader initially
    if 'show_default' not in st.session_state:
        st.session_state.show_default = False
    if 'default_files_clicked' not in st.session_state:
        st.session_state.default_files_clicked = False
    if 'previous_file_index' not in st.session_state:
        st.session_state.previous_file_index = -1

    # Sidebar buttons
    upload_button = st.sidebar.button("Upload XML Files", use_container_width=True, type="primary")
    default_button = st.sidebar.button("Use Default Files", use_container_width=True)
    st.sidebar.divider()

    # Handle "Upload XML Files" button click
    if upload_button:
        st.session_state.show_uploader = True
        st.session_state.show_default = False
        st.session_state.default_files_clicked = False

    # Handle "Use Default Files" button click
    if default_button:
        st.session_state.show_uploader = False
        st.session_state.show_default = True
        st.session_state.default_files_clicked = True

    # Show file uploader or default files based on session state
    if st.session_state.show_uploader and not st.session_state.default_files_clicked:
        with st.sidebar.expander("#### UPLOAD FILES", expanded=True):
            uploaded_files = st.file_uploader("Choose XML files", accept_multiple_files=True, type=["xml"])

            if uploaded_files:
                file_names = [file.name for file in uploaded_files]
                selected_file_name = st.sidebar.selectbox("Select a file to focus on", file_names)

                for uploaded_file in uploaded_files:
                    if uploaded_file.name == selected_file_name:
                        selected_file = uploaded_file
                        break
                selected_file_index = file_names.index(selected_file_name)

                # Check if the selected file has changed
                if selected_file_index != st.session_state.previous_file_index or selected_file is None:
                    file_changed = True
                    st.session_state.previous_file_index = selected_file_index
                else:
                    file_changed = False

    if st.session_state.show_default:
        # Retrieve the default XML files for use
        record_id = 1
        output_file_path = 'default_denial.xml'
        default_denial = retrieve_xml(db_path, record_id, output_file_path)

        record_id = 2
        output_file_path = 'default_concurrent.xml'
        default_concurrent = retrieve_xml(db_path, record_id, output_file_path)

        record_id = 3
        output_file_path = 'default_usage.xml'
        default_usage = retrieve_xml(db_path, record_id, output_file_path)

        default_files = [default_denial, default_concurrent, default_usage]

        # Process the default files
        file_names = ['default_denial.xml', 'default_concurrent.xml', 'default_usage.xml']
        selected_file_name = st.sidebar.selectbox("Select a default file to focus on", file_names)

        if selected_file_name == file_names[0]:
            selected_file = default_files[0]
            file_name = 'samp_eng_app_denial.xml'
        elif selected_file_name == file_names[1]:
            selected_file = default_files[1]
            file_name = 'samp_eng_app_concurrent.xml'
        elif selected_file_name == file_names[2]:
            selected_file = default_files[2]
            file_name = 'samp_eng_app_usage_summary.xml'
        def_file = True

        selected_file_index = file_names.index(selected_file_name)
        # Check if the selected file has changed
        if selected_file_index != st.session_state.previous_file_index:
            file_changed = True
            st.session_state.previous_file_index = selected_file_index
        else:
            file_changed = False

    if selected_file:
        # Load and parse the XML file
        if uploaded_files:
            tree = ET.parse(selected_file)
            root = tree.getroot()
            file_name = selected_file.name
            # Remove the prefix, file extension, and underscores, then convert to proper case
            display_file_name = file_name.replace("samp_eng_app_", "").replace("_", " ").rsplit('.', 1)[0].title()
        else:
            tree = ET.ElementTree(ET.fromstring(selected_file))
            root = tree.getroot()
            display_file_name = selected_file_name.replace("_", " ").replace(".xml", " ").title()

        # Update unload_date to the current timestamp
        update_unload_date(root)

        st.header(f"Update {display_file_name}")
        st.write(" ")

        # Your logic for updating other fields (usage, concurrent, denial)
        # Call classes for usage, concurrent, denial based on file type and update XML

        # Example:
        # if usage:
        #     usg = usage_class(...)
        #     ...
        
        # After all changes:
        modified_xml = save_modified_xml(file_name, tree)
        st.sidebar.download_button(
            label="Download Modified XML",
            data=modified_xml,
            file_name=file_name,
            mime='application/xml',
            type="primary"
        )

if __name__ == "__main__":
    DDMIcon= Image.open("DDM_Icon.ico")
    st.set_page_config(
        page_title="SVN Demo Data Modifier",
        layout="wide",
        page_icon=DDMIcon
    )
    
    st.markdown(sidebar_bg_img, unsafe_allow_html=True)
    st.logo("logoSN.png")
    main()
