import hashlib
import json
import os
import tempfile
from typing import Generator, Iterable, Iterator, List, Optional, Union

import pytest
from llm.default_plugins.openai_models import OpenAIEmbeddingModel

from llm_tools_memory import Memory


class MockEmbeddingModel(OpenAIEmbeddingModel):
    CACHE_DIR = os.path.join(os.getcwd(), "tests", ".cache")

    def embed(self, item: Union[str, bytes]) -> List[float]:

        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

        assert isinstance(item, str), "Item must be a string for testing"
        md5 = hashlib.md5(item.encode("utf-8")).hexdigest()

        cache_file = os.path.join(self.CACHE_DIR, f"{md5}.json")

        if os.path.exists(cache_file):
            with open(cache_file, "r") as f:
                return json.load(f)
        else:
            result = super().embed(item)
            with open(cache_file, "w") as f:
                json.dump(result, f)
            return result


@pytest.fixture
def memory() -> Generator[Memory, None, None]:
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        db_path = tmp_file.name

    # Create the memory instance
    memory = Memory(database=db_path)

    # Patch the collection.model() method to return our MockEmbeddingModel
    original_model = memory.collection.model

    def patched_model():
        # Create a cache directory if it doesn't exist
        return MockEmbeddingModel("3-small", "text-embedding-3-small")

    # Apply the monkey patch
    memory.collection.model = patched_model

    yield memory

    # Restore the original method after the test
    memory.collection.model = original_model
    os.unlink(db_path)


def test_basic(memory: Memory):
    memory.create_memory("The magic number is 42", id="the magic number")
    memory.create_memory("Baseball is my favorite sport", id="hobbies")
    memory.create_memory("I dislike anchovies", id="food")

    results = memory.search_memory("What is the magic number?")
    assert len(results) == 1
    assert "42" in results[0]["content"]


def test_updated(memory: Memory):
    memory.create_memory("The magic number is 42", id="the magic number")
    memory.create_memory("Baseball is my favorite sport", id="hobbies")
    memory.create_memory("I dislike anchovies", id="food")
    memory.create_memory("The magic number is 43", id="the magic number")

    results = memory.search_memory("What is the magic number?")
    assert len(results) == 1
    assert "43" in results[0]["content"]


def test_search_relevance_threshold(memory: Memory):
    memory.create_memory("The magic number is 42", id="the magic number")
    memory.create_memory("Baseball is my favorite sport", id="hobbies")
    memory.create_memory("I dislike anchovies", id="food")

    memory.search_relevance_threshold = 0

    results = memory.search_memory("What is the magic number?")
    assert len(results) == 3
    assert "42" in results[0]["content"]  # most relevant result is still first.
