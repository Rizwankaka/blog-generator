# YouTube Code Tutorial Blog Generator

A Streamlit application that converts YouTube coding tutorials into well-structured blog posts with code analysis.

## Features

- Extract and analyze YouTube video transcripts
- Analyze GitHub repository code
- Generate comprehensive blog posts
- Professional formatting and styling
- Easy-to-use interface

## Environment Variables

The following environment variables are required:

- `GOOGLE_API_KEY`: Your Google API key for Gemini Pro
- `GITHUB_TOKEN`: Your GitHub personal access token

## Local Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/youtube-code-tutorial-blog-generator.git
cd youtube-code-tutorial-blog-generator
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your environment variables:

```
GOOGLE_API_KEY=your_google_api_key
GITHUB_TOKEN=your_github_token
```

5. Run the application:

```bash
streamlit run main.py
```

## Deployment

The application is deployed on Vercel at: [your-app-url]

## License

MIT
