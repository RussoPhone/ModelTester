from ollama import chat 

def edit_file(path: str, old:str, new:str) -> str:
    with open(path, "r", encoding="utf-8") as file:
        content = file.read()

    if old not in content:
        return f"Text not found in {path}"

    content = content.replace(old, new, 1)

    with open(path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"File {path} edited succesfully."

tools = [edit_file]

messages = [
    {
        "role": "user",
        "content": (
            'Altere o arquivo teste/test.py. '
            'Troque "HELLO WORLD" por "HELLO HEFESTO".'
        ),
    }
]

print("Calling model.........", flush=True)

response = chat(
    model="qwen3-coder:30b",
    messages=messages,
    tools=tools,
    think=False,
)

print("model replied", flush=True)
print("CONTENT:", repr(response.message.content))
print("TOOL CALLS:", repr(response.message.tool_calls))

messages.append(response.message)

for tool_call in response.message.tool_calls:
    if tool_call.function.name == "edit_file":
        args = tool_call.function.arguments

        result = edit_file(
            args["path"],
            args["old"],
            args["new"],
        )

        messages.append({
            "role": "tool",
            "content": result,
        })

response = chat(
    model="qwen3-coder:30b",
    messages=messages,
    tools=tools,
    think=False,
)

print("FINAL:", response.message.content)
