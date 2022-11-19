"""This script tests the functions in the main.py module.
"""

from itertools import product

from main import dijkstra, build_knights_graph, generate_permitted_moves_from, \
    input_isvalid


def test_dijkstra():
    """Test if the Djikstra algorithm returns the correct shortest paths.
    """

    graph = {
        'A': {'B': 2, 'C': 4},
        'B': {'A': 2, 'C': 3, 'D': 8},
        'C': {'A': 4, 'B': 3, 'E': 5, 'D': 2},
        'D': {'B': 8, 'C': 2, 'E': 11, 'F': 22},
        'E': {'C': 5, 'D': 11, 'F': 1},
        'F': {'D': 22, 'E': 1}
    }

    results = [
        'A',
        'A B',
        'A C',
        'A C D',
        'A C E',
        'A C E F',
        'B A',
        'B',
        'B C',
        'B C D',
        'B C E',
        'B C E F',
        'C A',
        'C B',
        'C',
        'C D',
        'C E',
        'C E F',
        'D C A',
        'D C B',
        'D C',
        'D',
        'D C E',
        'D C E F',
        'E C A',
        'E C B',
        'E C',
        'E C D',
        'E',
        'E F',
        'F E C A',
        'F E C B',
        'F E C',
        'F E C D',
        'F E',
        'F'
    ]
    nodes = ''.join(graph.keys())
    paths = list(product(nodes, repeat=2))
    for p, r in zip(paths, results):
        assert dijkstra(graph, p[0], p[1]) == r


def test_build_knights_graph():
    """Test if the Knight's path graph is built correctly for a 3x3 Chess board
    for simplicity.
    """

    output = {
        'A1': {'C2': 1, 'B3': 1}, 
        'C2': {'A1': 1, 'A3': 1}, 
        'B3': {'A1': 1, 'C1': 1}, 
        'A2': {'C1': 1, 'C3': 1}, 
        'C1': {'A2': 1, 'B3': 1}, 
        'C3': {'A2': 1, 'B1': 1}, 
        'A3': {'B1': 1, 'C2': 1}, 
        'B1': {'A3': 1, 'C3': 1}
    }
    assert build_knights_graph(3) == output


def test_generate_permitted_moves_from():
    """Test if the permitted moves generate correctly.
    """

    inputs = list(product('012', repeat=2))
    outputs = [
        [(2, 1), (1, 2)],
        [(2, 0), (2, 2)],
        [(1, 0), (2, 1)],
        [(0, 2), (2, 2)],
        [],
        [(0, 0), (2, 0)],
        [(0, 1), (1, 2)],
        [(0, 0), (0, 2)],
        [(1, 0), (0, 1)]
    ]
    for inp, output in zip(inputs, outputs):
        result = list(generate_permitted_moves_from(
                        int(inp[0]), int(inp[1]), 3))
        assert result == output


def test_input_isvalid():
    """Test user input validity.
    """
    
    output1 = 'D4 D5'   # Should be valid.
    output2 = 'A1 H9'   # H9 does not exist for 8x8 board.
    output3 = 'A1  H8'  # More than one blank space.

    assert input_isvalid([output1]) == True
    assert input_isvalid([output2]) == False
    assert input_isvalid([output3]) == False
