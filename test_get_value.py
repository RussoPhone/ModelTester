from ollama import chat

def get_test_value() -> str: # "test that returns a fixed value"
    return "TEST_OK"

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_test_value",
            "description": "Returns a fixed test value",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    }
]


messages = [
    {
        "role": "user",
        "content": "Use the get_test_value tool.",
    }
]

print("Calling model.........", flush=True)

response = chat(
    model="qwen3-coder:30b", #choose local model to test here 
    messages=messages,
    tools=tools,
)

print("model replied", flush=True)
print("CONTENT:", repr(response.message.content))
print("THINKING:", repr(response.message.thinking))
print("TOOL CALLS:", repr(response.message.tool_calls))

tool_call = response.message.tool_calls[0]

if tool_call.function.name == "get_test_value":
    result = get_test_value()

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
