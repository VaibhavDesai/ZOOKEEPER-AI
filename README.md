# ZOOKEEPER-AI
Zookeeper AI is a AI agent who's task is to place baby reptile in a reptile house. Job is to find a place to puteach baby lizard in a nursery. However, there is a catch, the baby lizards have very long tongues. A baby lizard can shoot out its tongue and eat any other baby lizard before you have time to save it. As such, Agent want to make sure that no baby lizard can eat another baby lizard in the nursery (burp).  For each baby lizard, you can place them in one spot on a grid. From there, they can shoot out their tongue up, down, left, right and diagonally as well. Their tongues are very long and can reach to the edge ofthe nursery from any location.

There is a twist to this game. In addition to baby lizards, your nursery may havesome trees planted in it. Your lizards cannot shoot their tongues through the trees nor can agent move a lizard into the same place as a tree. As such, a tree will block any lizard from eating another lizard if it is in the path. Additionally, the tree will block the agnet from moving the lizard to that location.

Input:The file input.txt will be formatted as follows:

First line: instruction of which algorithm to use: BFS, DFS or SA

Second line: strictly positive 32-bit integer n, the width and height of the square nursery

Third line: strictly positive 32-bit integerp, the number of baby lizardsNext n lines: the n x n nursery, one file line per nursery row (to show you where the trees are).It will have a 0 where there is nothing, and a 2 where there is a tree.
