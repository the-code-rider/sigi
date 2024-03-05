import time

import streamlit as st
import os
from stability_ai_client import StabilityClient
from db_dml import DBDML


def _load_secret():
    if st.secrets['stability_api_key']:
        return st.secrets['stability_api_key']
    if os.getenv('STABILITY_API_KEY'):
        return os.getenv('STABILITY_API_KEY')

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
                pending_jobs = db_dml.get_pending_jobs()
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

                    except Exception as e:
                        print(e)
                        db_dml.update_job_status(job_id, 'FAILED')

            # import time
            # time.sleep(40)
            # st.write('just woke up')


def browse_pictures_page():
    st.title("Browse Pictures")
    # Example images and texts. In a real app, these would come from your database or an API
    images = ["image1.png", "image2.png", "image3.png"]  # Example image paths
    texts = ["Image 1", "Image 2", "Image 3"]  # Example texts associated with the images

    for i, img in enumerate(images):
        st.image(img, caption=texts[i])


# Define a function for the Job List page
def job_list_page():
    st.title("Job List")
    if st.button('View All'):
        all_jobs = db_dml.get_job_by_status(status='ALL')
        st.dataframe(all_jobs)
    if st.button('View Pending Jobs'):
        pending_jobs = db_dml.get_job_by_status(status='TODO')
        st.dataframe(pending_jobs)
    # Example job list. In a real app, this would come from your database
    jobs = ["Job 1", "Job 2", "Job 3"]
    for job in jobs:
        st.write(job)
