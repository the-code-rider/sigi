<img src="https://raw.githubusercontent.com/the-code-rider/sigi/main/logo.png" alt="drawing" width="200"/>

# SIGI: Simple Image Gen UI

I primarily wrote this app because I wanted to generate a bunch of images using Stability AI without having to wait for the result.
Just pass in one prompt after the other and have the app call the API and store the result.

Right now only Stability AI API is supported. I plan to add support for more models soon. 

If you are looking to run models locally, then you should take a look at [comfy ui](https://github.com/comfyanonymous/ComfyUI)

# Installation

1. Clone the repository
2. Install requirements  
`pip install -r requirements.txt`
3. Launch the app   
`streamlit run main.py`
4. Setting up API credential  
    a. you can either set the environment variable STABILITY_API_KEY  
    **Windows**  
    `set STABILITY_API_KEY=add_key_here`   
    
    **Linux and macOS** 
    `export STABILITY_API_KEY=add_key_here`

     b. Or create a streamlit secrets files  
     `mkdir .streamlit`  
     `touch .streamlit/secrets.toml`  
      edit the secrets.toml file  
        stability_api_key = 'add_key_here'

## Via Docker

**ToDo: setup docker** 

## Demo  

<video src="https://github.com/the-code-rider/sigi/raw/main/demo.mp4"></video>

