import io
import uuid

import pdfplumber

from sentence_transformers import (
    SentenceTransformer
)

from qdrant_client.models import (

    PointStruct
)

from backend.qdrant_store import (
    client
)


# ==================================================
# EMBEDDING MODEL
# ==================================================

embed_model = SentenceTransformer(

    "BAAI/bge-small-en-v1.5"
)


# ==================================================
# INDEX PDF
# ==================================================

def index_pdf(

    file_bytes: bytes,

    lawyer_id: str,

    case_id: str,

    filename: str
):


    print("\n============================")
    print("INDEXING STARTED")
    print("============================")


    # ------------------------------------------
    # EXTRACT PDF TEXT
    # ------------------------------------------

    chunks = []


    with pdfplumber.open(

        io.BytesIO(file_bytes)
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

                        "page_num": page_num,

                        "filename": filename,

                        "lawyer_id": lawyer_id,

                        "case_id": case_id
                    }
                )


    print(f"\nEXTRACTED CHUNKS: {len(chunks)}")


    # ------------------------------------------
    # CREATE EMBEDDINGS
    # ------------------------------------------

    texts = [

        c["text"]

        for c in chunks
    ]


    vectors = embed_model.encode(

        texts
    )


    # ------------------------------------------
    # CREATE POINTS
    # ------------------------------------------

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


    # ------------------------------------------
    # STORE IN QDRANT
    # ------------------------------------------

    client.upsert(

        collection_name="case_files",

        points=points
    )


    print("\n============================")
    print("FIRST STORED PAYLOAD")
    print("============================")

    print(points[0].payload)


    print(f"\nSTORED {len(points)} POINTS")


    return {

        "status": "success",

        "chunks_indexed": len(points)
    }