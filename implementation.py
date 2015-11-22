#!/usr/bin/python3

from life_renderer import LifeWindow


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


LifeWindow(10, 10, setup = setup, loop = loop)
