## Program

To write my first Python code, this is a pathfinding approach to solve the Rubik's cube. Three pathfinding approaches:

The first approach is a breadth-first search that uses a "visited" logic to avoid adding nodes already in the queue. Notice that the solutionness of a state is checked right before adding it to the list, as supposed to when popped from it. This makes finding the solution way faster, even if the time to explore the whole space (around 40 seconds on my pc) is about 10% slower, due to the "next" lists being longer.  
Another way to speed it up about another 10% would be to get rid of the per-depth-level logic and just add items to the list till it's empty. The data types are correct, so it's only about reducing the amount of O(1) operations.

The second is an iterative depth approach, that doesn't necessarily find the best solution, nor it explores the whole space faster (it takes about twice the time) but brings some attention to the unintuitive behaviors of depth-first pathfinding:  
The reason why it doesn't find the best solution is because it uses the visited logic, but it doesn't know if a solution is the shortest. Think about how there could be a faster path to any of the intermediate states of the found path. Getting rid of the visited logic would allow the algorithm to find the best (and every other) one, but it could take a while, even after cutting off some branches.
Another interesting point is that no iteration of this version (any that Python can handle) explores the whole net, but the visited logic makes it visit a different set of nodes in each one. This is why it is important to check if every state is the solution and not just the deepest ones.

The third is a hash function-based direct solve. The first time it is called, it fills a dictionary (that could instead be imported from a file or some other faster way) using the BFS algorithm (giving this modularity to it makes the BFS very slightly slower). The dictionary relates the solved state with every other, returning its shortest (or one of all its shortest) path. So the algorithm gets this path giving the scrambled state as an argument, and just inverses it to find the shortest path from it to the solved state.


I have tested A LOT of versions and data structures, non of them using heuristics, since I don't know enough about the problem to apply any, even if doing so would be rather easy with a priority queue.

When the cube class is imported its static method fills the dictionary with the key to orientation handling when turning. I tried to extend this idea to make the turn function direct but I wasn't able to easily fill the dictionary with the 3.6 million * 9 entrances. Since I didn't even know if those many entrances are hashable, or worth hashing, I gave up on that.  
In general, the implementation might not be the best nor Python the most adequate language, but even if it was twice as good it would only take half the time. There are 3.6 million states to be visited after all.

The fastest way to explore the whole space is, by far, to just go as deep as the language will allow you. It's four times faster than the BFS technique.  
Fun fact, if I was to extend the breadth-first algorithm into the 3x3 cube it would take my pc around 100 thousand years to explore every state.

## Key

                  |-----||-----|
                  |  19 ||  17 |
                  |-----||-----|
                  |-----||-----|
                  |  8  ||  10 |
                  |-----||-----|
    |-----||-----||-----||-----||-----||-----|
    |  20 ||  7  ||  6  ||  9  ||  11 ||  16 |
    |-----||-----||-----||-----||-----||-----|
    |-----||-----||-----||-----||-----||-----|
    |  22 ||  5  ||  3  ||  0  ||  1  ||  14 |
    |-----||-----||-----||-----||-----||-----|
                  |-----||-----|
                  |  4  ||  2  |
                  |-----||-----|
                  |-----||-----|
                  |  23 ||  13 |
                  |-----||-----|
                  |-----||-----|
                  |  21 ||  12 |
                  |-----||-----|
                  |-----||-----|
                  |  18 ||  15 |
                  |-----||-----|                  