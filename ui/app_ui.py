import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from app.agents.readme_agent import ReadmeGenerator
from app.core.code_extractor import CodeExtractor
from app.core.repo_fetcher import RepoFetcher
from app.utils.semantic_extractor import SemanticExtractor
from app.utils.agent_graph import run_readme_agent
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
            # Step 1: Clone the repo
            fetcher = RepoFetcher()
            local_path = fetcher.fetch_repo(repo_url)
            if not local_path:
                return

            extractor = CodeExtractor(local_path,repo_url)
            repo_summary = extractor.extract()

            # Phase 2: Semantic Summaries (one-time process)
            api_key = os.getenv("OPENAI_API_KEY")
            semantic_extractor = SemanticExtractor(api_key)
            enriched_summary = semantic_extractor.summarize(repo_summary)

            # --- Replace manual loop with agent invocation ---
            readme_md, review_report = run_readme_agent(enriched_summary)


            # Initialize README generator and start refine-review loop
            # readme_gen = ReadmeGenerator()
            # readme_md = None
            # review_report = None
            # max_iterations = 3
            # current_iteration = 0

            # while current_iteration < max_iterations:
            #     print(f"\nStarting refine-review iteration {current_iteration + 1}/{max_iterations}")
        
            #     # Generate or refine README
            #     readme_md, review_report, quality_score = readme_gen.generate_readme_markdown(
            #         enriched_summary,
            #         local_path,
            #         previous_readme=readme_md,
            #         review_report=review_report
            #     )
            
            #     # Save the current version
            #     readme_path = os.path.join(local_path, f"README_v{current_iteration + 1}.md")
            #     with open(readme_path, "w", encoding="utf-8") as f:
            #         f.write(readme_md)
        
            #     print(f"README version {current_iteration + 1} generated at: {readme_path}")
        
            #     # Check if review report indicates sufficient qualitys
            #     if quality_score >= 0.9:
            #         print("README quality is sufficient. Ending refine-review loop.")
            #         break
            #     current_iteration += 1
            
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
