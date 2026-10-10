from __future__ import annotations

from bindai_agent.nodes import NodeRegistry


def _validate_config(
    node,
    config,
    errors,
):
    """
    Validate Studio node configuration.
    """

    schema = node.config_schema()


    #
    # Schema must be a dictionary
    #

    if not isinstance(
        schema,
        dict,
    ):

        errors.append(
            f"Invalid config schema on {node.name}"
        )

        return


    #
    # Configuration must be a dictionary
    #

    if not isinstance(
        config,
        dict,
    ):

        errors.append(
            f"Invalid config on {node.name}: "
            f"expected object"
        )

        return


    #
    # Validate schema fields
    #

    for field_name, field_schema in schema.items():

        if not isinstance(
            field_schema,
            dict,
        ):

            errors.append(
                f"Invalid config field schema "
                f"{field_name} on {node.name}"
            )

            continue


        required = field_schema.get(
            "required",
            False,
        )

        field_type = field_schema.get(
            "type"
        )


        if (
            required
            and field_name not in config
        ):

            errors.append(
                f"Missing required config "
                f"{field_name} on {node.name}"
            )

            continue


        if field_name not in config:

            continue


        value = config[
            field_name
        ]


        #
        # Type validation
        #

        if field_type == "string":

            valid = isinstance(
                value,
                str,
            )


        elif field_type == "number":

            valid = (
                (
                    isinstance(
                        value,
                        int,
                    )
                    and not isinstance(
                        value,
                        bool,
                    )
                )
                or isinstance(
                    value,
                    float,
                )
            )


        elif field_type == "boolean":

            valid = isinstance(
                value,
                bool,
            )


        elif field_type == "object":

            valid = isinstance(
                value,
                dict,
            )


        elif field_type == "array":

            valid = isinstance(
                value,
                list,
            )


        else:

            valid = True


        if not valid:

            errors.append(
                f"Invalid config type for "
                f"{field_name} on {node.name}: "
                f"expected {field_type}"
            )


def validate_graph(
    graph,
):

    errors = []


    #
    # Node IDs
    #

    node_ids = set()

    for node in graph.nodes:

        if not node.id:

            errors.append(
                "Node id cannot be empty"
            )

        if node.id in node_ids:

            errors.append(
                f"Duplicate node id: {node.id}"
            )

        else:

            node_ids.add(
                node.id
            )


    #
    # Node types
    #

    available_types = set(
        NodeRegistry.available()
    )

    valid_nodes = {}

    for node in graph.nodes:

        if node.type not in available_types:

            errors.append(
                f"Unknown node type: {node.type}"
            )

            continue


        runtime_node = NodeRegistry.create(
            node.type
        )


        valid_nodes[
            node.id
        ] = runtime_node


        _validate_config(
            runtime_node,
            node.config,
            errors,
        )


    #
    # Build node lookup
    #

    nodes = {
        node.id: node
        for node in graph.nodes
    }


    #
    # Edge validation
    #

    input_connections = set()


    for edge in graph.edges:

        source = nodes.get(
            edge.source
        )

        target = nodes.get(
            edge.target
        )


        if source is None:

            errors.append(
                f"Missing source node: {edge.source}"
            )

            continue


        if target is None:

            errors.append(
                f"Missing target node: {edge.target}"
            )

            continue


        if source.id not in valid_nodes:

            continue


        if target.id not in valid_nodes:

            continue


        source_node = valid_nodes[
            source.id
        ]

        target_node = valid_nodes[
            target.id
        ]


        output_ports = {
            port["name"]: port
            for port in source_node.outputs()
        }

        input_ports = {
            port["name"]: port
            for port in target_node.inputs()
        }

        output_names = set(
            output_ports
        )

        input_names = set(
            input_ports
        )


        #
        # Port type compatibility
        #

        #
        # Source port
        #

        if edge.source_port not in output_names:

            errors.append(
                f"Invalid output port "
                f"{edge.source_port} "
                f"on {source.type}"
            )


        #
        # Target port
        #

        if edge.target_port not in input_names:

            errors.append(
                f"Invalid input port "
                f"{edge.target_port} "
                f"on {target.type}"
            )


        #
        # Port type compatibility
        #

        if (
            edge.source_port in output_ports
            and edge.target_port in input_ports
        ):

            source_type = output_ports[
                edge.source_port
            ].get(
                "type"
            )

            target_type = input_ports[
                edge.target_port
            ].get(
                "type"
            )

            if (
                source_type is not None
                and target_type is not None
                and source_type != target_type
            ):

                errors.append(
                    f"Incompatible port types: "
                    f"{source.type}.{edge.source_port} "
                    f"({source_type}) -> "
                    f"{target.type}.{edge.target_port} "
                    f"({target_type})"
                )


        #
        # Duplicate input connection
        #

        input_key = (
            edge.target,
            edge.target_port,
        )

        if input_key in input_connections:

            errors.append(
                f"Multiple connections to "
                f"{edge.target}.{edge.target_port}"
            )

        else:

            input_connections.add(
                input_key
            )


        #
        # Mapping validation
        #

        if edge.mapping is not None:

            if edge.mapping not in output_names:

                errors.append(
                    f"Invalid mapping "
                    f"{edge.mapping} "
                    f"on output "
                    f"{source.type}"
                )


    #
    # Cycle detection
    #

    incoming = {
        node_id: 0
        for node_id in valid_nodes
    }


    for edge in graph.edges:

        if (
            edge.source in valid_nodes
            and edge.target in valid_nodes
        ):

            incoming[
                edge.target
            ] += 1


    queue = [
        node_id
        for node_id, count in incoming.items()
        if count == 0
    ]

    visited = 0


    while queue:

        current = queue.pop(0)

        visited += 1


        for edge in graph.edges:

            if edge.source != current:

                continue


            if edge.target not in incoming:

                continue


            incoming[
                edge.target
            ] -= 1


            if incoming[
                edge.target
            ] == 0:

                queue.append(
                    edge.target
                )


    if visited != len(valid_nodes):

        errors.append(
            "Graph contains a cycle"
        )


    return errors
