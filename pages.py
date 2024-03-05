import time

import streamlit as st
import os
from stability_ai_client import StabilityClient
from db_dml import DBDML
from utils import *

@st.cache_data
def _load_secret():
    if os.getenv('STABILITY_API_KEY'):
        print("secret key found")
        return os.getenv('STABILITY_API_KEY')
    if st.secrets['stability_api_key']:
        return st.secrets['stability_api_key']

    raise Exception('Stability API Key Not Found')


api_key = _load_secret()
db_dml = DBDML()
sclient = StabilityClient(api_key)


def generate_page():
    st.title("Image Generation")
    theme_input = st.text_input("Enter theme")
    user_input = st.text_input("Enter your prompt")
    b1, b2 = st.columns(2)

    user_prompt = f'{user_input}, {theme_input}'

    with b1:
        if st.button("Generate"):
            if user_input:
                st.write("image gen queued for :", user_prompt)
                db_dml.add_to_job_queue(prompt=user_prompt, status='TODO')

            # trigger the loop
            while True:
                pending_jobs = db_dml.get_job_by_status('TODO')
                if pending_jobs.empty:
                    break
                for _, row in pending_jobs.iterrows():
                    prompt = row['prompt']
                    job_id = row['id']
                    try:
                        image = sclient.generate(prompt=prompt)
                        if image:
                            db_dml.update_job_status(job_id, 'COMPLETED')
                            db_dml.add_to_result(prompt=prompt, image=image)
                        else:
                            db_dml.update_job_status(job_id, 'FAILED')

                    except Exception as e:
                        print(e)
                        db_dml.update_job_status(job_id, 'FAILED')


@st.cache_data
def display_pictures(images_df):
    for _, row in images_df.iterrows():
        image_str = row['image']
        try:
            image = base64_to_image(image_str)
            st.image(image, caption=f'{row["prompt"]} @ {row["timestamp"]}')
        except Exception as e:
            print('failed to convert image')
            print(e)


def browse_pictures_page():
    images_df = db_dml.get_images()
    images_df_sorted = images_df.sort_values(by='timestamp', ascending=False)
    display_pictures(images_df_sorted)

    if (st.button('Show Table Entries')):
        st.dataframe(images_df_sorted)


# Define a function for the Job List page
def job_list_page():
    st.title("Job List")
    if st.button('View All'):
        all_jobs = db_dml.get_job_by_status(status='ALL')
        st.dataframe(all_jobs)
    if st.button('View Pending Jobs'):
        pending_jobs = db_dml.get_job_by_status(status='TODO')
        st.dataframe(pending_jobs)
