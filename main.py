import streamlit as st
import xml.etree.ElementTree as ET
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
         
        if selected_file:
           
            file_name = selected_file.name

            # Remove the prefix, file extension, and underscores, then convert to proper case
            display_file_name = file_name.replace("samp_eng_app_", "").replace("_", " ").rsplit('.', 1)[0].title()

            st.header(f"Update {display_file_name}")
           
            # Load and parse the XML file
            tree = ET.parse(selected_file)
            root = tree.getroot()
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
                sample2 = usage_class()
                sample2.set_tree(tree)
                sample2.set_root(root)
                sample2.set_min(min_range)
                sample2.set_max(max_range)
                sample2.set_new_source(new_source if update_button else None)
                sample2.set_new_date(new_date if update_button else None)
                sample2.set_total_idle_dur(total_idle_dur if update_button else None)
                sample2.set_total_session_dur(total_session_dur if update_button else None)
                error, tree = sample2.update_usage()
                
            elif concurrent:

                sample1 = concurrent_class()
                sample1.set_tree(tree)
                sample1.set_root(root)
                sample1.set_min(min_range)
                sample1.set_max(max_range)
                sample1.set_new_source(new_source if update_button else None)
                sample1.set_new_date(new_date if update_button else None)
                error, tree = sample1.update_concurrent()
        
            elif denial:
                print(type(uploaded_files))
                sample = denial_class()
                sample.set_tree(tree)
                sample.set_root(root)
                sample.set_min(min_range)
                sample.set_max(max_range)
                sample.set_new_source(new_source if update_button else None)
                sample.set_new_date(new_date if update_button else None)
                error,tree = sample.update_denial()
              
                #placeholder1.dataframe(sample.display_data())
                with placeholder1:
                    df = sample.display_data()
                
                    #Dates Tab Graph
                    col1, col2= st.columns((2))
                    df['denial_date'] = pd.to_datetime(df['denial_date'])

                    #Getting the min and max date
                    startDate = pd.to_datetime(df['denial_date']).min()
                    endDate = pd.to_datetime(df['denial_date']).max()

                    with col1:
                        date1 = pd.to_datetime(st.date_input("Start Date", startDate))

                    with col2:
                        date2 = pd.to_datetime(st.date_input("End Date", endDate))

                        df = df[(df['denial_date'] >= date1) & (df['denial_date'] <= date2)].copy()


                    col3, col4= st.columns([2, 1], gap="small")
                    with col3:
                        container = st.container(border=True, height=520)
                        container.subheader("Denial Date vs Denial Count")
                        fig = px.bar(df, x= df['denial_date'], y = df['total_denial_count'])
                        container.plotly_chart(fig, use_container_width= True, height =500)
                        fig.update_layout(bargap=0)
                
                    with col4:
                        container2 = st.container(border=True, height=200)
                        container2.subheader("Total Denial Count")
                        #den_count= int(df['total_denial_count'])
                        array= pd.Series(df['total_denial_count'])
                        array_int = array.astype(int)
                        container2.header(array_int.sum())

                    with col4:
                        container3 = st.container(border=True, height=300)
                        container3.subheader("Users")
                        container3.write(df['computer'].tolist())


                        #ytrain = df['computer']
                        #ytrain_numpy = np.array([x for x in df['computer']])

                        #userValue= pd.DataFrame(
                        #    {df['computer']: df['computer'].tolist(),
                        #    }
                        #    )

                
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
