

# RoboGambit 2025-26 — Software Round

## Team TERMINATOR



This program implements an autonomous AI engine designed to play a 6×6 chess variant.

The engine receives a board position and returns the best move using a search-based

decision system.



The system is designed to operate inside the RoboGambit tournament framework,

where the engine repeatedly receives updated board states and must respond

with a valid move within a time constraint.





### Board Representation and Move format:

Board is a 6x6 NumPy array

Piece encoding:

&#x20; - 0  : Empty cell

&#x20; - 1  : White Pawn

&#x20; - 2  : White Knight

&#x20; - 3  : White Bishop

&#x20; - 4  : White Queen

&#x20; - 5  : White King

&#x20; - 6  : Black Pawn

&#x20; - 7  : Black Knight

&#x20; - 8  : Black Bishop

&#x20; - 9  : Black Queen

&#x20; - 10 : Black King



Board coordinates:

&#x20; - Bottom-left  = A1  (index \[0]\[0])

&#x20; - Columns   = A–F (left to right)

&#x20; - Rows      = 6-1 (top to bottom)(from white's perspective)



Move output format:  "<piece\_id>:<source\_cell>-><target\_cell>"

&#x20; e.g.  "1:B3->B4"   (White Pawn moves from B3 to B4)





### Dependencies required to run the program: 



Python 3.8+



Required Python libraries:

numpy

Install using pip

pip install numpy







### Setup:



Clone the repository:

git clone https://github.com/<your-username>/<repo-name>.git

cd <repo-name>



Install dependencies:

pip install numpy



### Running the Engine

Running the script directly does not automatically start a game.

The engine is designed to be imported by the tournament framework, which repeatedly calls:

get\_best\_move(board, playing\_white)



Example integration:

import numpy as np

from game import get\_best\_move

board = np.array(\[

&#x20;\[2,3,4,5,3,2],

&#x20;\[1,1,1,1,1,1],

&#x20;\[0,0,0,0,0,0],

&#x20;\[0,0,0,0,0,0],

&#x20;\[6,6,6,6,6,6],

&#x20;\[7,8,9,10,8,7]

])

move = get\_best\_move(board, True)

print(move)





### AI Architecture

The engine uses several classical game search techniques.

1\. Iterative Deepening: Search depth increases gradually until time runs out.

2\. Alpha-Beta Pruning: Reduces search size by pruning branches that cannot influence the final result.

3\. Quiescence Search: keeps on calculating capture to prevent horizon effect

4\. Transposition Tables: Uses Zobrist hashing to store previously evaluated board positions.

5\. Move Ordering: Moves are sorted using MVV-LVA (Most Valuable Victim – Least Valuable Attacker) to improve pruning efficiency.



### Evaluation Function

###### The evaluation function combines:



Material Score: Standard piece values.


Piece-Square Tables: Encourages strong piece placement.

Pawn Structure:

* Passed pawns
* Doubled pawns
* Isolated pawns
* Pawn chains



Piece Activity

* Knight outposts
* Bishop pair bonus



King Safety

* Distance from enemy queen
* Escape squares
* Pin Detection



#### References

The engine design was inspired by the following resources:

Chess Programming Wiki  

https://www.chessprogramming.org



Sebastian Lague — Chess Coding Adventure  

https://www.youtube.com/watch?v=U4ogK0MIzqk



