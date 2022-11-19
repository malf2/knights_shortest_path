# Knight's shortest path between two points in a 8x8 Chess Board.
This program receives user instructions from the command line and returns the shortest path between two points in a 8x8 Chess Board. The instructions are the Knight's starting and ending positions, e.g.:
```
D4 G8
A1 H8
```
The shortest path is calculated and returned as:
```
D4 C6 E7 G8
A1 C2 A3 B5 D6 F7 H8
```
## Instructions
Python 3.10.7 was used to develop this project.

The easiest way to execute this program is to run the  unix executable file `knights_shortest_path` in the project's folder. This will open the command-line and ask for instructions.

Alternatively, clone this project and execute `Makefile`. This will install the dependencies and run tests. Open the python file `main.py`.

## Assumptions and Decisions
The Djikstra's algorithm was chosen for being one of the most famous and successful algorithms for finding the  shortest path between two points in a Graph for a single source. Another reason is because the Knight's path in a chess board can be constructed as a graph when considering the possible knight moves as the neighbour nodes of the knight's current position.


