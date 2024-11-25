# Python SDK for EdenAI workflows

This package is in **alpha** and the api can still change

## Installation

```sh
pip install edenai_sdk
```

## Example

You can use `client.create_or_update(name="my_unique_name", data=data)` to create a workflow. If a workflow with this name already exists
it will update the workflow. You can always view the workflow you've build in the UI in the [EdenAI App](https://app.edenai.run/v2/workflows)

To see which parameters are availabe for each feature, you can check our [api docs](https://docs.edenai.co/reference/text_chat_create)

```python

from edenai_sdk.workflow import workflow_client

def main():
    client = workflow_client(
        api_key=os.environ.get("API_KEY")
    )

    data = {
        "nodes": [
            {
                "type": "input",
                "name": "Input_Node",
                "data": [
                    {"type": "string", "label": "text", "defaultValue": "Hello, world!"}
                ],
            },
            {
                "type": "text/chat",
                "name": "some_chat",
                "data": [
                    {"name": "provider", "value": "openai/gpt-4o"},
                    {"name": "text", "value": "explain me: {{Input_Node.text}}"},
                ],
            },
            {
                "type": "translation/automatic_translation",
                "name": "Translation",
                "data": [
                    {"name": "provider", "value": "google"},
                    {"name": "text", "value": "{{some_chat.generated_text}}"},
                    {"name": "source_language", "value": "en"},
                    {"name": "target_language", "value": "fr"},
                ],
            },
            {
                "type": "text/keyword_extraction",
                "name": "Keywords",
                "data": [
                    {"name": "provider", "value": "openai"},
                    {"name": "text", "value": "{{Translation.text}}"},
                ],
            },
            {
                "type": "code",
                "name": "some_code",
                "data": [
                    {
                        "name": "code",
                        "value": "const valueFromInput = {{ Input_Node.text }};\n  const valueFromNode = {{ some_chat.generated_text }};  \nfunction greet(msg) {\n  return `welcome ${msg}!`;\n};\n\nreturn {\n input: greet(valueFromInput),\n node: greet(valueFromNode),\n};",
                    }
                ],
            },
            {
                "type": "output",
                "name": "Output_Node",
                "data": [{"name": "french_keywords", "value": "{{Keywords.items[*].keyword}}"}],
            },
        ]
    }

    response = client.create_or_update(name="code_test", data=data)
    execution = client.execute(name="code_test", data={"text": "Tell me a story about Eden AI"})
    print(execution["output"])



if __name__ == "__main__":
    main()


```
