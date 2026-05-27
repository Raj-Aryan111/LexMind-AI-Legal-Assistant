from qdrant_client import (
    QdrantClient
)

from qdrant_client.models import (
    VectorParams,
    Distance
)


# ==================================================
# QDRANT CLIENT
# ==================================================

client = QdrantClient(

    path="qdrant_data"
)


# ==================================================
# CREATE COLLECTION
# ==================================================

client.recreate_collection(

    collection_name="case_files",

    vectors_config=VectorParams(

        size=384,

        distance=Distance.COSINE
    )
)


print(

    "case_files collection ready"
)