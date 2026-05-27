# ==================================================
# FINAL POLISHED frontend/app.py
# ==================================================

import streamlit as st
import requests

from streamlit_pdf_viewer import pdf_viewer


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(

    page_title="LexMind — AI Legal Assistant",

    page_icon="⚖️",

    layout="wide",

    initial_sidebar_state="expanded"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""

<style>

.block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.stChatMessage {

    padding: 1rem;
    border-radius: 12px;
}

</style>

""", unsafe_allow_html=True)


# ==================================================
# API URL
# ==================================================

API_URL = "http://127.0.0.1:8000"


# ==================================================
# SESSION STATE
# ==================================================

if "session_id" not in st.session_state:

    st.session_state.session_id = None


if "lawyer_id" not in st.session_state:

    st.session_state.lawyer_id = None


if "messages" not in st.session_state:

    st.session_state.messages = []


if "selected_case" not in st.session_state:

    st.session_state.selected_case = None


if "uploaded_pdf_bytes" not in st.session_state:

    st.session_state.uploaded_pdf_bytes = None


# ==================================================
# CITATION RENDERER
# ==================================================

def render_citations(legal_resp):


    confidence = legal_resp.get(

        "confidence_score",

        0.0
    )


    # ------------------------------------------
    # CONFIDENCE
    # ------------------------------------------

    st.markdown("### Confidence")

    st.progress(confidence)


    st.caption(

        f"{round(confidence * 100)}%"
    )


    # ------------------------------------------
    # CAVEAT
    # ------------------------------------------

    if legal_resp.get("caveat"):


        st.warning(

            legal_resp["caveat"]
        )


    # ------------------------------------------
    # STATUTES
    # ------------------------------------------

    statutes = legal_resp.get(

        "cited_statutes",

        []
    )


    if statutes:


        st.markdown("## 📚 Relevant Legal Sections")


        for s in statutes:


            with st.container(border=True):


                st.markdown(

                    f"""
### IPC/BNS Section {s.get('section_number')}

**Act:** {s.get('act')}

{s.get('text')}
"""
                )


                st.caption(

                    f"Similarity Score: "
                    f"{round(s.get('similarity_score', 0), 3)}"
                )


    # ------------------------------------------
    # EVIDENCE
    # ------------------------------------------

    evidence_chunks = legal_resp.get(

        "retrieved_case_chunks",

        []
    )


    if evidence_chunks:


        st.markdown("## 📄 Retrieved Evidence")


        for chunk in evidence_chunks:


            with st.expander(

                f"Evidence — Page {chunk.get('page_num', '?')}"
            ):


                st.write(

                    chunk.get(
                        "text",
                        ""
                    )
                )


                st.caption(

                    f"Similarity Score: "
                    f"{round(chunk.get('score', 0), 3)}"
                )


# ==================================================
# SIDEBAR
# ==================================================

with st.sidebar:


    st.title("⚖️ LexMind")

    st.caption(

        "AI Legal Research Platform"
    )


    st.sidebar.header(

        "Case Workspace"
    )


    # ------------------------------------------
    # LOGIN
    # ------------------------------------------

    if not st.session_state.session_id:


        lawyer_id = st.text_input(

            "Lawyer ID",

            value="lawyer_001"
        )


        if st.button(

            "Start Session",

            type="primary"
        ):


            response = requests.post(

                f"{API_URL}/session/start",

                json={

                    "lawyer_id":

                    lawyer_id
                }
            )


            data = response.json()


            st.session_state.session_id = (

                data["session_id"]
            )


            st.session_state.lawyer_id = (

                lawyer_id
            )


            st.rerun()


    else:


        st.success(

            f"Logged in as "
            f"{st.session_state.lawyer_id}"
        )


        if st.button("Reset Session"):


            st.session_state.messages = []

            st.session_state.session_id = None

            st.session_state.selected_case = None

            st.session_state.uploaded_pdf_bytes = None


            st.rerun()


    # ------------------------------------------
    # CASES
    # ------------------------------------------

    st.markdown("---")

    st.subheader("📁 Cases")


    if st.session_state.lawyer_id:


        try:


            response = requests.get(

                f"{API_URL}/cases",

                params={

                    "lawyer_id":

                    st.session_state.lawyer_id
                }
            )


            cases = response.json().get(

                "cases",

                []
            )


            for case in cases:


                if st.button(

                    f"📄 {case}",

                    key=case
                ):


                    st.session_state.selected_case = case


        except:


            st.warning(

                "Backend unavailable"
            )


    # ------------------------------------------
    # FILE UPLOAD
    # ------------------------------------------

    st.markdown("---")

    st.subheader("📤 Upload Case")


    new_case_id = st.text_input(

        "Case ID",

        placeholder="state_vs_rajan"
    )


    uploaded_file = st.file_uploader(

        "Upload PDF",

        type=["pdf"]
    )


    if uploaded_file and new_case_id:


        if st.button(

            "Index Document"
        ):


            with st.status(

                "Analyzing legal document..."
            ):


                response = requests.post(

                    f"{API_URL}/cases/{new_case_id}/upload",

                    params={

                        "lawyer_id":

                        st.session_state.lawyer_id
                    },

                    files={

                        "file": (

                            uploaded_file.name,

                            uploaded_file.getvalue(),

                            "application/pdf"
                        )
                    }
                )


                if response.status_code == 200:


                    st.success(

                        "Document indexed successfully!"
                    )


                    st.session_state.selected_case = (

                        new_case_id
                    )


                    st.session_state.uploaded_pdf_bytes = (

                        uploaded_file.getvalue()
                    )


                else:


                    st.error(

                        response.text
                    )


# ==================================================
# MAIN HEADER
# ==================================================

st.markdown("""

# ⚖️ LexMind

### AI Legal Research & Case Analysis Platform

""")



# ==================================================
# ACTIVE CASE
# ==================================================

if st.session_state.selected_case:


    st.success(

        f"Active Case: "
        f"{st.session_state.selected_case}"
    )


# ==================================================
# PDF VIEWER
# ==================================================

if st.session_state.uploaded_pdf_bytes:


    st.markdown("## 📄 Case Document")


    pdf_viewer(

        st.session_state.uploaded_pdf_bytes,

        width=1000
    )


# ==================================================
# CHAT HISTORY
# ==================================================

for msg in st.session_state.messages:


    with st.chat_message(

        msg["role"]
    ):


        st.write(

            msg["content"]
        )


        if msg.get("legal_response"):


            render_citations(

                msg["legal_response"]
            )


        st.markdown("<br>", unsafe_allow_html=True)


# ==================================================
# CHAT INPUT
# ==================================================

prompt = st.chat_input(

    "Ask a legal question..."
)


if prompt:


    # ------------------------------------------
    # USER
    # ------------------------------------------

    st.session_state.messages.append(

        {

            "role": "user",

            "content": prompt
        }
    )


    with st.chat_message("user"):


        st.write(prompt)


    # ------------------------------------------
    # ASSISTANT
    # ------------------------------------------

    with st.chat_message("assistant"):


        with st.status(

            "Researching legal evidence..."
        ):


            response = requests.post(

                f"{API_URL}/query",

                json={

                    "session_id":

                    st.session_state.session_id,

                    "query":

                    prompt,

                    "lawyer_id":

                    st.session_state.lawyer_id,

                    "case_id":

                    st.session_state.selected_case
                }
            )


            if response.status_code == 200:


                legal_resp = (

                    response.json()["response"]
                )


                summary = legal_resp.get(

                    "summary",

                    "No response."
                )


                with st.container(border=True):


                    st.write(summary)


                render_citations(

                    legal_resp
                )


                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": summary,

                        "legal_response":

                        legal_resp
                    }
                )


            else:


                st.error(

                    response.text
                )