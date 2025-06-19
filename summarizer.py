import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from google import genai
from google.genai import types
import re
import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv('GEMINI-API-KEY')

client = genai.Client(api_key = key)


def get_video(url):
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    if match:
        return match.group(1)
    else:
        return None

def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = " ".join([item["text"] for item in transcript])
    return text

def summarize_text(text):
    prompt = "Summarize this YouTube video transcript in a concise and clear way:\n\n" + text
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0) # Disables thinking
    ),
)
    return response.text
  
st.title("Summarizer your YouTube Video")
url = st.text_input("Enter Video Link : ")

if st.button("Enter"):
    if url:
        video_id = get_video(url)
        if not video_id:
            st.error("Invalid YouTube URL.")
        else:
            with st.spinner("Getting your transcript"):
                transcript = fetch_transcript(video_id)

            if transcript.startswith("Error"):
                st.error(transcript)
            else:
                st.success("Transcript fetched!")
                with st.spinner("Summarizing..."):
                    summary = summarize_text(transcript)
                st.subheader("📝 Summary:")
                st.write(summary)