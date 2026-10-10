from __future__ import annotations


def apply_inputs(
    graph,
    node_id,
    context,
):
    """
    Copy values from upstream node outputs
    into this node's input ports.
    """

    for edge in graph.edges:

        if edge.target != node_id:
            continue

        source_value = context.variables.get(
            f"studio_output_{edge.source}"
        )

        value = source_value

        #
        # If the node returned a dictionary,
        # select the requested source port.
        #

        if isinstance(
            source_value,
            dict,
        ):

            if edge.mapping is not None:

                value = source_value.get(
                    edge.mapping
                )

            else:

                value = source_value.get(
                    edge.source_port
                )

        context.variables.set(
            edge.target_port,
            value,
        )


def store_output(
    node_id,
    result,
    context,
):
    """
    Store a node's runtime result.
    """

    context.variables.set(
        f"studio_output_{node_id}",
        result,
    )

    return result
