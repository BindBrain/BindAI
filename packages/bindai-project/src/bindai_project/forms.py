from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FormFieldDefinition:
    id: str
    type: str
    label: str
    name: str | None = None
    description: str | None = None
    required: bool = False
    default: Any = None
    placeholder: str | None = None
    options: list[dict[str, Any]] = field(default_factory=list)
    binding: str | None = None
    validation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "id": self.id,
            "type": self.type,
            "label": self.label,
        }

        if self.name is not None:
            data["name"] = self.name

        if self.description is not None:
            data["description"] = self.description

        if self.required:
            data["required"] = True

        if self.default is not None:
            data["default"] = self.default

        if self.placeholder is not None:
            data["placeholder"] = self.placeholder

        if self.options:
            data["options"] = self.options

        if self.binding is not None:
            data["binding"] = self.binding

        if self.validation:
            data["validation"] = self.validation

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> FormFieldDefinition:
        if not isinstance(data, dict):
            raise ValueError("Form field definition must be a mapping.")

        field_id = data.get("id")
        field_type = data.get("type")
        label = data.get("label")

        if not field_id:
            raise ValueError("Form field is missing 'id'.")

        if not field_type:
            raise ValueError(
                f"Form field '{field_id}' is missing 'type'."
            )

        if not label:
            raise ValueError(
                f"Form field '{field_id}' is missing 'label'."
            )

        options = data.get("options", [])

        if not isinstance(options, list):
            raise ValueError(
                f"Form field '{field_id}' 'options' must be a list."
            )

        validation = data.get("validation", {})

        if not isinstance(validation, dict):
            raise ValueError(
                f"Form field '{field_id}' 'validation' must be a mapping."
            )

        return cls(
            id=str(field_id),
            type=str(field_type),
            label=str(label),
            name=(
                str(data["name"])
                if data.get("name") is not None
                else None
            ),
            description=(
                str(data["description"])
                if data.get("description") is not None
                else None
            ),
            required=bool(data.get("required", False)),
            default=data.get("default"),
            placeholder=(
                str(data["placeholder"])
                if data.get("placeholder") is not None
                else None
            ),
            options=[dict(option) for option in options],
            binding=(
                str(data["binding"])
                if data.get("binding") is not None
                else None
            ),
            validation=dict(validation),
        )


@dataclass(slots=True)
class FormActionDefinition:
    id: str
    label: str
    value: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "label": self.label,
            "value": self.value,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> FormActionDefinition:
        if not isinstance(data, dict):
            raise ValueError("Form action definition must be a mapping.")

        action_id = data.get("id")
        label = data.get("label")
        value = data.get("value")

        if not action_id:
            raise ValueError("Form action is missing 'id'.")

        if not label:
            raise ValueError(
                f"Form action '{action_id}' is missing 'label'."
            )

        if not value:
            raise ValueError(
                f"Form action '{action_id}' is missing 'value'."
            )

        return cls(
            id=str(action_id),
            label=str(label),
            value=str(value),
        )


@dataclass(slots=True)
class FormDefinition:
    id: str
    name: str
    version: int = 1
    description: str = ""
    fields: list[FormFieldDefinition] = field(default_factory=list)
    actions: list[FormActionDefinition] = field(
        default_factory=list
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def field(
        self,
        field_id: str,
    ) -> FormFieldDefinition:
        for item in self.fields:
            if item.id == field_id:
                return item

        raise KeyError(
            f"Unknown form field: {field_id}"
        )

    def has_field(
        self,
        field_id: str,
    ) -> bool:
        return any(
            item.id == field_id
            for item in self.fields
        )

    def add_field(
        self,
        field: FormFieldDefinition,
    ) -> None:
        if self.has_field(field.id):
            raise ValueError(
                f"Duplicate form field id: {field.id}"
            )

        self.fields.append(field)

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "version": self.version,
            "form": {
                "id": self.id,
                "name": self.name,
                "fields": [
                    item.to_dict()
                    for item in self.fields
                ],
                "actions": [
                    action.to_dict()
                    for action in self.actions
                ],
            },
        }

        if self.description:
            data["form"]["description"] = self.description

        if self.metadata:
            data["form"]["metadata"] = self.metadata

        return data

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> FormDefinition:
        if not isinstance(data, dict):
            raise ValueError("Form definition must be a mapping.")

        form_data = data.get("form")

        if not isinstance(form_data, dict):
            raise ValueError(
                "Form definition must contain a 'form' mapping."
            )

        form_id = form_data.get("id")
        form_name = form_data.get("name")

        if not form_id:
            raise ValueError(
                "Form definition is missing 'form.id'."
            )

        if not form_name:
            raise ValueError(
                "Form definition is missing 'form.name'."
            )

        raw_fields = form_data.get("fields", [])

        if not isinstance(raw_fields, list):
            raise ValueError(
                "'form.fields' must be a list."
            )

        fields = [
            FormFieldDefinition.from_dict(item)
            for item in raw_fields
        ]

        field_ids = [item.id for item in fields]

        if len(field_ids) != len(set(field_ids)):
            raise ValueError(
                "Form definition contains duplicate field ids."
            )

        raw_actions = form_data.get("actions", [])

        if not isinstance(raw_actions, list):
            raise ValueError(
                "'form.actions' must be a list."
            )

        actions = [
            FormActionDefinition.from_dict(item)
            for item in raw_actions
        ]

        metadata = form_data.get("metadata", {})

        if not isinstance(metadata, dict):
            raise ValueError(
                "'form.metadata' must be a mapping."
            )

        return cls(
            id=str(form_id),
            name=str(form_name),
            version=int(data.get("version", 1)),
            description=str(
                form_data.get("description", "")
            ),
            fields=fields,
            actions=actions,
            metadata=dict(metadata),
        )
