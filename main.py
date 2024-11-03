import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL")
OPENAI_TEMPERATURE=int(os.environ.get("OPENAI_TEMPERATURE"))

openai = OpenAI(api_key=OPENAI_API_KEY)

# Given the video title, normalize it to a valid file name.
def normalize_video_title(title):
    return re.sub(r'[\\/*?:"<>|]', '_', title)

def add_indentation(text, spaces_count=2):
    """
    Add spaces at the beginning of each line in a multi-line string.
    """
    # Split the text into lines, add 4 spaces to each line, and join them back with newline characters
    spaces = ' ' * spaces_count
    indented_text = '\n'.join([spaces + line for line in text.splitlines()])
    return indented_text

################################
def generate_text_from_prompt(prompt, transcript): 
    response = openai.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=OPENAI_TEMPERATURE,
        messages=[
            {
                "role": "system",
                "content": os.environ.get("SYSTEM_PROMPT")  
            },
            {
                "role": "user",
                "content": prompt + transcript
            }
        ]
    )
    return response.choices[0].message.content

def write_separator(file, description, space_before=True):
    file.write(f"\n\n\n") if space_before else None
    file.write(f"## {description}\n")
    file.write(f"\n")

def generate_text_from_all_prompts(file, transcript):
    transcript = generate_text_from_prompt(os.environ.get("PROMPT_PUNCTUATION"), transcript)
    write_separator(file, "Transcript")
    file.write(add_indentation(transcript))
    key_points = generate_text_from_prompt(os.environ.get("PROMPT_KEY_POINTS"), transcript)
    write_separator(file, "Key Points")
    file.write(add_indentation(key_points))
    summary = generate_text_from_prompt(os.environ.get("PROMPT_SUMMARIZE"), transcript)
    write_separator(file, "Summary")
    file.write(add_indentation(summary))

def get_video_title(video_url):
    """
    Get the video title from YouTube using the video ID.
    """
    try:
        response = requests.get(video_url)
        response.raise_for_status()
        #response = re.get(url)
        #response.raise_for_status()
        matches = re.findall(r'<title>(.*?)</title>', response.text)
        return matches[0].replace(" - YouTube", "") if matches else "Unknown"
    except re.RequestException as e:
        print(f"Error fetching video title: {e}")
        return "Unknown title"


def get_video_id(url):
    """
    Extract the video ID from the YouTube URL.
    """
    match = re.search(r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None

def download_transcription(video_id):
    """
    Download the transcription of a YouTube video given its ID.
    """
    
    try:
        # Fetch the transcription
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Format the transcript to plain text
        formatter = TextFormatter()
        formatted_transcript = formatter.format_transcript(transcript)
        
        return formatted_transcript
    
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    if len(sys.argv) == 1:
        youtube_url = input("Enter the YouTube video link: ")
    else:
        youtube_url = sys.argv[1]

    video_id = get_video_id(youtube_url)

    if video_id:
        transcript_text = download_transcription(video_id)
        if transcript_text:
            video_title = normalize_video_title(get_video_title(youtube_url))
            output_dir = 'output'
            file_name = f"{video_id}_{video_title}.txt"
            file_name = re.sub(r'[\\/*?:"<>|]', '', file_name)  # Remove invalid characters
            file_name = f"{output_dir}/{file_name}"
            
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # remove newlines
            # transcript_text = transcript_text.replace("\n", " ")

            with open(file_name, 'w', encoding='utf-8') as file:
                write_separator(file, "Original Unprocessed Transcript", False)
                file.write(f"[Link to the Video]({youtube_url})\n\n")
                file.write(transcript_text)
                generate_text_from_all_prompts(file, transcript_text)


            print(f"Transcript and OpenAI output saved to {file_name}")
        else:
            print("Cannot download the transcript.")
    else:
        print("Invalid YouTube URL")

if __name__ == "__main__":
    main()
