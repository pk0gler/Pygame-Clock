"""
This Module represents the logical Controller of the Simple Game.
Its main purpose is the creation of View and Model as well as connecting
those components in one single Application
"""

from datetime import datetime

import pygame as pg

from kogler.button import Button
from kogler.clock_view import View


class Controller(object):
    """ Creates the ClockController for the (M)VC - Application

    This class acts as the MainController for all interactions with
    the MainView.
    It connects the View with the Model

    - **Included Functions**
        Following Functions and methods can be invoked

        *init - Method*
        :func:`__init__`

        *game_start_game_loop - Method*
        :func:`start_game_loop`

        *initiate_buttons - Method*
        :func:`initiate_buttons`

        *change_mode - Method*
        :func:`change_mode`

    """
    def __init__(self, size=(600, 700), schema=View.CLR_SCHEMA_TEAL, time=datetime.now().time().strftime("%H:%M:%S"),mode=0):
        """ init - Method

        This Method initializes all Attributes and verifies ist
        values and types

        :param tuple size: width, height as inz
        :param dict schema: schema according to guidelines in clock_view
        :param str time: optional time setting
        :param int mode: int start mode
        """

        # Check parameter
        if type(size[0]) != int or type(size[1]) != int:
            raise TypeError("Incompatible types for size please use int instead of >>", type(size[0]), "<<")

        if schema is not View.CLR_SCHEMA_TEAL:
            raise TypeError("Incompatible Colour design")

        # Set specified Attributes
        self.size = self.width,self.height = size[0], size[1]
        self.schema = schema
        self.mode = mode
        # Initialize pygame
        # Same outcome as initializing every module by itself
        # -> pygame.font.init()
        pg.init()
        # Set screen
        self.screen = pg.display.set_mode(size)
        # initialize the view
        self.clock_view = View(self.schema, self.screen, self.size)

        # initiate buttons
        self.initiate_buttons()

        # Start game / main loop
        self.start_game_loop()

    def start_game_loop(self):
        """ Initiate Drawing

        This method intiates the game loop
        It will act according to the current mode and will invoke
        the necessary methods of the view

        """

        clock = pg.time.Clock()
        self.seconds = 0
        pg.time.set_timer(pg.USEREVENT + 1, 1000)
        smooth = False

        while 1:
            self.change = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()
                    elif event.key == pg.K_a:
                        self.mode = 0
                    elif event.key == pg.K_d:
                        self.mode = 1
                    elif event.key == pg.K_h:
                        self.mode = 2
                    elif event.key == pg.K_s:
                        smooth = not smooth
                elif event.type == pg.USEREVENT + 1:
                    self.change = True
                    self.seconds += 1

                self.button.check_event(event)
                self.btn_cl_orange.check_event(event)
                self.btn_cl_brown.check_event(event)
                self.btn_cl_indigo.check_event(event)
                self.btn_cl_teal.check_event(event)

            # lock fps to 120
            clock.tick(120)

            self.clock_view.update_view(clock)

            self.button.update(self.screen)
            self.btn_cl_orange.update(self.screen)
            self.btn_cl_brown.update(self.screen)
            self.btn_cl_teal.update(self.screen)
            self.btn_cl_indigo.update(self.screen)

            # switch between modes
            if self.mode == 0:
                self.clock_view.show_analog_clock(smooth)
            elif self.mode == 1:
                self.clock_view.show_digital_clock()
            elif self.mode == 2:
                self.clock_view.show_help(self.change)

            pg.display.flip()

    def initiate_buttons(self):
        """ Initiate Buttons

        Initiate Buttons for later use
        Setting position and passing necessary function which will be called
        later on in the process

        """
        self.button = Button((self.width/2 - 85, 615, 170, 50), View.hex_to_rgb(View.CLR_SCHEMA_TEAL.get("a-cl-bd")), self.change_mode,
                             text="SHOW / HIDE INFO TEXT", **View.BUTTON_STYLE_TEAL)
        self.btn_cl_orange = Button((50, 615, 60, 50), View.BUTTON_STYLE_ORANGE.get("clicked_color"), self.set_o,
                                    text="Orange", **View.BUTTON_STYLE_ORANGE)
        self.btn_cl_indigo = Button((70 + 60, 615, 60, 50), View.BUTTON_STYLE_INDIGO.get("clicked_color"), self.set_i,
                                    text="Indigo", **View.BUTTON_STYLE_INDIGO)
        self.btn_cl_brown = Button((self.width - 50 - 60 - 20 - 60, 615, 60, 50),
                                   View.BUTTON_STYLE_BRWN.get("clicked_color"), self.set_b,
                                   text="Brown", **View.BUTTON_STYLE_BRWN)
        self.btn_cl_teal = Button((self.width - 50 - 60, 615, 60, 50), View.BUTTON_STYLE_TEAL.get("clicked_color"),
                                  self.set_t,
                                  text="Teal", **View.BUTTON_STYLE_TEAL)

    # Help Methods for Buttons class
    def set_o(self):
        """ Set Colours available

        """
        self.schema = View.CLR_SCHEMA_ORANGE
        self.clock_view.schema = self.schema

    def set_t(self):
        self.schema = View.CLR_SCHEMA_TEAL
        self.clock_view.schema = self.schema

    def set_b(self):
        self.schema = View.CLR_SCHEMA_BROWN
        self.clock_view.schema = self.schema

    def set_i(self):
        self.schema = View.CLR_SCHEMA_INDIGO
        self.clock_view.schema = self.schema

    def change_mode(self):
        """ Change Mode

        Modes:
            - 1: Analog Clock
            - 2: Digital Clock
            - 3: Help Window

        """
        self.mode = 0 if self.mode == 2 else 2

if __name__ == "__main__":
    c = Controller()