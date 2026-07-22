class SnapshotStore:

    def save(
        self,
        snapshot,
    ):
        ...

    def load(
        self,
        execution_id,
    ):
        ...

    def delete(
        self,
        execution_id,
    ):
        ...