import streamlit as st
from groq import Groq

st.set_page_config(page_title="Smart Message Composer", page_icon="✉️", layout="centered")

st.title("✉️ Smart Message Composer")
st.caption("Generate context-aware professional messages using the Groq API")

with st.sidebar:
    st.header("🔑 API Configuration")
    api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get your free key from https://console.groq.com/keys",
    )
    model = st.selectbox(
        "Model",
        ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it"],
    )

st.subheader("📝 Message Details")

raw_input = st.text_area(
    "What do you want to say? (rough draft or key points)", height=150
)

col1, col2 = st.columns(2)
with col1:
    tone = st.selectbox(
        "Tone",
        ["Formal", "Friendly", "Assertive", "Diplomatic", "Neutral", "Persuasive", "Empathetic"],
    )
    management_level = st.selectbox(
        "Management Level",
        ["Individual Contributor", "Team Lead", "Manager", "Director", "VP/C-Level"],
    )
    audience = st.selectbox(
        "Audience",
        ["Direct Report", "Peer", "Manager/Boss", "Senior Leadership", "Client/External", "Cross-functional Team"],
    )

with col2:
    context = st.selectbox(
        "Context",
        ["Email", "Slack/Chat Message", "Performance Review", "Project Update", "Meeting Follow-up", "Escalation", "Announcement"],
    )
    criticality = st.selectbox("Criticality", ["Low", "Medium", "High", "Urgent/Crisis"])

extra_notes = st.text_area("Additional notes (optional)", height=80)

generate = st.button("🚀 Generate Message", type="primary", use_container_width=True)


def build_prompt() -> str:
    return f"""You are an expert corporate communication assistant. Compose a polished message based on the following parameters.

Raw input / key points: {raw_input}

Tone: {tone}
Management Level of Sender: {management_level}
Audience: {audience}
Context/Medium: {context}
Criticality: {criticality}
Additional notes: {extra_notes if extra_notes else "None"}

Instructions:
- Craft a ready-to-send message appropriate for the given context/medium.
- Match the specified tone precisely.
- Adjust vocabulary, formality and structure for the management level and audience.
- Reflect the criticality level in urgency, framing, and any calls to action.
- Keep it concise and professional unless the context calls for more detail.
- Output ONLY the final message, with no preamble, labels, or explanation.
"""


if generate:
    if not api_key:
        st.error("Please enter your Groq API key in the sidebar.")
    elif not raw_input.strip():
        st.error("Please enter some input text or key points.")
    else:
        try:
            client = Groq(api_key=api_key)
            with st.spinner("Generating your message..."):
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": build_prompt()}],
                    temperature=0.7,
                    max_tokens=1024,
                )
            result = response.choices[0].message.content
            st.subheader("✅ Generated Message")
            st.text_area("Output", value=result, height=300)
            st.download_button("📥 Download as .txt", result, file_name="generated_message.txt")
        except Exception as e:
            st.error(f"Error generating message: {e}")

st.markdown("---")
st.caption("Powered by Groq API & Streamlit")
