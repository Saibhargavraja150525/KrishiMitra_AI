import streamlit as st
from dotenv import load_dotenv

from database import init_db, save_interaction, get_recent_interactions
from services.advisor import get_farming_advice
from services.gnani import transcribe_audio, synthesize_telugu

load_dotenv()
init_db()

st.set_page_config(page_title="KrishiMitra AI", page_icon="🌾", layout="wide")

st.markdown("""
<style>
    .main {background-color: #f7fbf5;}
    .hero {
        background: linear-gradient(120deg, #14532d, #3f8f46);
        padding: 1.5rem 1.8rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1rem;
    }
    .hero h1 {color: white; margin-bottom: .2rem;}
    .small-note {color: #64748b; font-size: .9rem;}
    div.stButton > button {border-radius: 10px; min-height: 2.8rem;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <h1>🌾 KrishiMitra AI</h1>
  <p>Your language. Your farm. Your AI companion.</p>
  <p>తెలుగులో మాట్లాడండి — మీ వ్యవసాయ ప్రశ్నలకు సులభమైన సమాధానాలు పొందండి.</p>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("👨‍🌾 Farmer profile")
    farmer_name = st.text_input("Farmer name", value="Guest Farmer")
    village = st.text_input("Village / District", placeholder="e.g. Nalgonda")
    crop = st.selectbox(
        "Main crop",
        ["Cotton", "Paddy", "Maize", "Chilli", "Groundnut", "Other"]
    )
    st.caption("Your profile is stored locally in this demo.")
    st.divider()
    st.markdown("**Application status**")
    st.success("Demo mode is ready")
    st.caption("Gnani API calls activate after you add your API key to .env.")

st.subheader("Ask your farming question")
st.write("Type your question or record a short Telugu voice message.")

typed_question = st.text_area(
    "Your question",
    placeholder="ఉదాహరణ: నా పత్తి మొక్కల ఆకులు పసుపు రంగులోకి మారుతున్నాయి. నేను ఏమి చేయాలి?",
    height=110
)

audio_file = st.audio_input("🎙️ Record your question (up to the supported recording limit)")

col1, col2 = st.columns([1, 1])
with col1:
    ask_button = st.button("Get farming guidance", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("Clear question", use_container_width=True)

if clear_button:
    st.rerun()

question = typed_question.strip()

if ask_button:
    if audio_file is not None:
        try:
            with st.spinner("Transcribing your voice..."):
                transcript, source = transcribe_audio(audio_file)
            question = transcript.strip()
            st.info(f"Recognized speech ({source}): {question}")
        except Exception as exc:
            st.error(f"Voice transcription failed: {exc}")
            st.stop()

    if not question:
        st.warning("Please type a question or record a voice message first.")
    else:
        with st.spinner("Preparing farming guidance..."):
            answer, mode = get_farming_advice(question, crop=crop, village=village)

        st.session_state["last_answer"] = answer
        st.session_state["last_mode"] = mode
        st.session_state["last_question"] = question

        save_interaction(
            farmer_name=farmer_name,
            village=village,
            crop=crop,
            question=question,
            answer=answer,
            mode=mode
        )

if st.session_state.get("last_answer"):
    st.markdown("### 🌱 KrishiMitra's response")
    st.markdown(st.session_state["last_answer"])
    st.caption(f"Response mode: {st.session_state.get('last_mode', 'Demo')}")

    if st.button("🔊 Listen to this answer"):
        try:
            with st.spinner("Generating Telugu voice..."):
                audio_bytes, voice_source = synthesize_telugu(
                    st.session_state["last_answer"]
                )
            st.audio(audio_bytes, format="audio/wav")
            st.caption(f"Audio source: {voice_source}")
        except Exception as exc:
            st.error(f"Voice generation failed: {exc}")

st.divider()
st.subheader("🕘 Recent questions")

history = get_recent_interactions(limit=8)
if history:
    for item in history:
        with st.expander(f"{item['created_at']} · {item['crop']} · {item['question'][:65]}"):
            st.write("**Question:**", item["question"])
            st.write("**Answer:**", item["answer"])
            st.caption(f"Mode: {item['mode']} | Village: {item['village']}")
else:
    st.info("Your recent questions will appear here after your first interaction.")

st.divider()
st.caption(
    "KrishiMitra AI is an educational prototype. Crop symptoms can have multiple causes. "
    "Verify pesticide, fertilizer and treatment decisions with a qualified local agricultural officer or KVK."
)
