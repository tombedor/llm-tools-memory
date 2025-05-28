from dataclasses import asdict
from datetime import datetime
from typing import Optional

import llm
from sqlite_utils import Database


class Memory(llm.Toolbox):
    """
    A toolbox for creating and searching memories using embeddings.

    This class provides tools for storing text as embeddings in a database
    and retrieving relevant memories based on semantic similarity.

    Attributes:
        database (str): Path to the SQLite database file
        rag (RAG): Retrieval-augmented generation instance
        collection (llm.Collection): Collection for storing embeddings
    """

    def __init__(
        self, database: Optional[str] = None, search_relevance_threshold: float = 0.5
    ):
        """
        Initialize the Memory toolbox.

        Args:
            database (Optional[str]): Path to the SQLite database file.
                                     If None, defaults to embeddings.db in the user directory.
            search_relevance_threshold (float): Minimum relevance score for search results.

        """
        self.database = (
            database if database is not None else str(llm.user_dir() / "embeddings.db")
        )
        self.collection = llm.Collection(
            "memory", db=Database(self.database), create=True, model_id="3-small"
        )
        self.search_relevance_threshold = search_relevance_threshold

    def create_memory(self, input: str, id: Optional[str] = None) -> None:
        """
        Create a new memory by embedding the input text.

        Args:
            input (str): The text content to store as a memory
            id (Optional[str]): Unique identifier for the memory.
                               If None, a timestamp-based ID will be generated.
                               If ID matches an existing memory, it will be updated.

        """
        self.collection.embed(
            id=id or "Memory created at " + datetime.now().isoformat(),
            value=input,
            metadata={
                "created_at_utc": datetime.now().isoformat(),
            },
            store=True,
        )

    def search_memory(self, query: str, number=3) -> list[dict]:
        """
        Search for memories semantically similar to the query.

        Args:
            query (str): The search query text

        Returns:
            list[dict]: A list of dictionaries containing relevant memories.
                       Each dictionary includes the memory content and metadata.
        """
        return [
            asdict(entry)
            for entry in self.collection.similar(query, number=number)
            if entry.score and entry.score >= self.search_relevance_threshold
        ]


@llm.hookimpl
def register_tools(register):
    register(Memory)
