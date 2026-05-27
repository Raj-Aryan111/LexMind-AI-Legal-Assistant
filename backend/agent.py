import os

from dotenv import load_dotenv

from openai import OpenAI

from backend.retrieval import (

    retrieve_legal_context,

    retrieve_case_context
)


# ==================================================
# LOAD ENV VARIABLES
# ==================================================

load_dotenv()


# ==================================================
# OPENROUTER CLIENT
# ==================================================

client = OpenAI(

    api_key=os.getenv("OPENROUTER_API_KEY"),

    base_url="https://openrouter.ai/api/v1"
)


# ==================================================
# MAIN QUERY FUNCTION
# ==================================================

def run_structured_query(

    query: str,

    lawyer_id: str,

    case_id: str
):


    # ------------------------------------------
    # RETRIEVE STATUTES
    # ------------------------------------------

    statutes = retrieve_legal_context(

        query=query,

        top_k=5
    )


    print("\nSTATUTE RETRIEVAL RESULTS:\n")


    for s in statutes:

        print(s)


    # ------------------------------------------
    # RETRIEVE CASE CONTEXT
    # ------------------------------------------

    case_docs = retrieve_case_context(

        query=query,

        lawyer_id=lawyer_id,

        case_id=case_id,

        top_k=3
    )


    print("\nCASE RETRIEVAL RESULTS:\n")


    for c in case_docs:

        print(c)


    # ------------------------------------------
    # FORMAT STATUTES
    # ------------------------------------------

    statute_text = ""


    for s in statutes:


        statute_text += (

            f"\nSection {s['section_number']} "

            f"{s['act']}:\n"

            f"{s['text']}\n"
        )


    # ------------------------------------------
    # FORMAT CASE DOCUMENTS
    # ------------------------------------------

    case_text = ""


    for c in case_docs:


        case_text += (

            f"\nPage {c['page_num']}:\n"

            f"{c['text']}\n"
        )


    # ------------------------------------------
    # PROMPT
    # ------------------------------------------

    prompt = f"""

You are LexMind,
an expert Indian legal research assistant.

Answer ONLY using:
1. Retrieved statutes
2. Retrieved case evidence

If information is unavailable,
say:
"Information not available in retrieved evidence."

USER QUERY:
{query}

RETRIEVED STATUTES:
{statute_text}

RETRIEVED CASE EVIDENCE:
{case_text}

Provide:

1. Legal Summary
2. Relevant Sections
3. Case-document Insights
4. Short Explanation
"""


    # ------------------------------------------
    # OPENROUTER CALL
    # ------------------------------------------

    completion = client.chat.completions.create(

        model="openai/gpt-4.1-mini",

        messages=[

            {

                "role": "user",

                "content": prompt
            }
        ],

        max_tokens=700,

        temperature=0.2
    )


    summary = (

        completion
        .choices[0]
        .message
        .content
    )


    # ------------------------------------------
    # FINAL RESPONSE
    # ------------------------------------------

    return {

        "summary": summary,

        "confidence_score": 0.95,

        "cited_statutes": statutes,

        "retrieved_case_chunks": case_docs,

        "caveat": None
    }