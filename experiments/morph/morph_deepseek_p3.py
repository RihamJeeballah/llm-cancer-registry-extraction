import streamlit as st
import pandas as pd
import ollama

def generate_response(model, prompt, report, json_template):
    json_template_str = str(json_template)
    input_text = (
        f"{prompt}\n\n"
        f"Pathology Report:\n{report}\n\n"
        f"Here is the JSON template to be filled in:\n{json_template_str}\n"
    )
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": input_text}],
        options={"temperature": 0, "max_tokens": 100}
    )
    return response.get("message", {}).get("content", "")

st.title("LLM Pathology Report Processor")

# Model selection
#model = st.selectbox("Choose Model:", ["llama3.3 ", "deepseek-r1:70b"])

# User input or file upload
input_option = st.radio("Select Input Method:", ("Manual Input", "Upload CSV"))
json_template = {'Morphology': ""}

if input_option == "Manual Input":
    prompt = st.text_area("Enter your prompt:")
    report = st.text_area("Enter pathology report:")
    if st.button("Generate Response"):
        if prompt and report:
            response = generate_response("deepseek-r1:70b", prompt, report, json_template)
            st.write("### Response:")
            st.write(response)
        else:
            st.warning("Please enter both a prompt and a pathology report.")
elif input_option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if "text" in df.columns:
            prompt = st.text_area("Enter your prompt:")
            if st.button("Process CSV"):
                df["response"] = df["text"].apply(lambda report: generate_response("deepseek-r1:70b", prompt, report, json_template))
                st.write("### Processed Responses:")
                st.dataframe(df)
                
                # Create a separate DataFrame with prompt_type and response
                response_df = pd.DataFrame({
                    "prompt_type": ["Anticipatory"] * len(df),
                    "response": df["response"]
                })
                
                # Provide download button for the response as JSON file
                json_data = response_df.to_json(orient="records", indent=2)
                st.download_button("Download JSON", json_data, "morph_responses_deepseek_p3.json", "application/json")
                
                # Provide download button for the response as CSV file
                st.download_button("Download CSV", response_df.to_csv(index=False), "morph_responses_deepseek_p3.csv", "text/csv")
        else:
            st.error("CSV must contain a 'text' column.")