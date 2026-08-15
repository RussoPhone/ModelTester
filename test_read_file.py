from ollama import chat


def read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


tools = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the contents of a text file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read.",
                    }
                },
                "required": ["path"],
            },
        },
    }
]

messages = [
    {
        "role": "user",
        "content": "Read the file teste.txt and tell me what language it contains.",
    }
]

print("Calling model.........", flush=True)

response = chat(
    model="qwen3-coder:30b",
    messages=messages,
    tools=tools,
)

print("model replied")
print("CONTENT:", repr(response.message.content))
print("TOOL CALLS:", repr(response.message.tool_calls))

if response.message.tool_calls:
    tool_call = response.message.tool_calls[0]

    if tool_call.function.name == "read_file":
        path = tool_call.function.arguments["path"]
        result = read_file(path)

        messages.append(response.message)
        messages.append({
            "role": "tool",
            "content": result,
        })

        response = chat(
            model="qwen3-coder:30b",
            messages=messages,
            tools=tools,
        )

        print("FINAL:", response.message.content)
