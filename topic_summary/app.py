import streamlit as st
import sys
import os
from pathlib import Path

# Add the src directory to the path so we can import the topic_summary package
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from topic_summary.crew import TopicSummaryCrew

def run():
    st.set_page_config(page_title="AI Topic Summary Crew", page_icon="🤖")
    
    st.title("🤖 AI Topic Summary Crew")
    st.markdown("Build a mini multi-agent system that researches and summarizes any topic!")

    # Sidebar for API Keys
    with st.sidebar:
        st.header("Configuration")
        openai_key = st.text_input("Enter OpenAI API Key", type="password")
        serper_key = st.text_input("Enter Serper API Key", type="password")
        
        if openai_key:
            os.environ["OPENAI_API_KEY"] = openai_key
        if serper_key:
            os.environ["SERPER_API_KEY"] = serper_key

    topic = st.text_input("Enter a topic to research:", placeholder="e.g., Space Exploration")

    if st.button("Kickoff Crew"):
        if not topic:
            st.warning("Please enter a topic.")
        elif not os.getenv("OPENAI_API_KEY") or not os.getenv("SERPER_API_KEY"):
            st.error("Please provide both OpenAI and Serper API Keys.")
        else:
            with st.status("🚀 Crew is working...", expanded=True) as status:
                st.write("Gathering facts...")
                try:
                    inputs = {"topic": topic}
                    crew_instance = TopicSummaryCrew().crew()
                    result = crew_instance.kickoff(inputs=inputs)
                    
                    st.success("Research and Summarization complete!")
                    
                    # Display the final summary
                    st.header("Summary Output")
                    st.markdown(result.raw)
                    
                    # Optional: Display tool usage/stats if available
                    if hasattr(result, 'token_usage'):
                        with st.expander("Token Usage Stats"):
                            st.write(result.token_usage)
                    
                    status.update(label="Complete!", state="complete", expanded=False)
                except Exception as e:
                    if "403" in str(e) or "Unauthorized" in str(e):
                        st.error("❌ API Authorization Error: It looks like your Serper API Key is incorrect or unauthorized. Please check your key at serper.dev.")
                    else:
                        st.error(f"An error occurred: {e}")
                    status.update(label="Error!", state="error", expanded=False)

if __name__ == "__main__":
    run()
