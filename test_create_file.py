from ollama import chat
from pathlib import Path


def create_file(path: str, content: str) -> str:
    target = Path(path)

    if target.exists():
        return f"File already exists: {path}"

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return f"File created successfully: {path}"


tools = [create_file]


messages = [
    {
        "role": "user",
        "content": (
            "Crie o arquivo test/created.py contendo um programa "
            "que imprime HELLO FROM CREATED FILE."
        ),
    }
]


print("Calling model.........", flush=True)

while True:
    response = chat(
        model="qwen3-coder:30b",
        messages=messages,
        tools=tools,
        think=False,
    )

    messages.append(response.message)

    print("model replied", flush=True)
    print("CONTENT:", repr(response.message.content))
    print("TOOL CALLS:", repr(response.message.tool_calls))

    if not response.message.tool_calls:
        break

    for tool_call in response.message.tool_calls:
        name = tool_call.function.name
        args = tool_call.function.arguments

        if name == "create_file":
            result = create_file(
                args["path"],
                args["content"],
            )
        else:
            result = f"Unknown tool: {name}"

        messages.append({
            "role": "tool",
            "tool_name": name,
            "content": str(result),
        })


print("FINAL:", response.message.content)
