from fastapi import (

    FastAPI,

    UploadFile,

    File
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from pydantic import BaseModel

from backend.agent import (
    run_structured_query
)

from backend.indexing import (
    index_pdf
)


# ==================================================
# FASTAPI APP
# ==================================================

app = FastAPI(

    title="LexMind API",

    version="1.0"
)


# ==================================================
# CORS
# ==================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==================================================
# REQUEST MODELS
# ==================================================

class SessionStartRequest(

    BaseModel
):

    lawyer_id: str


class QueryRequest(

    BaseModel
):

    session_id: str

    query: str

    lawyer_id: str

    case_id: str


# ==================================================
# ROOT
# ==================================================

@app.get("/")
async def root():

    return {

        "message": "LexMind Backend Running"
    }


# ==================================================
# START SESSION
# ==================================================

@app.post("/session/start")
async def start_session(

    req: SessionStartRequest
):


    session_id = (

        f"{req.lawyer_id}_session"
    )


    return {

        "session_id": session_id,

        "lawyer_id": req.lawyer_id
    }


# ==================================================
# QUERY ENDPOINT
# ==================================================

@app.post("/query")
async def query_endpoint(

    req: QueryRequest
):


    response = run_structured_query(

        query=req.query,

        lawyer_id=req.lawyer_id,

        case_id=req.case_id
    )


    return {

        "session_id":

        req.session_id,

        "response":

        response
    }


# ==================================================
# LIST CASES
# ==================================================

@app.get("/cases")
async def list_cases(

    lawyer_id: str
):


    return {

        "cases": [

            "state_vs_rajan"
        ]
    }


# ==================================================
# PDF UPLOAD
# ==================================================

@app.post("/cases/{case_id}/upload")
async def upload_case_file(

    case_id: str,

    lawyer_id: str,

    file: UploadFile = File(...)
):


    try:


        contents = await file.read()


        result = index_pdf(

            file_bytes=contents,

            lawyer_id=lawyer_id,

            case_id=case_id,

            filename=file.filename
        )


        return {

            "status": "success",

            "result": result
        }


    except Exception as e:


        return {

            "status": "error",

            "message": str(e)
        }


# ==================================================
# DELETE CASE
# ==================================================

@app.delete("/cases/{case_id}")
async def delete_case(

    case_id: str,

    lawyer_id: str
):


    return {

        "deleted": case_id
    }