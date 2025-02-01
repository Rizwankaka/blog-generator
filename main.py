import streamlit as st
from importlib import reload
import agents.blog_generator
reload(agents.blog_generator)
from agents.blog_generator import BlogGeneratorGraph
from pathlib import Path
import json
from datetime import datetime

def main():
    st.set_page_config(layout="wide")
    
    # Add custom CSS
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("🤖 YouTube Code Tutorial Blog Generator")
    st.markdown("""
    Transform YouTube coding tutorials into well-structured blog posts with code analysis.
    Just provide the YouTube URL and GitHub repository link!
    """)
    
    # Create two columns for input
    col1, col2 = st.columns(2)
    
    with col1:
        youtube_url = st.text_input("🎥 YouTube Video URL")
    with col2:
        github_repo = st.text_input("📦 GitHub Repository URL")
    
    if st.button("🚀 Generate Blog"):
        if not youtube_url or not github_repo:
            st.error("Please provide both YouTube URL and GitHub repository URL")
            return
            
        with st.spinner("🔄 Analyzing content and generating blog..."):
            try:
                # Initialize the graph
                generator = BlogGeneratorGraph()
                graph = generator.create_graph()
                
                # Prepare initial state
                initial_state = {
                    "video_id": extract_video_id(youtube_url),
                    "github_repo": github_repo
                }
                
                # Execute the graph
                result = graph.invoke(initial_state)
                
                # Display blog content
                st.markdown(result["blog_content"], unsafe_allow_html=True)
                
                # Add download button
                if st.button("💾 Save Blog"):
                    save_blog(result["blog_content"])
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    if "youtube.com" in url:
        video_id = url.split("v=")[1].split("&")[0]
    elif "youtu.be" in url:
        video_id = url.split("/")[-1]
    else:
        raise ValueError("Invalid YouTube URL")
    return video_id

def save_blog(content: str):
    """Save blog content to file"""
    output_dir = Path("generated_blogs")
    output_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"blog_{timestamp}.md"
    
    # Remove HTML styling for markdown file
    content_md = content.split('<div class="blog-content">')[-1].split('</div>')[0]
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content_md)
    
    st.success(f"✅ Blog saved to {output_file}")

if __name__ == "__main__":
    main() 