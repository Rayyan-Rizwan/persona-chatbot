import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage,HumanMessage,SystemMessage

load_dotenv()

# Use an active Groq model ID
model = init_chat_model(
    "groq/compound-mini",
    model_provider="groq",
    temperature = 0.9,
)
print("Press 1 for sad assistant, 2 for helpful assistant and 3 for funny assistant")
choice = input("Enter your choice: ")
if choice == "1":
    message = [
        SystemMessage(content="You are a sad assistant and reply in sad way everytime.")
    ]
elif choice == "2":
    message = [
        SystemMessage(content="You are a helpful assistant.")
    ]
elif choice == "3":
    message = [
        SystemMessage(content="You are a funny assistant.")
    ]
else:
    print("Invalid choice. Exiting.")
    exit()

print("-----------------------Type 'exit' to quit.---------------------")
while True:
    
    prompt = input("You: ")
    message.append(HumanMessage(content=prompt))
    if prompt.lower() == "exit":
        break
    # Test invocation
    response = model.invoke(message)
    message.append(AIMessage(content=response.content))
    print(f"Bot: {response.content}")

print (message)