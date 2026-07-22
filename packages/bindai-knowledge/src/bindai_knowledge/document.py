from dataclasses import dataclass, field


@dataclass(slots=True)
class KnowledgeDocument:
    id: str

    title: str

    content: str

    metadata: dict[str, object] = field(
        default_factory=dict,
    )
