from typing import Dict, List, Any
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, Graph
from langchain_google_genai import ChatGoogleGenerativeAI
from youtube_transcript_api import YouTubeTranscriptApi
from github import Github
from config import Config

class BlogGeneratorGraph:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=Config.GOOGLE_API_KEY
        )
        self.github_client = Github(Config.GITHUB_TOKEN)
        
    def create_graph(self) -> Graph:
        # Initialize the graph with Dict type
        workflow = StateGraph(Dict)

        # Define nodes/agents
        workflow.add_node("transcript_agent", self.get_transcript)
        workflow.add_node("code_analyzer", self.analyze_github_code)
        workflow.add_node("content_summarizer", self.summarize_content)
        workflow.add_node("blog_formatter", self.format_blog)

        # Define edges - both transcript and code analysis must complete before summarization
        workflow.add_edge("transcript_agent", "code_analyzer")
        workflow.add_edge("code_analyzer", "content_summarizer")
        workflow.add_edge("content_summarizer", "blog_formatter")

        # Set entry point
        workflow.set_entry_point("transcript_agent")

        return workflow.compile()

    def get_transcript(self, state: Dict) -> Dict:
        """Extract transcript from YouTube video"""
        video_id = state["video_id"]
        try:
            # Get transcript using YouTubeTranscriptApi
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            # Combine all transcript text
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            return {**state, "transcript": full_transcript}
        except Exception as e:
            return {**state, "transcript": f"Error getting transcript: {str(e)}"}

    def analyze_github_code(self, state: Dict) -> Dict:
        """Analyze code from GitHub repository"""
        repo_url = state["github_repo"]
        try:
            repo = self.github_client.get_repo(repo_url)
            
            # Get main code files
            code_files = []
            contents = repo.get_contents("")
            for content in contents:
                if content.path.endswith(('.py', '.ipynb')):
                    code_files.append({
                        "path": content.path,
                        "content": content.decoded_content.decode()
                    })
            
            return {**state, "code_analysis": code_files}
        except Exception as e:
            return {**state, "code_analysis": f"Error analyzing code: {str(e)}"}

    def summarize_content(self, state: Dict) -> Dict:
        """Summarize video transcript and code content"""
        try:
            prompt = f"""
            Analyze the following video transcript and code files to create a comprehensive summary:
            
            Transcript: {state.get('transcript', 'No transcript available')}
            
            Code Files: {state.get('code_analysis', 'No code analysis available')}
            
            Create a detailed technical summary including:
            1. Main concepts covered
            2. Key implementation details
            3. Important code snippets
            4. Prerequisites and setup requirements
            """
            
            summary = self.llm.invoke(prompt).content
            return {**state, "summary": summary}
        except Exception as e:
            return {**state, "summary": f"Error creating summary: {str(e)}"}

    def format_blog(self, state: Dict) -> Dict:
        """Format content into blog structure"""
        try:
            prompt = f"""
            Convert the following summary into a well-structured technical blog post:
            {state.get('summary', 'No summary available')}
            
            Create a professional blog post with the following structure:
            1. A clear, descriptive title that captures the main topic
            2. A brief introduction explaining what will be covered
            3. Prerequisites section listing all required tools and libraries
            4. Implementation section with:
               - Step-by-step instructions
               - Code snippets with proper markdown formatting
               - Clear explanations for each step
            5. Key features and capabilities
            6. Conclusion summarizing the main points
            
            Format Requirements:
            - Use markdown formatting
            - Use code blocks with language specification (```python)
            - Use headers with appropriate levels (# for title, ## for main sections)
            - Include bullet points where appropriate
            - Make code snippets easy to copy and use
            - Add brief explanations before each code block
            - Include any setup instructions or environment configurations
            """
            
            # Get the content from AIMessage
            blog_content = self.llm.invoke(prompt).content
            formatted_content = self._add_styling(blog_content)
            return {**state, "blog_content": formatted_content}
        except Exception as e:
            return {**state, "blog_content": f"Error formatting blog: {str(e)}"}
    
    def _add_styling(self, content: str) -> str:
        """Add additional styling and formatting to the blog content"""
        # Add CSS styling
        styled_content = """
        <style>
        .blog-content {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            font-family: 'Arial', sans-serif;
        }
        .blog-content h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .blog-content h2 {
            color: #34495e;
            margin-top: 30px;
        }
        .blog-content pre {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .blog-content code {
            font-family: 'Consolas', monospace;
        }
        .blog-content p {
            line-height: 1.6;
            color: #2c3e50;
        }
        .blog-content ul {
            padding-left: 20px;
        }
        .blog-content li {
            margin: 10px 0;
        }
        </style>
        <div class="blog-content">
        """
        
        # Add the content
        styled_content += content
        
        # Close the div
        styled_content += "</div>"
        
        return styled_content 