# =========================================================
# LEXMIND — FINAL PROFESSIONAL STREAMLIT APP
# =========================================================
import os

os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"

import streamlit as st
import pdfplumber
import io
import uuid
import numpy as np

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from openai import OpenAI


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="LexMind — AI Legal Assistant",

    page_icon="⚖️",

    layout="wide",

    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""

<style>

.block-container {

    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1400px;
}

.stChatMessage {

    padding: 1rem;
    border-radius: 14px;
}

[data-testid="stSidebar"] {

    background-color: #111827;
}

.main {

    background-color: #0B1120;
}

</style>

""", unsafe_allow_html=True)


# =========================================================
# OPENROUTER CLIENT
# =========================================================

client_llm = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=st.secrets["OPENROUTER_API_KEY"]
)


# =========================================================
# EMBEDDING MODEL
# =========================================================

@st.cache_resource
def load_embedding_model():

    return SentenceTransformer(

        "BAAI/bge-small-en-v1.5"
    )


embed_model = load_embedding_model()


# =========================================================
# QDRANT
# =========================================================

@st.cache_resource
def init_qdrant():

    client = QdrantClient(":memory:")


    collections = client.get_collections().collections

    collection_names = [c.name for c in collections]


    if "case_files" not in collection_names:


        client.create_collection(

            collection_name="case_files",

            vectors_config=VectorParams(

                size=384,

                distance=Distance.COSINE
            )
        )


    return client


qdrant = init_qdrant()


# =========================================================
# MOCK STATUTES
# =========================================================

STATUTES = [

    {
        "section": "506 IPC",
        "text": "Punishment for criminal intimidation."
    },

    {
        "section": "452 IPC",
        "text": "House trespass after preparation for hurt or assault."
    },

    {
        "section": "324 IPC",
        "text": "Voluntarily causing hurt by dangerous weapons."
    },

    {
        "section": "447 IPC",
        "text": "Punishment for criminal trespass."
    },

    {
        "section": "503 IPC",
        "text": "Criminal intimidation definition."
    }
]


# =========================================================
# SESSION STATE
# =========================================================

if "indexed" not in st.session_state:

    st.session_state.indexed = False


if "messages" not in st.session_state:

    st.session_state.messages = []


if "case_name" not in st.session_state:

    st.session_state.case_name = None


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:


    st.title("⚖️ LexMind")

    st.caption(

        "AI Legal Research Platform"
    )


    st.markdown("---")


    st.subheader("👨‍⚖️ Lawyer Workspace")


    lawyer_id = st.text_input(

        "Lawyer ID",

        value="lawyer_001"
    )


    st.success(

        f"Logged in as: {lawyer_id}"
    )


    st.markdown("---")


    st.subheader("📁 Case Upload")


    case_name = st.text_input(

        "Case ID",

        placeholder="state_vs_rajan"
    )


    uploaded_file = st.file_uploader(

        "Upload Case PDF",

        type=["pdf"]
    )


    # =====================================================
    # INDEXING
    # =====================================================

    if uploaded_file and case_name:


        if st.button(

            "Index Document",

            type="primary"
        ):


            with st.status(

                "Analyzing legal document..."
            ):


                pdf_bytes = uploaded_file.read()


                chunks = []


                with pdfplumber.open(

                    io.BytesIO(pdf_bytes)
                ) as pdf:


                    for page_num, page in enumerate(

                        pdf.pages,

                        start=1
                    ):


                        text = page.extract_text()


                        if not text:

                            continue


                        paragraphs = text.split("\n\n")


                        for para in paragraphs:


                            para = para.strip()


                            if len(para) < 30:

                                continue


                            chunks.append(

                                {

                                    "text": para,

                                    "page_num": page_num,

                                    "case_id": case_name,

                                    "lawyer_id": lawyer_id
                                }
                            )


                texts = [

                    c["text"]

                    for c in chunks
                ]


                vectors = embed_model.encode(

                    texts
                )


                points = []


                for chunk, vector in zip(

                    chunks,

                    vectors
                ):


                    points.append(

                        PointStruct(

                            id=str(uuid.uuid4()),

                            vector=vector.tolist(),

                            payload=chunk
                        )
                    )


                qdrant.upsert(

                    collection_name="case_files",

                    points=points
                )


                st.session_state.indexed = True

                st.session_state.case_name = case_name


                st.success(

                    f"Indexed {len(points)} chunks"
                )


# =========================================================
# MAIN HEADER
# =========================================================

st.markdown("""

# ⚖️ LexMind

### AI Legal Research & Case Analysis Platform

""")



# =========================================================
# ACTIVE CASE
# =========================================================

if st.session_state.case_name:


    st.success(

        f"Active Case: {st.session_state.case_name}"
    )


# =========================================================
# CHAT HISTORY
# =========================================================

for msg in st.session_state.messages:


    with st.chat_message(msg["role"]):


        st.write(msg["content"])


# =========================================================
# CHAT INPUT
# =========================================================

if st.session_state.indexed:


    query = st.chat_input(

        "Ask legal question..."
    )


    if query:


        # =================================================
        # USER MESSAGE
        # =================================================

        st.session_state.messages.append(

            {

                "role": "user",

                "content": query
            }
        )


        with st.chat_message("user"):

            st.write(query)


        # =================================================
        # RETRIEVAL
        # =================================================

        query_vector = embed_model.encode(

            query
        ).tolist()


        results = qdrant.query_points(

            collection_name="case_files",

            query=query_vector,

            limit=3
        ).points


        retrieved_text = "\n\n".join(

            [

                r.payload["text"]

                for r in results
            ]
        )


        # =================================================
        # STATUTE MATCHING
        # =================================================

        matched_sections = []


        lower_query = query.lower()


        if (

            "threat" in lower_query

            or "intimidation" in lower_query
        ):

            matched_sections.append(STATUTES[0])


        if (

            "house" in lower_query

            or "trespass" in lower_query

            or "entered" in lower_query
        ):

            matched_sections.append(STATUTES[1])


        if (

            "knife" in lower_query

            or "weapon" in lower_query

            or "hurt" in lower_query
        ):

            matched_sections.append(STATUTES[2])


        if len(matched_sections) == 0:

            matched_sections = STATUTES[:3]


        statute_text = "\n".join(

            [

                f"{s['section']} : {s['text']}"

                for s in matched_sections
            ]
        )


        # =================================================
        # PROMPT
        # =================================================

        prompt = f"""

You are an expert Indian legal AI assistant.

STRICT RULES:
- Use ONLY retrieved evidence.
- Do NOT invent facts.
- Do NOT assume forensic matches unless stated.
- Keep answers professional.

Question:
{query}

Relevant Statutes:
{statute_text}

Retrieved Evidence:
{retrieved_text}

Generate response in this format:

1. Legal Summary
2. Relevant Sections
3. Case-document Insights
4. Short Explanation

"""


        # =================================================
        # LLM CALL
        # =================================================

        with st.chat_message("assistant"):


            with st.status(

                "Analyzing legal evidence..."
            ):


                response = client_llm.chat.completions.create(

                    model="openai/gpt-3.5-turbo",

                    messages=[

                        {

                            "role": "user",

                            "content": prompt
                        }
                    ]
                )


                answer = (

                    response

                    .choices[0]

                    .message

                    .content
                )


                # =========================================
                # MAIN RESPONSE
                # =========================================

                with st.container(border=True):


                    st.write(answer)


                # =========================================
                # CONFIDENCE
                # =========================================

                st.markdown("## Confidence")


                scores = [

                    r.score

                    for r in results
                ]


                confidence = float(

                    np.mean(scores)
                )


                confidence = min(

                    confidence,

                    0.99
                )


                st.progress(confidence)


                st.caption(

                    f"🟢 {round(confidence * 100)}%"
                )


                # =========================================
                # STATUTES
                # =========================================

                st.markdown(

                    "## 📚 Statute Citations"
                )


                for s in matched_sections:


                    with st.container(border=True):


                        st.markdown(

                            f"""
### {s['section']}

{s['text']}
"""
                        )


                # =========================================
                # EVIDENCE
                # =========================================

                st.markdown(

                    "## 📄 Retrieved Evidence"
                )


                for r in results:


                    with st.expander(

                        f"Page {r.payload['page_num']}"
                    ):


                        st.write(

                            r.payload["text"]
                        )


                        st.caption(

                            f"Similarity Score: "
                            f"{round(r.score, 3)}"
                        )


                # =========================================
                # SAVE CHAT
                # =========================================

                st.session_state.messages.append(

                    {

                        "role": "assistant",

                        "content": answer
                    }
                )


else:


    st.info(

        "Upload and index a legal PDF to begin."
    )