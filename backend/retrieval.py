from sentence_transformers import (
    SentenceTransformer
)

from qdrant_client.models import (

    Filter,

    FieldCondition,

    MatchValue
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
# LEGAL STATUTE RETRIEVAL
# ==================================================

def retrieve_legal_context(

    query: str,

    top_k: int = 5
):


    # TEMP STATIC STATUTES

    return [

        {

            "section_number": "506",

            "act": "IPC",

            "text": "Punishment for criminal intimidation.",

            "similarity_score": 0.91
        },

        {

            "section_number": "452",

            "act": "IPC",

            "text": "House trespass after preparation for hurt or assault.",

            "similarity_score": 0.88
        },

        {

            "section_number": "324",

            "act": "IPC",

            "text": "Voluntarily causing hurt by dangerous weapons.",

            "similarity_score": 0.85
        }
    ]


# ==================================================
# CASE DOCUMENT RETRIEVAL
# ==================================================

def retrieve_case_context(

    query: str,

    lawyer_id: str,

    case_id: str,

    top_k: int = 3
):


    # ------------------------------------------
    # QUERY EMBEDDING
    # ------------------------------------------

    query_vector = embed_model.encode(

        query
    ).tolist()


    print("\n============================")
    print("QUERY")
    print("============================")

    print(query)


    print("\n============================")
    print("LAWYER ID")
    print("============================")

    print(lawyer_id)


    print("\n============================")
    print("CASE ID")
    print("============================")

    print(case_id)


    # ------------------------------------------
    # QDRANT SEARCH
    # ------------------------------------------

    results = client.query_points(

        collection_name="case_files",

        query=query_vector,

        limit=top_k,

        query_filter=Filter(

            must=[

                FieldCondition(

                    key="lawyer_id",

                    match=MatchValue(
                        value=lawyer_id
                    )
                ),

                FieldCondition(

                    key="case_id",

                    match=MatchValue(
                        value=case_id
                    )
                )
            ]
        )
    ).points


    print("\n============================")
    print("RAW RESULTS")
    print("============================")

    print(results)


    # ------------------------------------------
    # FORMAT RESULTS
    # ------------------------------------------

    retrieved = []


    for r in results:


        payload = r.payload or {}


        retrieved.append(

            {

                "text": payload.get(
                    "text",
                    ""
                ),

                "page_num": payload.get(
                    "page_num",
                    "?"
                ),

                "filename": payload.get(
                    "filename",
                    ""
                ),

                "score": getattr(
                    r,
                    "score",
                    0
                )
            }
        )


    print("\n============================")
    print("FINAL RETRIEVED")
    print("============================")

    print(retrieved)


    return retrieved