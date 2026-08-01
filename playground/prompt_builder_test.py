from bindai_core import (
    Conversation,
    PromptBuilder,
)

conversation = Conversation()

conversation.add_user("Hello")

conversation.add_assistant("Hi!")


request = PromptBuilder().system("You are helpful.").conversation(conversation).build()

for message in request.messages:
    print(
        message.role,
        message.content,
    )
