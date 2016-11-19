## Hints

Try to think of the problem as follows:

Remember that we want to update the state of any given cell
based on the *current* state of the grid. In other words, when
we loop over the cells in the grid, **we must not modify them.**

When we talk about a *grid* here, we're referring to a data structure
that represents a two-dimensional grid. The simplest way to do this
is to use a 2D array. *Iterating* across the array is basically doing
a double for loop across the dimensions of the array.

So before we start, we should make a second grid that represents
the state of the game at the *end* the turn. The grid that we iterate
upon is the state of the game at the *start* of the turn.

By default, you should make this *end state* grid empty.

1. For every cell in the *start state* grid (cell `c` at location `(p, q)`)
   1. Check how many neighbors it has
   2. If it is alive:
      1. If it has two or three neighbors, create a new cell on the
         *end state* grid at `(p, q)`
      2. Otherwise don't do anything.
   3. If it is dead:
      1. If it has exactly three neighbors, create a new cell on the
         *end state* grid at `(p, q)`

To iterate across a grid called `start_state`, consider the following code:

```python
for i in range(len(start_state)):
    for j in range(len(start_state[i])):
        # Do something here!
```
