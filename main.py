from PyPDF2 import PdfReader
import spacy
from googleapiclient.discovery import build
import openai
from dotenv import load_dotenv
import os
from youtube_transcript_api import YouTubeTranscriptApi
from fpdf import FPDF

# Function to extract video ID from URL
def extract_video_id(url):
    # This is a simplified extractor, consider using more robust methods for different URL formats
    return url.split("v=")[-1]

# Function to get video transcript
def get_video_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en']).fetch()
        full_transcript = " ".join([t['text'] for t in transcript])
        return full_transcript
    except Exception as e:
        print(f"An error occurred while fetching the transcript: {e}")
        return None

# Function to summarize transcript
def summarize_transcript(transcript):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Provide a detailed summary of the following transcript:\n{transcript}"}
        ],
        temperature=0.7,
        max_tokens=1024
    )
    summary = response.choices[0].message["content"].strip()
    return summary

# Function to create PDF from text
def create_pdf(text, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(pdf_path)

# Main function to process a YouTube video URL and generate a PDF summary
def youtube_video_to_pdf(video_url, pdf_path):
    video_id = extract_video_id(video_url)
    transcript = get_video_transcript(video_id)
    if transcript:
        summary = summarize_transcript(transcript)
        create_pdf(summary, pdf_path)
        print(f"PDF summary created at {pdf_path}")
    else:
        print("Failed to create summary.")

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Example usage
youtube_video_url = "https://www.youtube.com/watch?v=kqtD5dpn9C8&t=791s"
output_pdf_path = "video_summary.pdf"  # Specify the desired output PDF file path
youtube_video_to_pdf(youtube_video_url, output_pdf_path)
