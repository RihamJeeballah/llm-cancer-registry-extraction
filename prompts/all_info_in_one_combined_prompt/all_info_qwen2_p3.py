import streamlit as st
import pandas as pd
import ollama
import os
import json

# Restrict to GPU 0
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


# --------------------------
# LLM CALL FUNCTION
# --------------------------
def generate_response(model, prompt, report, json_template):

    # Convert strict JSON template to string without indentation
    template_str = json.dumps(json_template)

    input_text = (
        f"{prompt}\n\n"
        f"Pathology Report:\n{report}\n\n"
        f"Return ONLY valid JSON. No explanation. No additional text.\n"
        f"Use this exact JSON format:\n{template_str}"
    )

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": input_text}],
        options={"temperature": 0, "max_tokens": 200}
    )

    return response.get("message", {}).get("content", "")


# --------------------------
# STREAMLIT UI
# --------------------------
st.title("Unified LLM Pathology Extractor – Anticipatory Prompt (P3)")

# STRICT JSON ENFORCEMENT (TNM STYLE)
json_template = {
    "Grade": "",
    "Morphology": "",
    "T": "",
    "N": "",
    "M": "",
    "Laterality": ""
}

input_option = st.radio("Select Input Method:", ("Manual Input", "Upload CSV"))

model_name = "qwen2:latest"


# --------------------------
# MANUAL INPUT WORKFLOW
# --------------------------
if input_option == "Manual Input":
    prompt = st.text_area("Enter the combined anticipatory prompt:")
    report = st.text_area("Enter pathology report text:")

    if st.button("Generate Response"):
        if prompt and report:
            response = generate_response(model_name, prompt, report, json_template)
            st.write("### Extracted Output (Raw JSON):")
            st.code(response)
        else:
            st.warning("Please enter both prompt and report.")


# --------------------------
# CSV WORKFLOW
# --------------------------
elif input_option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV (must contain 'text' column)", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if "text" not in df.columns:
            st.error("CSV must contain a 'text' column.")
        else:
            prompt = st.text_area("Enter the combined anticipatory prompt:")

            if st.button("Process CSV"):

                df["response"] = df["text"].apply(
                    lambda r: generate_response(model_name, prompt, r, json_template)
                )

                st.write("### Processed Data:")
                st.dataframe(df)

                # Create minimal response dataframe
                response_df = pd.DataFrame({
                    "prompt_type": ["Anticipatory-P3-Combined"] * len(df),
                    "response": df["response"]
                })

                # JSON download
                json_data = response_df.to_json(orient="records", indent=2)
                st.download_button(
                    "Download JSON Output",
                    json_data,
                    "combined_p3_qwen2_extractions.json",
                    "application/json"
                )

                # CSV download
                st.download_button(
                    "Download CSV Output",
                    response_df.to_csv(index=False),
                    "combined_p3_qwen2_extractions.csv",
                    "text/csv"
                )
