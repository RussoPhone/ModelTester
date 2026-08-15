import subprocess
from ollama import chat


def run_command(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
    )

    return (
        f"EXIT CODE: {result.returncode}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}"
    )


tools = [run_command]

messages = [
    {
        "role": "user",
        "content": (
            "Execute o comando `python test/hello.py` "
            "usando a ferramenta disponível e me diga o resultado."
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

for tool_call in response.message.tool_calls or []:
    if tool_call.function.name == "run_command":
        command = tool_call.function.arguments["command"]
        result = run_command(command)

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
