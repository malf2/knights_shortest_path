"""Finds shortest Knight's path for a 8x8 Chess board.

On the command-line user enters the knight's starting and end positions, for
example:
D4 G7
D4 D5
A1 H8

The output is the shortest knight's path displayed as following:
D4 E6 G7
D4 C2 B4 D5
A1 C2 A3 B5 D6 F7 H8
"""

import sys
import re
from heapq import heappush, heappop
from itertools import product
from collections import defaultdict


def dijkstra(graph: dict, src: str, dst: str) -> str:
    """Dijkstra algorithm to find single-source shortest path.

    Args:
        graph (dict): Graph containing all nodes and edges with nonnegative
            weights.
        src (str): Source node.
        dst (str): Destination node.

    Returns:
        str: Shortest path. (eg D4 E6 G7)
    """

    inf = sys.maxsize   # System max size for infinity.

    # Initialize all nodes costs to be infinity and predecessors to be an empty
    # list.
    node_data = {k: {'cost': inf, 'pred': []} for k in graph}

    # Cost of source is known to be zero.
    node_data[src]['cost'] = 0

    # Nodes that have been visited.
    visited = []

    # A priority queue of nodes with known costs from src.
    min_heap = [(0, src)]

    while min_heap:
        #  Get the node temp that currently has the shortest path from src.
        _, temp = heappop(min_heap)

        if src == dst:
            break

        # If node temp has already been visited, continue to another node.
        if temp in visited:
            continue

        visited.append(temp)

        # If node doesn't have neighbours, continue to another node.
        neighbours = graph[temp]
        if not neighbours:
            continue

        # Check each temp's neighbours to update costs and predecessors if
        # the neighbour has not been visited yet.
        for j in neighbours:
            if j not in visited:
                cost = node_data[temp]['cost'] + neighbours[j]
                if cost < node_data[j]['cost']:
                    node_data[j]['cost'] = cost
                    node_data[j]['pred'] = node_data[temp]['pred'] + [temp]
                heappush(min_heap, (node_data[j]['cost'], j))

    # Generate the shortest path in the format: D4 E6 G7    
    shortest_path = node_data[dst]['pred'] + [dst]
    shortest_path = ' '.join(shortest_path)
    return shortest_path


def get_mapping() -> dict:
    """Generates a mapping dictionary to transform (x, y) coordinates into
    letters and numbers.

    Example: {(1, 1): 'B2'}

    Returns:
        dict: Dictionary containing the mapping.
    """

    # Create a list with all combinations for a 8x8 Chess board: A1-H8
    letters = list(product('ABCDEFGH', '12345678', repeat=1))
    letters = list(map(lambda x: ''.join(x), letters))

    # Create a list with all (x, y) coordinates for a 8x8 Chess board:
    # (0, 0) - (7, 7)
    n = list(product('01234567', repeat=2))
    n = list(map(lambda x: (int(x[0]), int(x[1])), n))

    # Create a mapping to transform from (x, y) coordinates to alphanumerical
    # ones: A1-H8
    mapping = {num: letter for letter, num in zip(letters, n)}

    return mapping


def add_edge(graph: dict, vertex_a: str, vertex_b: str) -> None:
    """Add edges to a Graph.

    Args:
        graph (dict): Graph to add edges to.
        vertex_a (str): First vertex.
        vertex_b (str): Second vertex.
    """
    graph[vertex_a].update({vertex_b: 1})
    graph[vertex_b].update({vertex_a: 1})


def build_knights_graph(board_size: int) -> dict:
    """Build a graph representing the Knight's path in a Chess board.

    Args:
        board_size (int): Desired size of the Chess board.

    Returns:
        dict: Graph representing the Knight's path in a Chess board.

    Limitations: Builds a graph for a maximum of 8x8 board due to the
        get_mapping function.
    """

    graph = defaultdict(dict)
    mapping = get_mapping()
    for row in range(board_size):
        for col in range(board_size):
            for to_row, to_col in generate_permitted_moves_from(
                    row, col, board_size):
                
                # Add a graph edge only with permitted knight's moves
                add_edge(graph, mapping[(row, col)], mapping[(to_row, to_col)])
    return graph


# Permitted moves for a Knight in a Chess board.
PERMITTED_MOVES = (
    (-1, -2), ( 1, -2),
    (-2, -1), ( 2, -1),
    (-2,  1), ( 2,  1),
    (-1,  2), ( 1,  2),
)


def generate_permitted_moves_from(row: int, col: int, board_size: int):
    """Generates the permitted moves a Knight can perform in a Chess board.

    Args:
        row (int): Row position.
        col (int): Column position.
        board_size (int): Desired Chess board size.

    Yields:
        Iterator[tuple]: (x, y) coordinate permitted for a Knight to move.
    """

    for row_offset, col_offset in PERMITTED_MOVES:
        move_row, move_col = row + row_offset, col + col_offset
        if 0 <= move_row < board_size and 0 <= move_col < board_size:
            yield move_row, move_col


def input_isvalid(user_input: list) -> bool:
    """Validate the user input for the Knight's starting and end positions.

    Args:
        user_input (list): List with a multiple line user input.

    Returns:
        bool: User input validity.
    """
    
    input_pattern = r'^[A-H][1-8]\s[A-H][1-8]$'
    for inp in user_input:
        if not re.match(input_pattern, inp):
            return False
    return True


def main():
    """Main function containing all the steps of the script."""
    
    # Build Knight's path graph.
    knights_graph = build_knights_graph(8)

    print("Please, enter the knight's starting and ending positions"
          " in a 8x8 Chess board (eg. D4 D5) (MacOS: ^D to exit):")
    lines = []

    # Infinite loop to retrieve multiple lines of user input and to save it to 
    # a list.
    while True:
        try:
            line = input()
            if line:
                lines.append(line)

            # If no input is given, exit program.
            else:
                break

        # If ^D is pressed on macOS, EOFError is thrown and program exits.
        except EOFError:
            break

    # If user input is valid, read each instruction and return the shortest
    # path for each.
    if input_isvalid(lines):
        output = []
        for line in lines:
            start, end = line.split()
            result = dijkstra(knights_graph, start, end)
            output.append(result)
        text = '\n'.join(output)
        print(text)
    else:
        print('Invalid input. Please, enter start and end positions in a 8x8 '
                'Chess board (eg. D4 D5).')
    
    print('Press <enter> to exit.')
    input()


if __name__ == '__main__':
    main()
