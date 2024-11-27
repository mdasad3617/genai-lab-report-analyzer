import streamlit as st
import logging
from models.summarizer import TextSummarizer
from services.text_input_handler import handle_text_input
from services.file_input_handler import read_text_file, read_pdf_file, read_docx_file
from services.audio_input_handler import audio_to_text
from utils.logging_utils import setup_logging


def main():
    # Setup logging
    setup_logging()
    logging.info("Starting GenAI Lab Report Analyzer with Streamlit.")
    
    # Initialize summarizer
    summarizer = TextSummarizer()

    # Streamlit UI
    st.title("GenAI Lab Report Analyzer")
    st.write("Upload a file, record audio, or type text to generate a summary. Select the appropriate input type and provide the input.")

    input_type = st.radio(
        "Select Input Type:",
        options=["Text", "Text File", "PDF", "DOCX", "Audio"],
        index=0
    )

    file = None
    text = None
    audio = None

    if input_type == "Text":
        text = st.text_area("Enter your text here:", placeholder="Type your text here...")
    elif input_type in ["Text File", "PDF", "DOCX"]:
        file = st.file_uploader(f"Upload your {input_type}:", type=["txt", "pdf", "docx"])
    elif input_type == "Audio":
        audio = st.file_uploader("Upload your audio file:", type=["wav", "mp3", "m4a"])

    if st.button("Summarize"):
        try:
            if input_type == "Text" and text:
                logging.info("Processing text input.")
                processed_text = handle_text_input(text)
                summary = summarizer.summarize(processed_text)
                logging.info("Text input processed successfully.")
            elif input_type in ["Text File", "PDF", "DOCX"] and file:
                if input_type == "Text File":
                    logging.info(f"Processing text file: {file.name}")
                    processed_text = read_text_file(file)
                elif input_type == "PDF":
                    logging.info(f"Processing PDF file: {file.name}")
                    processed_text = read_pdf_file(file)
                elif input_type == "DOCX":
                    logging.info(f"Processing DOCX file: {file.name}")
                    processed_text = read_docx_file(file)
                
                if processed_text:
                    summary = summarizer.summarize(processed_text)
                    logging.info(f"{input_type} processed successfully.")
                else:
                    summary = "Failed to process the file. Check logs for more details."
                    logging.error(f"Failed to process {input_type}: {file.name}")
            elif input_type == "Audio" and audio:
                logging.info("Processing audio input.")
                processed_text = audio_to_text(audio)
                if processed_text:
                    summary = summarizer.summarize(processed_text)
                    logging.info("Audio input processed successfully.")
                else:
                    summary = "Failed to convert audio to text. Check logs for more details."
                    logging.error("Failed to convert audio to text.")
            else:
                summary = "Invalid input. Please provide a valid file or text."
                logging.warning("Invalid input type provided.")

            st.text_area("Summary Result:", summary, height=200)
        except Exception as e:
            logging.error(f"Error during summarization: {e}")
            st.error("An error occurred during summarization. Please check the logs for more details.")

    logging.info("Closing GenAI Lab Report Analyzer with Streamlit.")


if __name__ == "__main__":
    main()
