from qdrant_client import (
    QdrantClient
)

from qdrant_client.models import (

    Distance,

    VectorParams
)


# ==================================================
# SHARED CLIENT
# ==================================================

client = QdrantClient(

    path="shared_qdrant"
)


# ==================================================
# CREATE COLLECTION
# ==================================================

collections = client.get_collections().collections

collection_names = [

    c.name

    for c in collections
]


if "case_files" not in collection_names:


    client.create_collection(

        collection_name="case_files",

        vectors_config=VectorParams(

            size=384,

            distance=Distance.COSINE
        )
    )


    print(

        "\nCreated case_files collection\n"
    )