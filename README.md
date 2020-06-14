# Hungarian-Globe-Puzzle
Solved the Hungarian Globe using BFS and A*-Search approach.


![Image of the glovbe](https://i.pinimg.com/originals/20/d7/78/20d778c8c6166a38dc0ed3b04158f68e.jpg)

It is a puzzle similar to the Rubick's Cube, based on tile rotation.

This code uses Artificial Intelligence algorithms to solve the puzzle using BFS and A* Search techniques.

For A* the Heuristic of **Manhattan distance** is used.  
**Distance = abs(Current_location (x co-ord) – Goal_location (x co-ord) + Current_location (y co-ord) – Goal_location (y co-ord.))**

You need to provide a file as mentioned in the resources folder.  
Example line in the input file:  
`Tile(30-180, (60,180), Exact(30,180))`  
`Where _'30-180'_ is the ID of the tile, _'60-180'_ is the initial location of the tile and _'30,180'_ is the final or goal location of that tile.`   

This code will be called as follows:  
`Search.py <ALG> <FILE>`  
`Where ALG is one of: ”BFS” or ”AStar” and FILE is the puzzle file name.`
