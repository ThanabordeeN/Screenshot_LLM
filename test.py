from litellm import completion

response = completion(
    model="gemini/gemini-1.5-flash-002",
    messages=[{'role': 'user', 'content': 'Hello, how are you?'}],
    api_key="AIzaSyBtZZgmEu1ifMNeg2NbZPqMwXT5V6P2S-g"
)

print(response.choices[0].message.content)