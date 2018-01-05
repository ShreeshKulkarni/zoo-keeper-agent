# zoo-keeper-agent
Solution to Modified N-Queens using BFS, DFS and Simulated Annealing Algorithms

Short Description: A Zookeeper AI Agent in Python 2.7, to place baby lizards (analogous to Queens in N-Queens Problem) in a nursery safely.


Challenges
----------
A lizard placed in a spot on the grid can kill other lizards in the same row, same column and on the diagonals.
Additionally, the nursery can have some trees planted in it (locations are part of input). These trees act as barricades and prevent lizards from shooting their tongues across them. Essentially, a tree will block any lizard from eating another lizard if it is in the path.


Input
-----
The program reads a text file "input.txt" in the current directory. This file contains the problem description in the format:

First line: 	Instruction of which algorithm to use: BFS, DFS or SA
Second line: 	Strictly positive 32-bit integer n, the width and height of the square nursery
Third line: 	Strictly positive 32-bit integer p, the number of baby lizards to be placed
Next n lines: The n x n nursery, one file line per nursery row
The nursery has a 0 where there is nothing, and a 2 where there is a tree.

An example "input.txt" and the corresponding "output.txt" are uploaded in the repository.


Output
------
Solution is written to "output.txt" in the current directory. The format is as follows:

First line: 	OK or FAIL, indicating whether a solution was found or not.
Next n lines: (If a solution was found) The n x n nursery, one line in the file per nursery row, including the baby lizards and trees. 			It will have a 0 where there is nothing, a 1 where the program placed a baby lizard, and a 2 where there is a 				tree.


How to Run?
----------
Needs Python 2.7 interpreter
> python zookeeperAgent.py


Note
----
The program prints "FAIL" when either a solution cannot be found no matter what (for example, trying to place 10 lizards on a 3x3 board..) or when the program times out after running for 5 minutes.
