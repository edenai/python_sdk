from email.mime import base
import requests
from typing import Any, Callable, TypeVar, Generic, Union
import time
import json

T = TypeVar("T", bound="BaseClient")


class BaseClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url

    def get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _make_request(
        self, endpoint: str, method: str = "GET", data: Any = None
    ) -> Any:
        url = f"{self.base_url}/{endpoint}"
        headers = self.get_headers()
        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            try:
                return response.json()
            except (requests.exceptions.InvalidJSONError, TypeError) as json_exc:
                raise Exception(
                    "Response was not JSON as excpected", exc_info=json_exc
                ) from json_exc
        except requests.exceptions.RequestException as http_exc:
            raise Exception(
                f"Request failed with status: {response.status_code}"
            ) from http_exc


class WorkflowClient(BaseClient):
    def create_or_update(self, name: str, data: Any) -> Any:
        return self._make_request(
            "workflow/", method="POST", data={"code": data, "name": name}
        )

    def execute(self, name: str, data: Any) -> Any:

        execution = self._make_request(
            f"workflow/name/{name}/execution/", method="POST", data=data
        )

        while True:
            execution = self._make_request(
                f"workflow/name/{name}/execution/{execution['id']}",
                method="GET",
                data=data,
            )

            if execution["content"]["status"] == "error":
                raise Exception(f"Execution failed. Response: {execution}")
            if execution["content"]["status"] not in ["running", "waiting"]:
                break

            time.sleep(1)  # Wait for 1 second before polling again

        if (
            execution["content"]["status"] == "success"
            and "output" in execution["content"]["results"]
        ):
            # if  isinstance(execution["content"]["results"]["output"]["results"], list):
            return {"output": execution["content"]["results"]["output"]["results"][0]}
        else:
            return {"output": None}


class Client(Generic[T]):
    client: Union[None, T]

    def __init__(self, client: Generic[T]):

        self.client = client

    def __getattr__(self, name: str) -> Callable[..., Any]:
        if self.client and hasattr(self.client, name):
            return getattr(self.client, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


def workflow_client(
    api_key: str, base_url="https://api.edenai.run/v2"
) -> WorkflowClient:

    return Client(client=WorkflowClient(api_key=api_key, base_url=base_url))
