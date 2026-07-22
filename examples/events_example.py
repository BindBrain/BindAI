from bindai_core import Event, EventBus

bus = EventBus()


def hello(event):
    print(event.name)
    print(event.payload)


bus.subscribe("hello", hello)

bus.publish(
    Event(
        name="hello",
        payload={"framework": "BindAI"},
    )
)
