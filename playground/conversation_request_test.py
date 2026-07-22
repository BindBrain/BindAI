from bindai_core import Conversation

conversation = Conversation()

conversation.add_system("You are helpful.")

conversation.add_user("Hello!")

request = conversation.to_request()

print(len(request.messages))

for message in request.messages:
    print(
        message.role,
        message.content,
    )
