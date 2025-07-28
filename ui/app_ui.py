import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.agents.readme_generator import ReadmeGenerator
from app.agents.code_extractor import CodeExtractor
import tempfile
import shutil
import git

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
    st.title("AI README Generator")

    repo_url = st.text_input("Enter GitHub Repo URL (HTTPS)")

    if st.button("Generate README"):
        if not repo_url:
            st.warning("Please enter a valid GitHub repo URL.")
            return

        with st.spinner("Cloning repo and generating README..."):
            local_path = clone_repo(repo_url)
            if not local_path:
                return

            extractor = CodeExtractor(local_path)
            repo_summary = extractor.extract()

            readme_gen = ReadmeGenerator()
            readme_md, review_report = readme_gen.generate_readme_markdown(repo_summary, local_path)

            st.subheader("Generated README.md")
            st.code(readme_md, language="markdown")

            st.subheader("Review Report")
            st.text(review_report)

            st.download_button("Download README.md", data=readme_md, file_name="README.md")
            shutil.rmtree(local_path)

if __name__ == "__main__":
    main()
