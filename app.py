# app.py

import streamlit as st
import logging
from main_agent import MedicalAgent

# ------------------ Logging Setup ------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/medical_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ------------------ Page Config ------------------
st.set_page_config(
    page_title="AI Healthcare Agent",
    page_icon="🧠",
    layout="wide"
)

# ------------------ Session State ------------------
if "agent" not in st.session_state:
    try:
        st.session_state.agent = MedicalAgent()
        logger.info("MedicalAgent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        st.error(f"🔴 System initialization failed: {e}")
        st.error("Please ensure vector store is created (run ingest_pdfs.py) and API key is configured.")
        st.stop()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Sidebar ------------------
with st.sidebar:
    st.title("⚙️ Settings")
    user_type = st.radio(
        "Patient Profile",
        ["Adult", "Infant"],
        help="Infant mode enables pediatric emergency rules"
    )

    st.divider()
    st.subheader("🕘 Conversation History")

    if st.session_state.chat_history:
        for i, item in enumerate(st.session_state.chat_history):
            with st.expander(f"Query {i+1}"):
                st.write(item["user"])
                st.write(f"Risk: {item['risk']}")
    else:
        st.info("No history yet.")

    if st.button("🗑 Clear History"):
        st.session_state.chat_history.clear()
        st.rerun()

# ------------------ Main UI ------------------
st.title("🧠 AI Healthcare Assistant")
st.caption(
    "⚠️ This system provides general medical information only "
    "and does NOT replace professional medical advice."
)

user_input = st.text_area(
    "Describe your symptoms",
    height=140,
    placeholder="Example: Severe headache, fever, nausea..."
)

analyze_btn = st.button("🔍 Analyze", type="primary")

# ------------------ Processing ------------------
if analyze_btn:
    if not user_input.strip():
        st.warning("Please enter your symptoms.")
    else:
        with st.spinner("Analyzing symptoms safely..."):
            try:
                result = st.session_state.agent.process_query(
                    user_input=user_input,
                    user_type=user_type
                )
            except ValueError as e:
                st.error(f"❌ Invalid input: {e}")
                logger.warning(f"Validation error: {e}")
                st.stop()
            except Exception as e:
                st.error(f"❌ Processing error: {e}")
                logger.error(f"Query processing failed: {e}", exc_info=True)
                st.error("Please try again or contact support if the issue persists.")
                st.stop()

        # ---------- Emergency ----------
        if result["emergency"]:
            st.error("🚨 EMERGENCY DETECTED")
            st.error(result["message"])
            st.stop()

        # ---------- Save History ----------
        st.session_state.chat_history.append({
            "user": user_input,
            "risk": result["risk"].get("risk_level", "Unknown")
        })

        # ---------- Results Tabs ----------
        tab1, tab2, tab3 = st.tabs(
            ["🩺 Assessment", "📄 Doctor Report", "🧪 Raw Data"]
        )

        with tab1:
            st.subheader("Risk Assessment")

            risk_score = result["risk"].get("score", 0) * 100
            st.metric("Risk Level", result["risk"].get("risk_level", "Unknown"))
            st.progress(min(int(risk_score), 100))

            st.divider()
            st.subheader("Medical Guidance")
            st.markdown(result["response"])

        with tab2:
            st.subheader("Doctor-Friendly Report")
            st.text_area(
                "Generated Report",
                result["report"],
                height=400
            )
            st.download_button(
                "📥 Download Report",
                data=result["report"],
                file_name="medical_report.txt"
            )

        with tab3:
            st.subheader("Extracted Data")
            st.json(result["symptoms"])
            st.json(result["risk"])