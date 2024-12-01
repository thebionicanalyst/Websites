import streamlit as st
import streamlit_shadcn_ui as ui
from streamlit_option_menu import option_menu
from local_components import card_container
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import altair as alt
import requests
import base64
from PIL import Image
from io import BytesIO

st.set_page_config(layout="wide")

json_dict = {
    "type": "service_account",
    "project_id": "bionic-workout",
    "private_key_id": "54a2b7aa0bc298428f8ab0617f2059d3e4f59abd",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC29FeCX79NcACA\nbhqwS2dXrxSdDK+k/eys5XleReVjK+HLE/tCb5v2fNblOjfom/dwlNA3s7rLT/Pv\ns7pU4Yskm/O4JjoFHA1EzN1g9vIAkwUZToLGmb05feOi4zFlEtbLbOwGbhOCdbY2\n8DnB6ChyoFzhHolylaBXM0PvR5kidctylWps+ObqVFK0qygpGLw8lj3X7F9ca2TN\nJzvzr4qaVzJWt0I9/YTaiDoxOQ1wkbyuqvgfvGOuDdClNJF+Zn2n54ug9efTGxsa\nud8QKHpMA6rmso1M9Vmo917h7InxhcmgrCpb4JKDZRxpUwBrv7sy4q3HadI0foRB\n6T6o3lgTAgMBAAECggEAEhyubSG9dpUX957u1XUhjfSvPbz7xoG85IDzOvoAc4js\nmYYo4bLa5dQGEjtpPYXzQRn6YwlP/MC1jY1lbPHHLKCjyB9ArzDPv3fokqjf3F6x\nqoezOqYNrZtg5cdIJJFw4kKuOxS6qbetilLN5PxuxKpLh53WTZmyfe99UjrsVhTY\nBZusSu9DSy8Z/7UY15BUJ0RhEVFkPQholv0Wrzd7mYnJSUyvhWPZGWOvROrpH/jz\nCSpYW01NDo9QCV051+84KSIqi7NdqsZIgCJLdLN5s0O2TEdzv/jP2pLPDl8TPi4z\nNAdjdegCMEc7Oklr8nwdkKcs/GCJGvtetf4hMu1WQQKBgQD4WHqfS+w4212nSJpR\n56/LMd79/6SK1PN8pBYQKDe8K8UAjA5xd/rlEWVFNsWV6dEdIcvpNo112lZ7aAQz\nZNkpIphDcwNgcepNulwumN8004hzogs3FXdpScnwSrY2Ji0k/IZwgVMwIeK3UWkA\nQuxov0Baug0rb54I7oICEB7cxQKBgQC8l+g2giHmJjpU+nbF+RPh5/jktcbSYbi1\n/otsVcybkgcxWq4mPD/r9/soaDbv/p8LbCVj6onTKMWX0QaS7VFZ338d9xrhGbIX\n7z/gK5HvqTHr02utC8A7/xyjQl+dc4kzOz7/uKPK2lnaJKwzdTZv74BTixefDe7v\nb05U3Fte9wKBgQDcGm7zZ/LAoYtri6laFiFz0Yt1SnGmqf3y5eq3/y0GlTRQu9DB\nODkhdD1xDo4nw8cWLrHuy+6sGQq07QdsFWFyV7rjbLf9bnje0uCIW+zXgPNaqK+P\n7nKa2k8jrNO5QjSYp0bvx27XJfEtz/VjyeyFGZwLzQGHEbHa8KhA89CmkQKBgDZ7\nmB0vKQXpI07rcKau11ya/F9uWDrs+kSxfavVeZ+z5xoN/WOUYk8UO92nhb99iort\nOjwMRLbY/4RlYYXOw4K4O2v3uC8xki6x8n0beTSIZ6CeWmwKigWLJMXRZfgBqbBA\nPGn5+G+g9vY7Q/g1s31Q7ny0ISXVC6LmP/XqFwdvAoGBAJMj1AXXMA/nGJgN1SRs\n6B52MdqjZra60woSAJ/lx/QycUbduLLikhNZJTwlL54SAKXx1bdFs6Bb4P4j86/2\nfKUUojhOU1Jbrm/hbkVSFzpL58LoMYvani1yJzBOY+AxsJO+TqBUU3frh1qF9w/+\n2t/CWAIehILqi2Cbcso2ERtq\n-----END PRIVATE KEY-----\n",
    "client_email": "bionic-workout@bionic-workout.iam.gserviceaccount.com",
    "client_id": "108582586574783695607",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/bionic-workout%40bionic-workout.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"
}

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding-top: 0px !important;  /* Remove padding from the top */
                margin-top: 0px !important; /* Force move the content upwards */
            }
            .element-container {
                margin-top: 0px !important; /* Move element container upwards */
            }
            .stApp {
                margin-top: -10px !important; /* Force the entire app to move upwards */
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Initialize session state variables
session_state_defaults = {
    "set_number": 1,
    "workout_data": [],
    "load_unit": "kg",
    "message": "",
    "show_data": False,
    "heart_rate_data": pd.DataFrame()
}
for key, value in session_state_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# Function to handle exercise change
def exercise_change():
    st.session_state.set_number = 1
    st.rerun()

# Function to handle data submission
def submit_data():
    data = {
        "exercise": st.session_state.exercise,
        "load_unit": st.session_state.load_unit,
        "load_value": st.session_state.load_value,
        "set_number": st.session_state.set_number,
        "reps": st.session_state.reps,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.workout_data.append(data)
    st.session_state.set_number += 1
    st.session_state.message = f"Data submitted successfully at {data['datetime']}"
    st.rerun()

# Function to fetch heart rate data from Google Sheets
def fetch_heart_rate_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1gLThHTU-cz80r_giekxkJktX48jBlWKfTOlNu1wd2RA').worksheet('HR')
    
    # Get all records from the sheet
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    
    # Convert 'datetime' column to datetime objects
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.rename(columns={'datetime': 'time', 'heart_rate': 'heart_rate'}, inplace=True)
   
    return df


def page0():
    # URL to fetch base64 data
    url = "https://raw.githubusercontent.com/BionicAnalyst/images/main/base64.txt"

    # Fetch the base64 image data from the URL
    response = requests.get(url)
    base64_data = response.text

    # Decode the base64 data
    image_data = base64.b64decode(base64_data)

    # Convert the binary data to an image
    image = Image.open(BytesIO(image_data))

    # Display the image in the Streamlit app
    st.image(image, caption="Retrieved Image", use_column_width=True)


# Define Page 1 with the specified elements
def page1():
    st.write("  ")
    st.write("  ")
    st.write("  ")
    # st.markdown("<h1 style='text-align: center;'>🏋️ Workout Data Input</h1>", unsafe_allow_html=True)
    col0, col1 = st.columns([1, 1])
    with col0:
        with card_container(key="exercise_container"):       
            st.write("Exercise")
            st.selectbox("Exercise", ["Lat Pull Down", "Cable Rows", "Floor db press","Cable Flies (Low to High)", "Lateral Raises", "Face Pulls"], key="exercise", on_change=exercise_change, label_visibility="collapsed")
            st.write("  ")
    with col1:
        with card_container(key="load_container"):    
            st.write("Load Value")
            col0, col1 = st.columns([1, 1])
            with col0:
                st.text_input("(e.g., 50)", key="load_value", label_visibility="collapsed")
            with col1:
                load_unit_tab = ui.tabs(options=["kg", "lbs"], default_value=st.session_state.load_unit, className="w-full", key="load_unit_tabs")
                st.session_state.load_unit = load_unit_tab

    col0, col1 = st.columns([1, 1])
    with col0:
        with card_container(key="set_number_container"):
            st.write("Set Number")
            set_number_tab = ui.tabs(options=[str(i) for i in range(1, 10)], default_value=str(st.session_state.set_number), className="w-full", key="set_number_tabs")
            st.session_state.set_number = int(set_number_tab)
            
    with col1:
        with card_container(key="reps_container"):
            st.write("Number of Reps")
            st.slider("Number of Reps", min_value=1, max_value=20, value=10, key="reps", label_visibility="collapsed", help="Adjust the number of reps")

    col0, col1 = st.columns([1, 1])
    with col0:
        ui_result = ui.button("Submit Data", key="submit_btn")
        if ui_result:
            submit_data()
    with col1:
        switch_value = ui.switch(default_checked=st.session_state.show_data, label="Change and Modify Session Data", key="switch1")
        st.session_state.show_data = switch_value

    if st.session_state.show_data:
        with card_container(key="workout_data_container"):
            st.write("Current Workout Data:")
            if st.session_state.workout_data:
                df = pd.DataFrame(st.session_state.workout_data)
                ui.table(data=df, maxHeight=300)
            else:
                st.write("No data submitted yet.")
    
        if st.session_state.message:
            st.success(st.session_state.message)

# Define Page 2 with the dashboard elements
def page2():
    st.session_state.heart_rate_data = fetch_heart_rate_data()
    df = st.session_state.heart_rate_data

    # Set date range for the last 15 days
    end_date = pd.to_datetime(df['time'].max())
    start_date = end_date - pd.Timedelta(days=30)

    # Filter DataFrame to include only the last 15 days
    filtered_df = df[(df['time'] >= start_date) & (df['time'] <= end_date)]

    with card_container(key="heart_rate_evolution_container"):
    # Layout for date selectors and view filter
        col0, col1, col2 = st.columns([1, 1, 1])

        with col1:
            selected_start_date = st.date_input('Select Start Date', value=start_date)
        
        with col2:
            selected_end_date = st.date_input('Select End Date', value=end_date)
        
        with col0:
            view_option = st.selectbox(
                'Select View', 
                options=['Detailed', 'Average per Day'], 
                index=0
            )
        
    # Validate the date range
    if selected_start_date > selected_end_date:
        st.error("Start date must be before or equal to end date.")
    else:
        # Filter data based on selected date range within the last 15 days
        range_data = filtered_df[(filtered_df['time'].dt.date >= selected_start_date) & 
                                 (filtered_df['time'].dt.date <= selected_end_date)]

    # Layout for charts
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        with card_container(key="heart_rate_evolution_container"):
            st.markdown('##### Heart Rate Evolution')
            if view_option == 'Detailed':
                line_chart =  alt.Chart(range_data).mark_line(opacity=0.8).encode(
                    x=alt.X('time:T', title=None, axis=alt.Axis(labelAngle=-45, grid=False)),
                    y=alt.Y('heart_rate:Q', title=None, axis=alt.Axis(grid=False)),
                    tooltip=['time:T', 'heart_rate:Q']
                ).properties(
                    width='container',
                    height=250
                )
            else:  # Average per Day
                daily_avg_hr = range_data.groupby(range_data['time'].dt.date)['heart_rate'].mean().reset_index()
                daily_avg_hr.columns = ['date', 'avg_heart_rate']
                line_chart = alt.Chart(daily_avg_hr).mark_line(opacity=0.8).encode(
                    x=alt.X('date:T', title=None, axis=alt.Axis(labelAngle=-45, grid=False)),
                    y=alt.Y('avg_heart_rate:Q', title=None, axis=alt.Axis(grid=False)),
                    tooltip=['date:T', 'avg_heart_rate:Q']
                ).properties(
                    width='container',
                    height=250
                )
            
            st.altair_chart(line_chart, use_container_width=True)


    with col2:
        with card_container(key="heart_rate_distribution_container"):
            st.markdown('##### Heart Rate Distribution')
            # Set bin size to 10
            bin_size = 10
            min_heart_rate = int((range_data['heart_rate'].min() // bin_size) * bin_size)
            max_heart_rate = int(((range_data['heart_rate'].max() + bin_size - 1) // bin_size) * bin_size)

            # Create bins manually
            bins = list(range(min_heart_rate, max_heart_rate + bin_size, bin_size))

            range_data['bin'] = pd.cut(range_data['heart_rate'], bins)
            bin_counts = range_data['bin'].value_counts().sort_index(ascending=True).reset_index()
            bin_counts.columns = ['bin', 'count']
            bin_counts['bin_start'] = bin_counts['bin'].apply(lambda x: x.left)
            bin_counts = bin_counts.sort_values(by='bin_start')
            bin_labels = [f"{int(b.left)}-{int(b.right)}" for b in bin_counts['bin']]
            bar_data = pd.DataFrame({
                'bin_start': bin_counts['bin_start'],
                'bin_label': bin_labels,
                'count': bin_counts['count'].values
                })
            
            # Sorting by 'bin_start' to ensure correct order
            bar_data = bar_data.sort_values(by='bin_start')

            bar_chart = alt.Chart(bar_data).mark_bar(opacity=0.8, cornerRadius=3).encode(
                x=alt.X('bin_label:N', title=None, sort=bar_data['bin_start'].tolist(), axis=alt.Axis(labelAngle=-45, grid=False)),
                y=alt.Y('count:Q', title=None, axis=alt.Axis(grid=False)),
                tooltip=['bin_label:N', 'count:Q']
            ).properties(
                width='container',
                height=250
            )
            st.altair_chart(bar_chart, use_container_width=True)


    with col3:
        with card_container(key="heart_rate_zones_container"):
            st.markdown('##### Heart Rate Zones Evolution')
            
            # Categorize heart rate into zones
            range_data['zone'] = pd.cut(range_data['heart_rate'], 
                                        bins=[0, 60, 100, range_data['heart_rate'].max()], 
                                        labels=['Low', 'Medium', 'High'])
            
            # Group by date and zone, and count the occurrences
            zones_evolution = range_data.groupby([range_data['time'].dt.date, 'zone']).size().reset_index(name='count')
            
            # Calculate total counts per day for percentage calculation
            daily_totals = zones_evolution.groupby('time')['count'].transform('sum')
            zones_evolution['percentage'] = zones_evolution['count'] / daily_totals * 100
            
            # Create stacked area chart
            zones_chart = alt.Chart(zones_evolution).mark_area(opacity=0.8).encode(
                x=alt.X('time:T', title=None, axis=alt.Axis(labelAngle=-45, grid=False)),
                y=alt.Y('percentage:Q', title='Percentage', axis=alt.Axis(grid=False)),
                color=alt.Color('zone:N', legend=None),
                tooltip=['time:T', 'zone:N', 'count:Q', 'percentage:Q']
            ).properties(
                width='container',
                height=250
            )
            
            st.altair_chart(zones_chart, use_container_width=True)

def fetch_workout_data():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1gLThHTU-cz80r_giekxkJktX48jBlWKfTOlNu1wd2RA').worksheet('Workout')
    
    # Get all records from the sheet
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    
    # Convert 'datetime' column to datetime objects
    df['datetime'] = pd.to_datetime(df['datetime'])
    return df


def page3():
    # Fetch workout data if not already fetched
    st.session_state.workout_data = fetch_workout_data()
    df = st.session_state.workout_data

    exercise_options = df['exercise'].unique()
    

    with card_container(key="heart_rate_zones_container"):
        col1, col2, col3 = st.columns([5, 1, 1])
        with col1:
            selected_exercises = st.multiselect('Select Exercise', exercise_options, default=exercise_options[:3])
        with col2:
            start_date = st.date_input("Start Date",min_value=df['datetime'].min().date(), value=df['datetime'].min().date())
        with col3:
            end_date = st.date_input("End Date", max_value=df['datetime'].max().date(), value=df['datetime'].max().date())

    # Filter data based on selected exercises and date range
    filtered_df = df[
        (df['exercise'].isin(selected_exercises)) &
        (df['datetime'].dt.date >= start_date) &
        (df['datetime'].dt.date <= end_date)
    ]

    # Create a new column for volume
    filtered_df['volume'] = filtered_df['load_value'].astype(float) * filtered_df['reps'].astype(int)

    # Aggregate data
    daily_summary = filtered_df.groupby([filtered_df['datetime'].dt.date, 'exercise']).agg(
        total_volume=('volume', 'sum'),
        max_load=('load_value', 'max'),
        total_reps=('reps', 'sum'),
        total_sets=('set_number', 'sum')
    ).reset_index()

    daily_summary['datetime'] = pd.to_datetime(daily_summary['datetime']).dt.strftime('%d-%m')
    daily_summary['total_volume'] = daily_summary['total_volume'].astype(float)
    daily_summary['max_load'] = daily_summary['max_load'].astype(float)
    daily_summary['total_reps'] = daily_summary['total_reps'].astype(int)
    daily_summary['total_sets'] = daily_summary['total_sets'].astype(int)

    overall_max_load = filtered_df.groupby('exercise').agg(max_load=('load_value', 'max')).reset_index()
    overall_max_load['max_load'] = overall_max_load['max_load'].astype(float)

    # Plotting

    col0, col1, col2 = st.columns([1, 1, 1])
    
    
    with col2:
        with card_container(key="heart_rate_zones_container"):
            st.markdown('##### Volume per Day')
            st.markdown('')
            volume_chart = alt.Chart(daily_summary).mark_area(opacity=0.8,cornerRadius=3).encode(
                x=alt.X('datetime:O', title=None, axis=alt.Axis(labelAngle=-45,grid=False)),
                y=alt.Y('total_volume:Q', title=None, axis=alt.Axis(grid=False)),
                color=alt.Color('exercise:N', legend=None),
                tooltip=['datetime:O', 'exercise:N', 'total_volume:Q']
            ).properties(
                width='container',
                height=250
            )
            st.altair_chart(volume_chart, use_container_width=True)

    with col1:
        with card_container(key="heart_rate_zones_container"):
            st.markdown('##### Total Reps per Day')
            st.markdown('')
            total_reps_chart = alt.Chart(daily_summary).mark_bar(opacity=0.8,cornerRadius=3).encode(
                x=alt.X('datetime:O', title=None, axis=alt.Axis(labelAngle=-45,grid=False)),
                y=alt.Y('total_reps:Q', title=None, axis=alt.Axis(grid=False)),
                color=alt.Color('exercise:N', legend=None),
                tooltip=['datetime:O', 'exercise:N', 'total_reps:Q']
            ).properties(
                width='container',
                height=250
            )

            st.altair_chart(total_reps_chart , use_container_width=True)
    
    with col0:
        with card_container(key="heart_rate_zones_container"):
            st.markdown('##### Maximum Load (Kg)')
            st.markdown('')
            max_load_chart = alt.Chart(overall_max_load).mark_bar(opacity=0.8,cornerRadius=3).encode(
                y=alt.Y('exercise:N', title=None, sort='-x', axis=alt.Axis(grid=False)),
                x=alt.X('max_load:Q', title=None, axis=alt.Axis(grid=False)),
                color=alt.Color('exercise:N', legend=None),
                tooltip=['exercise:N', 'max_load:Q'],
                text=alt.Text('max_load:Q')
            ).properties(
                width='container',
                height=250
            ).configure_mark(
                color='teal'  # Modern color
            ).configure_text(
                fontSize=12,
                color='black'
            )

            st.altair_chart(max_load_chart , use_container_width=True)



# Add the new page to navigation
def navigation():

    page = option_menu(
            menu_title=None,
            options=["main","HR Dashboard", "Workout Dashboard","Workout Input"],
            icons=["info-lg","activity", "bar-chart", "clipboard"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
        )
    if page == "main":
        page0()
    elif page == "Workout Input":
        page1()
    elif page == "HR Dashboard":
        page2()
    elif page == "Workout Dashboard":
        page3()

# Run the navigation function
navigation()