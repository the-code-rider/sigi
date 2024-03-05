from pages import *


def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Generate", "Browse Pictures", "Job List"))

    # Page routing
    if page == "Generate":
        generate_page()
    elif page == "Browse Pictures":
        browse_pictures_page()
    elif page == "Job List":
        job_list_page()


if __name__ == '__main__':
    main()
