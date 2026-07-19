from __future__ import annotations

from typing import Any


class Variables:
    """
    Runtime variable storage.

    Behaves similarly to a dictionary while
    allowing future validation and tracking.
    """

    def __init__(self):

        self._values: dict[str, Any] = {}

    #
    # CRUD
    #

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._values[key] = value

    def get(
        self,
        key: str,
        default=None,
    ):

        return self._values.get(
            key,
            default,
        )

    def update(
        self,
        values: dict | "Variables",
    ) -> None:

        if isinstance(
            values,
            Variables,
        ):

            self._values.update(
                values._values,
            )

        else:

            self._values.update(
                values,
            )

    def contains(
        self,
        key: str,
    ) -> bool:

        return key in self._values

    def remove(
        self,
        key: str,
    ) -> None:

        self._values.pop(
            key,
            None,
        )

    def clear(
        self,
    ) -> None:

        self._values.clear()

    #
    # Helpers
    #

    def copy(
        self,
    ) -> "Variables":

        variables = Variables()

        variables.update(
            self,
        )

        return variables

    def as_dict(
        self,
    ) -> dict[str, Any]:

        return dict(
            self._values,
        )

    #
    # Python API
    #

    def __getitem__(
        self,
        key,
    ):

        return self._values[key]

    def __setitem__(
        self,
        key,
        value,
    ):

        self._values[key] = value

    def __contains__(
        self,
        key,
    ):

        return key in self._values

    def __iter__(
        self,
    ):

        return iter(
            self._values,
        )

    def __len__(
        self,
    ):

        return len(
            self._values,
        )