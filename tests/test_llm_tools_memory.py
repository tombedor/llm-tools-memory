import llm
import json
from llm_tools_memory import create_memory


def test_tool():
    model = llm.get_model("echo")
    chain_response = model.chain(
        json.dumps(
            {
                "tool_calls": [
                    {"name": "create_memory", "arguments": {"input": "pelican"}}
                ]
            }
        ),
        tools=[create_memory],
    )
    responses = list(chain_response.responses())
    tool_results = json.loads(responses[-1].text())["tool_results"]
    assert tool_results == [
        {"name": "create_memory", "output": "hello pelican", "tool_call_id": None}
    ]
