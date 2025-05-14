# Menu to Braille Converter

An AI-powered application that converts food menu images to Braille text for visually impaired users.

## Features

- Upload menu images
- Extract text using AI-powered document understanding (LayoutLMv2)
- Process and structure menu text using LLMs
- Convert text to Braille
- Display Braille in multiple formats (text, visual, side-by-side)
- Download as PDF in different formats

## Deployment on Hugging Face Spaces

### Option 1: Direct GitHub Repository Deployment

1. Fork this repository to your GitHub account
2. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
3. Click "Create new Space"
4. Choose "Streamlit" as the SDK
5. Connect your GitHub account and select this repository
6. Choose hardware requirements (recommend at least GPU for better performance)
7. Click "Create Space"

### Option 2: Manual Deployment

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Streamlit" as the SDK
4. Give your Space a name
5. Choose hardware requirements (recommend at least GPU for better performance)
6. Click "Create Space"
7. Clone the Space repository locally
8. Copy all files from this project to the cloned repository
9. Push the changes to the Space repository

## Hardware Requirements

- **Minimum**: CPU (2 vCPUs, 16 GB RAM)
- **Recommended**: GPU (T4 or better)

## Models Used

- **Document AI**: microsoft/layoutlmv2-base-uncased
- **Text Processing**: meta-llama/Meta-Llama-3-8B-Instruct (with fallback to mistralai/Mistral-7B-Instruct-v0.2)
- **Context Enhancement**: facebook/bart-large-cnn

## Local Development

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt` 
3. Run the application: `streamlit run app.py`


## Future Enhancements

- Improved menu section recognition
- Support for multiple languages
- Physical Braille printer integration
- Mobile app version
