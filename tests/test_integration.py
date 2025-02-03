import pytest
import os
import sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from edenai_sdk.workflow import workflow_client
from .example_workflow import example_workflow


@pytest.fixture(scope="module")
def client():
    return workflow_client(
        api_key=os.environ.get("API_KEY")
    )


def test_create_or_update(client):
    response = client.create_or_update(name="code_test", data=example_workflow)
    assert "id" in response
    assert response["name"] == "code_test"


def test_execute(client):
    client.create_or_update(name="code_test", data=example_workflow)
    data = {"text": "tell a story about lyon, france"}
    execution = client.execute(name="code_test", data=data)
    assert "output" in execution
    assert "items" in execution["output"]


if __name__ == "__main__":
    pytest.main()
