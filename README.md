C9753: Designing the Game of Life: Implementing Cellular Automata in Python 
===================

![Snowflake automata](http://i.imgur.com/WzSytPy.png?1)
[Source](http://psoup.math.wisc.edu/extras/hexca/hexca.html)

Feel free to leave the class at any time if you don’t find it interesting. You can attend a walk-in activity in Lobby 13, or change your schedule in 4-163.

This can be a slightly harder coding assignment than those offered at your high school. Don't feel frustrated if you don't get it at first. If you're stuck, just raise your hand, and I'll come over to help.

----------


Installation
-------------

 1. Open up a terminal and execute the following command: `git clone https://github.com/AnimatedRNG/splash-2015-conway.git`
 2. Execute `ls`. You should see a folder called `splash-2015-conway`. Execute the command `cd splash-2015-conway`.
 3. In this directory are multiple files, including this very README. Execute `alias python=python3`
 4. Now if you execute `python implementation.py` you should see a grid and three buttons. If you don't see a grid and three buttons or if you see an ugly error instead, raise your hand and I'll come over to help you. Either close the window with the grid in it, or type the key combination `Ctrl+C` into the terminal to end the program.
 5. I've been having some difficulties getting emacs and vi working on these machines; however, you can get a nice Python IDE up and running by executing `sudo apt-get install idle3`, typing in the espuser password (on the Google Slides screen), and pressing `y` to the `Do you want to continue?` prompt.
 6. Execute `idle3 implementation.py` in the terminal. You can now run your code by pressing `F5`. Happy Hacking!


Relevant Methods
-------------------------

While life_renderer.py has a lot of stuff in it, only four of them are publicly accessible.

From `LifeWindow` in `life_renderer.py`:
```python
    def create_cell(self, row = -1, col = -1, x = -1, y = -1):
        """Creates a cell at the specified row and column OR 
        (exclusive OR) at the position specified by (x, y).

        If the cell at the specified position is already alive,
        this function does nothing.


        Example:

        lifewindow.create_cell(row = 1, col = 2)
        lifewindow.create_cell(x = 2, y = 1)

        Both of the examples above create a cell at the same
        location.

        """
        self.__exec_cell__(lambda p: self.__render_cells__.add(p),
            row, col, x, y)


    def check_cell(self, row = -1, col = -1, x = -1, y = -1):
        """Determines whether the cell at the specified row and
        column OR (exclusive OR) at the position specified by (x, y)
        is alive.

        Returns True if a cell is found at the specified position
        otherwise False.

        Example:

        lifewindow.check_cell(row = 1, col = 2)
        lifewindow.check_cell(x = 2, y = 1)

        Both of the examples above check for a cell at the same
        location.

        """
        return self.__exec_cell__(lambda c: c in self.__render_cells__, row, col, x, y)


    def kill_cell(self, row = -1, col = -1, x = -1, y = -1):
        """Kills a cell at the specified row and column OR 
        (exclusive OR) at the position specified by (x, y).

        If there is no living cell at the specified position,
        this function does nothing.


        Example:

        lifewindow.kill_cell(row = 1, col = 2)
        lifewindow.kill_cell(x = 2, y = 1)

        Both of the examples above kill a cell at the same
        location.

        """

        self.__exec_cell__(lambda p: self.__render_cells__.remove(p),
            row, col, x, y)


    def clear_grid(self):
        """Kills all the cells on the grid."""

        self.__render_cells__ = set()

```

From `implementation.py`:
```python
def setup(lifewindow):
    """This callback runs prior to the start of the Game of Life.
    Put any initialization code in here.

    Any object returned from this method is ignored.

    """
    pass


def loop(lifewindow):
    """This callback runs on every iteration of the Game of Life.
    Implement the rules of the game here.

    Any object returned from this method is ignored.

    """
    pass
```

----------

Commonly asked Questions
--------

### (Row, Column) vs (x, y)

When I had to implement the Game of Life, I kept mixing up (Row, Column) with (x, y). So I decided to use the Pythonic convention of **Explicit over Implict** and encourage named arguments:

``` python
    lifewindow.create_cell(row = 0, col = 5)
```

This snippet of code creates a cell at row 0, column 5. I could do the same using (x, y) coordinates:

``` python
    lifewindow.create_cell(x = 5, y = 0)
```

But it makes no sense to mix the two:

``` python
    lifewindow.create_cell(y = 0, row = 5)
```

That's just weird. So **don't** do it. You'll get an exception.

### I wrote perfect code, but nothing happens!

The simulation starts out paused. Press the Pause button to unpause it.

### I get an exception about "Out of Range". How do I fix it?

Don't render cells outside the grid.

### I want a bigger grid

The first two parameters to the LifeWindow constructor are the number of rows and columns in the grid. You can change these numbers as you see fit

### Why does check_cell() say that there are already living cells at the beginning of loop()?

LifeWindow doesn't clear the grid after every iteration. If you created a cell during one iteration of loop(), it will remain there until you remove it.

### How do I make a 2D array in python?

Technically Python doesn't really have arrays, but it does have lists. A nice shortcut to creating a 2D list of `False`:

```python
array = [[False for y in range(DIM_2)] for x in range(DIM_1)] 
```

where `DIM_1` and `DIM_2` are the dimensions of your desired array.

### How do I make a set in python?

Clever you. Take a look at [this](https://docs.python.org/3/tutorial/datastructures.html#sets).
