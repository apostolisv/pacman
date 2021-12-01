# Pacman
A pacman clone using the a* pathfinding algorithm.

### A* algorithm demo using chebyshev distance as the heuristic function
![pacman gif](https://media.giphy.com/media/m6qJDrfZLyhyv8HdIF/giphy.gif)


### A* algorithm Game demo with a distance limit of 20 blocks between player and enemy
![pacman gif](https://media.giphy.com/media/R8RYmgGBE4Ihruvej9/giphy.gif)

### Final Game demo
When the player kills a ghost, sometimes it gets teleported to it's spawn location instead of walking, in order to avoid freezing the game (the algorithm requires more time due to the location of the ghost's spawn block)

![pacman gif](https://media.giphy.com/media/Vz4u0ckCJuFJ0RpHYi/giphy.gif)

## Begin the game

To begin the game, a player has to run the main.py. The difficulty can be changed by changing the player_hunt_block_limit variable, which determines the maximum distance between player and enemy in order for the enemy to hunt the player.

## Board

The Board class consists of a simple 2D list to store the squares of the board (Nodes). Each node has a reference to top, left, right and bottom node (if it exists) and allows a Player object to move on to those referenced nodes. The ghosts' spawn points are marked as 'special access nodes' in order to prevent players from entering this location. (Only dead ghosts can have access there).

