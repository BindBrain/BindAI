from bindai_core import Conversation


conversation = Conversation()

conversation.add_system("You are helpful.")

conversation.add_user("Hello!")

conversation.add_assistant("Hi there!")

for message in conversation.messages:
    print(
        message.role,
        message.content,
    )

print()

print(len(conversation))
