import os
import subprocess
import concurrent.futures
import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


question = st.text_area("Question", height=100)

col_a, col_b = st.columns(2)
with col_a:
    st.markdown("**Baseline Answer** (markdown supported)")
    baseline = st.text_area("Baseline Answer", height=350, label_visibility="collapsed")

with col_b:
    st.markdown("**Experiment Answer** (markdown supported)")
    experiment = st.text_area("Experiment Answer", height=350, label_visibility="collapsed")

def build_prompt(question, baseline, experiment):
    return (
        f"Which one of these answers is a better answer to the question and why?\n\n"
        f"Ignore the grounding and citations when evaluating which one is better. "
        f"The answers may contain markdown formatting — consider the quality and clarity of the formatting as part of your evaluation.\n\n"
        f"Question: {question}\n\n"
        f"Answer A (Baseline):\n{baseline}\n\n"
        f"Answer B (Experiment):\n{experiment}"
    )

if st.button("Evaluate"):
    if not question.strip() or not baseline.strip() or not experiment.strip():
        st.warning("Please fill in all fields.")
    else:
        prompt = build_prompt(question, baseline, experiment)

        gemini_key = os.getenv("GEMINI_API_KEY") or st.secrets.get("GEMINI_API_KEY", "")
        openai_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", "")

        def run_gemini():
            if not gemini_key:
                return None, "GEMINI_API_KEY not set in secrets."
            try:
                genai.configure(api_key=gemini_key)
                model = genai.GenerativeModel("gemini-3.1-pro-preview")
                response = model.generate_content(prompt)
                return response.text, None
            except Exception as e:
                return None, f"Gemini error: {e}"

        def run_openai():
            if not openai_key:
                return None, "OPENAI_API_KEY not set in secrets."
            try:
                client = OpenAI(api_key=openai_key)
                response = client.chat.completions.create(
                    model="gpt-5.4",
                    messages=[{"role": "user", "content": prompt}],
                )
                return response.choices[0].message.content, None
            except Exception as e:
                return None, f"GPT-4o error: {e}"

        def run_claude():
            try:
                result = subprocess.run(
                    ["claude", "-p", "--model", "us.anthropic.claude-sonnet-4-6", "--bare", prompt],
                    capture_output=True, text=True, timeout=120,
                )
                if result.returncode != 0:
                    return None, f"Claude error (rc={result.returncode}):\nstdout: {result.stdout.strip()}\nstderr: {result.stderr.strip()}"
                return result.stdout.strip(), None
            except Exception as e:
                return None, f"Claude error: {type(e).__name__}: {e}"

        col1, col2, col3 = st.columns(3)

        with st.spinner("Running evaluations..."):
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future_gemini = executor.submit(run_gemini)
                future_openai = executor.submit(run_openai)
                future_claude = executor.submit(run_claude)
                gemini_result, gemini_error = future_gemini.result()
                openai_result, openai_error = future_openai.result()
                claude_result, claude_error = future_claude.result()

        with col1:
            st.subheader("Gemini 3.1 pro")
            if gemini_error:
                st.error(gemini_error)
            else:
                st.markdown(gemini_result)

        with col2:
            st.subheader("GPT-5.4")
            if openai_error:
                st.error(openai_error)
            else:
                st.markdown(openai_result)

        with col3:
            st.subheader("Sonnet 4.6")
            if claude_error:
                st.error(claude_error)
            else:
                st.markdown(claude_result)
