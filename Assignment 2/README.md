Mini-project 2 of COMP472 class taught at Concordia University by Professor Leila Kosseim at Fall2021.

Line 'em up is a generalization of tic-tac-toe. The game is won when a certain number of consecutive pieces (either 'X' or 'O') is placed in a horizontal, vertical or diagonal line within the grid. There may also be blocs ('B') within the grid where no piece can be placed.

See the following examples:
```buildoutcfg
		['O', 'O', '.', 'B', '.']
		['X', 'B', '.', '.', '.']
		['B', 'X', '.', 'B', '.']
		['O', 'B', 'X', '.', '.']
		['.', 'O', 'B', 'X', '.']
		
	X won (diagonally) with grid-size = 5 x 5, blocs at [(0,3), (1,1), (2,0), (2,3), (3,1), (4,2)] and winning-size = 4
        
                ['O', 'O', 'X', 'B', 'X']
		['X', 'B', 'X', 'X', 'O']
		['B', 'X', '.', 'B', 'O']
		['O', 'B', 'X', 'X', 'O']
		['X', 'O', 'B', 'O', 'O']
		
	O won (vertically) with grid-size = 5 x 5, blocs at [(0,3), (1,1), (2,0), (2,3), (3,1), (4,2)] and winning-size = 4
		
		['O', 'O', 'O', 'B', 'X'],
		['X', 'B', 'X', 'X', 'X'],
		['B', 'O', 'O', 'B', 'O'],
		['O', 'B', 'O', 'O', 'X'],
		['X', 'O', 'B', 'X', 'X']
		
	Game tied with grid-size = 5 x 5, blocs at [(0,3), (1,1), (2,0), (2,3), (3,1), (4,2)] and winning-size = 4
	
```

This mini-project implements a line 'em up AI using state-space graph search and 2 heuristics. Player_X and Player_O's 
heuristic, search depth, the game's board-size, bloc number and positions can be controlled 
by the constructor and the play function. 

The code skeleton is based on https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python. The 2 heuristics are
unsophisticated, but that is not the main point of this project. So enjoy beating the dumb AIs! :D   

Organization:
```buildoutcfg
line_em_up.py (src)
gameTrace-3032.txt (sample output 1)
gameTrace-4145.txt (sample output 2)
gameTrace-8651.txt (sample output 3)

```
