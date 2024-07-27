from openai import OpenAI
import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi

st.title("Compedia")

client=OpenAI(api_key="")

prompt="""You are Yotube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words. Please provide the summary of the text given here:  """

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
# Call ChatGPT API to generate summary
def generate_summary(prompt):
    try:
        # Example OpenAI Python library request
        MODEL = "gpt-3.5-turbo"
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": prompt}
            ],
            temperature=0,
        )

        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        raise e

# Main Streamlit app
def main():

    # Get YouTube video link from user
    youtube_video_url = st.text_input("Enter YouTube Video URL:")

    if st.button("Generate Summary"):
        if youtube_video_url:
            try:
                # Get transcript text from YouTube video
                transcript = extract_transcript_details(youtube_video_url)

                # Generate summary using ChatGPT API
                summary = generate_summary(prompt + transcript)

                # Display summary
                st.subheader("Summary:")
                st.write(summary)

            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a YouTube video URL.")

if __name__ == "__main__":
    main()
