from graph import build_graph

EXPECTED_NODES = {
    "discover_reports",
    "validate_reports",
    "load_intelligence",
    "classify_prompt_type",
    "build_prompt_context",
    "generate_prompt",
    "validate_prompt",
    "save_outputs",
}


def test_build_graph_returns_compiled_graph():
    g = build_graph()
    assert g is not None


def test_build_graph_has_expected_nodes():
    g = build_graph()
    graph_obj = g.get_graph()
    node_names = set(graph_obj.nodes) - {"__start__", "__end__"}
    assert node_names == EXPECTED_NODES


def test_build_graph_node_count():
    g = build_graph()
    graph_obj = g.get_graph()
    # 8 user nodes + __start__ + __end__
    assert len(graph_obj.nodes) == 10


def test_build_graph_deterministic():
    g1 = build_graph()
    g2 = build_graph()
    nodes1 = set(g1.get_graph().nodes)
    nodes2 = set(g2.get_graph().nodes)
    assert nodes1 == nodes2
