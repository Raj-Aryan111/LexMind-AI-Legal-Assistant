import streamlit as st
import pdfplumber
import io
import uuid

from sentence_transformers import SentenceTransformer

from qdrant_client import QdrantClient

from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

from openai import OpenAI


# ==================================================
# CONFIG
# ==================================================

st.set_page_config(

    page_title="LexMind",

    page_icon="⚖️",

    layout="wide"
)


# ==================================================
# OPENROUTER CLIENT
# ==================================================

client_llm = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=st.secrets["OPENROUTER_API_KEY"]
)


# ==================================================
# EMBEDDING MODEL
# ==================================================

@st.cache_resource
def load_model():

    return SentenceTransformer(

        "BAAI/bge-small-en-v1.5"
    )


embed_model = load_model()


# ==================================================
# QDRANT
# ==================================================

@st.cache_resource
def init_qdrant():

    client = QdrantClient(":memory:")


    client.recreate_collection(

        collection_name="case_files",

        vectors_config=VectorParams(

            size=384,

            distance=Distance.COSINE
        )
    )

    return client


qdrant = init_qdrant()


# ==================================================
# TITLE
# ==================================================

st.title("⚖️ LexMind")

st.caption(

    "AI Legal Research Assistant"
)


# ==================================================
# SESSION
# ==================================================

if "indexed" not in st.session_state:

    st.session_state.indexed = False


# ==================================================
# PDF UPLOAD
# ==================================================

uploaded_file = st.file_uploader(

    "Upload Case PDF",

    type=["pdf"]
)


# ==================================================
# INDEX PDF
# ==================================================

if uploaded_file:


    if st.button("Index Document"):


        with st.spinner(

            "Processing PDF..."
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


                        if len(para) < 20:

                            continue


                        chunks.append(

                            {

                                "text": para,

                                "page_num": page_num
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


            st.success(

                f"Indexed {len(points)} chunks"
            )


            st.session_state.indexed = True


# ==================================================
# CHAT
# ==================================================

if st.session_state.indexed:


    query = st.chat_input(

        "Ask legal question..."
    )


    if query:


        with st.chat_message("user"):

            st.write(query)


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


        prompt = f"""

You are a legal AI assistant.

Use ONLY retrieved evidence.

Question:
{query}

Retrieved Evidence:
{retrieved_text}

Provide:
1. Legal Summary
2. Relevant Sections
3. Case-document Insights
4. Short Explanation

"""


        response = client_llm.chat.completions.create(

            model="openai/gpt-3.5-turbo",

            messages=[

                {

                    "role": "user",

                    "content": prompt
                }
            ]
        )


        answer = response.choices[0].message.content


        with st.chat_message("assistant"):

            st.write(answer)


            st.markdown("## 📄 Retrieved Evidence")


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