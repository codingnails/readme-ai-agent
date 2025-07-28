import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.agents.readme_generator import ReadmeGenerator
from app.agents.code_extractor import CodeExtractor
import tempfile
import shutil
import git

def set_dark_theme():
    st.markdown(
        """
        <style>
        /* Background */
        .stApp {
            background-color: #1e1e1e;
            color: white;
        }
        /* Input fields */
        .stTextInput > div > div > input {
            background-color: #2c2c2c;
            color: white;
            border: 1px solid #444;
        }
        /* Buttons */
        button[kind="primary"] {
            background-color: #3a3a3a;
            color: white;
            border: 1px solid #555;
        }
        button[kind="primary"]:hover {
            background-color: #555;
        }
        /* Code blocks */
        pre {
            background-color: #2b2b2b !important;
            color: #e0e0e0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def clone_repo(repo_url):
    temp_dir = tempfile.mkdtemp(prefix="repo_")
    try:
        git.Repo.clone_from(repo_url, temp_dir)
        return temp_dir
    except Exception as e:
        st.error(f"Failed to clone repo: {e}")
        shutil.rmtree(temp_dir)
        return None

def main():
    set_dark_theme()
    st.markdown("Built by Rupali Gupta<br>Email: rupaligupta.tech@gmail.com", unsafe_allow_html=True)
    st.title("AI README Generator")
    st.write("Here's a quick demo of my project that generates professional README files using AI.")
    repo_url = st.text_input("Enter GitHub Repo URL (HTTPS)")

    if st.button("Generate README"):
        if not repo_url:
            st.warning("Please enter a valid GitHub repo URL.")
            return

        with st.spinner("Cloning repo and generating README..."):
            local_path = clone_repo(repo_url)
            if not local_path:
                return

            extractor = CodeExtractor(local_path,repo_url)
            repo_summary = extractor.extract()

            readme_gen = ReadmeGenerator()
            readme_md, review_report = readme_gen.generate_readme_markdown(repo_summary, local_path)

            tab1, tab2 = st.tabs(["Generated README.md", "AI Agent Review Report"])

            with tab1:
                # Use markdown rendering for better appearance
                st.markdown(readme_md, unsafe_allow_html=True)

            with tab2:
                st.markdown(review_report, unsafe_allow_html=True)

            st.download_button("Download README.md", data=readme_md, file_name="README.md")
            shutil.rmtree(local_path)

if __name__ == "__main__":
    main()
