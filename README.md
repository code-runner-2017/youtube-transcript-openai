# Youtube Transcript OpenAI

This utility:

    - downloads the transcript of any Youtube video
    - uses OpenAI's API to summarize and extract key points from the video
    - saves everything in a local file in markdown format

## Requirements

You need an OpenAI API key and Python v3. 

## Setup Instructions

    # create and activate a virtual env
    python -m venv venv
    source venv/bin/activate
    # clone this repository
    git clone https://github.com/code-runner-2017/youtube-transcript-openai.git
    cd youtube-transcript-openai
    # install dependencies
    pip install -r requirements.txt
    cp .env.example .env
    # customize your .env file with your API KEY, adjust prompts, etc.

## How to Run

    python main.py "http://youtube.com/...."
    python main.py    # will prompt for the Youtube link

Wait a few seconds and you'll get the output file under the `output/` folder.

## Sponsor

<a href="https://buymeacoffee.com/igliop3" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>