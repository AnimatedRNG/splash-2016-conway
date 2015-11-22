import pyglet
from pyglet import pyglet_gui
from pyglet.pyglet_gui.theme.theme import Theme
from pyglet.pyglet_gui.manager import Manager
from pyglet.pyglet_gui.mixins import HighlightMixin
from pyglet.pyglet_gui.buttons import Button
from pyglet.pyglet_gui.containers import Container
from pyglet.pyglet_gui.gui import Label
from pyglet.gl import *

FONT_SIZE_NORMAL = 20
FONT_SIZE_SMALL = 12
HEIGHT_RATIO = 0.5
WIDTH_RATIO = 0.5
GRID_RATIO = 9/10
LINE_THICKNESS = 3.0
NUM_BUTTONS = 6
RESET_BUTTON_PAUSE = 1 / 5
FRAMERATE = 60
SPEED = 1


""" https://github.com/jorgecarleitao/pyglet-gui/blob/master/examples/button_highlight.py """
class HighlightedButton(Button, HighlightMixin):
    """
    An example of a Button that changes behavior when is mouse-hovered.
    We mix the behavior of button with HighlightMixin.
    """
    def __init__(self, text, is_pressed=False, on_press=None):
        Button.__init__(self, text, is_pressed, on_press)
        HighlightMixin.__init__(self)

    def load_graphics(self):
        super().load_graphics()
        HighlightMixin.load_graphics(self)

    def layout(self):
        super().layout()
        HighlightMixin.layout(self)

    def unload_graphics(self):
        Button.unload_graphics(self)
        HighlightMixin.unload_graphics(self)


class LifeWindow(pyglet.window.Window):


    def __init__(self, rows, cols, setup=None, loop=None):
        screen_res = self.__get_square_screen_size__()
        self.rows, self.cols = rows, cols
        self.__generation_count__ = 0
        self.__grid_width__ = int(screen_res[0] * WIDTH_RATIO)
        self.__grid_height__ = int(screen_res[1] * HEIGHT_RATIO)
        self.__paused__ = False
        self.__game_paused__ = False
        self.__render_cells__ = set()
        
        self.theme = Theme({
                  "font": "Lucida Grande",
                  "font_size": int((FONT_SIZE_NORMAL / 1280) * int(screen_res[0])),
                  "font_size_small": int(FONT_SIZE_SMALL / 1280) * int(screen_res[0]),
                  "gui_color": [255, 255, 255, 255],
                  "disabled_color": [160, 160, 160, 255],
                  "text_color": [255, 255, 255, 255],
                  "highlight_color": [255, 255, 255, 64],
                  "button": {
                      "down": {
                          "highlight": {
                              "image": {
                                  "source": "button-highlight.png",
                                  "frame": [8, 6, 2, 2],
                                  "padding": [18, 18, 8, 6]
                              }
                          },
                          "image": {
                              "source": "button-down.png",
                              "frame": [6, 6, 3, 3],
                              "padding": [12, 12, 4, 2]
                          },
                          "text_color": [0, 0, 0, 255]
                      },
                      "up": {
                          "highlight": {
                              "image": {
                                  "source": "button-highlight.png",
                                  "frame": [8, 6, 2, 2],
                                  "padding": [18, 18, 8, 6]
                              }
                          },
                          "image": {
                              "source": "button.png",
                              "frame": [6, 6, 3, 3],
                              "padding": [12, 12, 4, 2]
                          }
                      }
                  }}, resources_path='assets/')

        super(LifeWindow, self).__init__(
            self.__grid_width__, int((1/GRID_RATIO) * self.__grid_height__))
        self.set_caption("Conway\'s Game of Life")

        self.setup = setup
        if self.setup != None:
            self.setup(self)

        self.loop = loop
        pyglet.clock.schedule_once(self.on_logic, SPEED)

        def on_press_play(is_pressed):
            self.__game_paused__ = not self.__game_paused__
            if self.__game_paused__ == False:
                pyglet.clock.schedule_once(self.on_logic, SPEED)


        def on_press_reset(is_pressed):
            pyglet.clock.schedule_once(self.__reset_button__, RESET_BUTTON_PAUSE, self.reset)
            self.clear_grid()
            if self.setup != None:
                self.setup(self)

        def on_press_step(is_pressed):
            pyglet.clock.schedule_once(self.__reset_button__, RESET_BUTTON_PAUSE, self.step)
            self.on_logic()

        self.play = HighlightedButton('Pause', on_press = on_press_play)
        self.reset = HighlightedButton('Reset', on_press = on_press_reset)
        self.step = HighlightedButton('Step', on_press = on_press_step)
        self.generation = Label(str(self.__generation_count__))
        self.button_container = Container(content=[self.play, self.reset, self.step, self.generation])
        self.batch = pyglet.graphics.Batch()

        Manager(self.button_container, window = self, theme = self.theme, batch = self.batch)

        pyglet.clock.schedule_interval(self.on_draw, 1 / FRAMERATE)

        pyglet.app.run()


    def on_logic(self, dt = SPEED):
        if self.loop != None:
            self.loop(self)
        self.__generation_count__ += 1
        if not self.__game_paused__:
            pyglet.clock.schedule_once(self.on_logic, SPEED)


    def on_draw(self, dt = 1 / FRAMERATE):
        if not self.__paused__:
            glClearColor(0.129, 0.129, 0.129, 1.0)
            self.clear()
            for cell in self.__render_cells__:
                self.__draw_cell__(cell[0], cell[1], (1.0, 0.671, 0.569))
            self.__draw_grid__((.12, 0.59, 0.95))
            self.__draw_toolbar__()
            self.batch.draw()


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
        return self.__exec_cell__(lambda c: c in self.__render_cells__, \
            row, col, x, y)


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


    def __draw_toolbar__(self):
        bottom_toolbar = self.__grid_height__
        top_toolbar = self.height
        padding = 9
        padded_bottom = bottom_toolbar + padding
        padded_top = top_toolbar - padding
        padded_left = padding
        padded_right = self.width - padding

        width = (padded_right - padded_left - padding * 2) // NUM_BUTTONS

        # left, top, right, bottom
        button_boundaries = lambda n: (n * (width) + padded_left + padding, \
            padded_top - padding, (n + 1) * (width) + padded_left - padding, \
            padded_bottom + padding)

        self.__draw_rectangle__(0, top_toolbar, self.width, bottom_toolbar, \
            (1., 1., 1.))
        self.__draw_rectangle__(padded_left, padded_top, padded_right, \
            padded_bottom, (0.506, 0.78, 0.518))


        def render_buttons(buttons):
            for button_index in range(len(buttons)):
                bound = button_boundaries(button_index)
                self.__draw_rectangle__(bound[0], bound[1], bound[2], bound[3], \
                    (1., 1., 1.))

                buttons[button_index].set_position(bound[0], bound[3])
                buttons[button_index].width = bound[2] - bound[0]
                buttons[button_index].height = bound[1] - bound[3]

        render_buttons([self.play, self.reset, self.step])
        self.generation.set_text(str(self.__generation_count__))


    def __reset_button__(self, dt, button):
        self.reset._is_pressed = False
        self.reset.reload()

    def __exec_cell__(self, func, row = -1, col = -1, x = -1, y = -1):
        bad_arguments = lambda a, b, c, d: True if a < 0 or a > c or b < 0 or b > d else False
        if row == -1 and col == -1 and x == -1 and y == -1:
            raise ValueError("Please specify a position")
        elif (row == -1 and col == -1) or (x == -1 and y == -1):
            if row == -1 and col == -1:
                if bad_arguments(y, x, self.rows, self.cols):
                    raise ValueError('Position {} was out of range'.format((x, y)))
                return func((y, x))
            else:
                if bad_arguments(row, col, self.rows, self.cols):
                    raise ValueError('Position {} was out of range'.format((row, col)))
                return func((row, col))
        else:
            raise ValueError('Either give the position in (x, y) OR (row, col) but NOT both')


    def __draw_grid__(self, color):
        for i in range(0, self.__grid_width__, int(self.__grid_width__ / self.cols)):
            self.__draw_line__(i, 0, i, self.__grid_height__, color, LINE_THICKNESS)
        for j in range(0, self.__grid_height__, int(self.__grid_height__ / self.rows)):
            self.__draw_line__(0, j, self.__grid_width__, j, color, LINE_THICKNESS)


    def __draw_cell__(self, row, col, color):
        dx, dy = (self.__grid_width__ // self.cols), (self.__grid_height__ // self.rows)
        x1, y1, x2, y2 = dx * col, dy * row, \
             dx * (col + 1), dy * (row + 1)
        self.__draw_rectangle__(x1, y1, x2, y2, color)


    def __draw_rectangle__(self, x1, y1, x2, y2, color):
        pyglet.graphics.draw(4, GL_QUADS,
            ('v2i', (x1, y1, x1, y2, x2, y2, x2, y1)),
            ('c3f', color * 4))


    def __draw_pixel__(self, x, y, color):
        pyglet.graphics.draw(1, GL_POINTS,
            ('v2i', (x, y)),
            ('c3B', (color[0], color[1], color[2])))


    def __draw_line__(self, x1, y1, x2, y2, color, width = 1.0):
        glLineWidth(width)
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
            ('v2i', (x1, y1, x2, y2)), ('c3f', color * 2))


    def __draw_error__(self, error_string):
        self.paused = True
        print(error_string)


    def __get_screen_size__(self):
        screen = pyglet.window.Platform().get_default_display(). \
            get_default_screen()
        return (screen.width, screen.height)


    def __get_square_screen_size__(self):
        size = self.__get_screen_size__()
        s = min(size[0], size[1])
        return (s, s)


if __name__ == "__main__":
    window = LifeWindow(10, 10)