# Imports
import random

import pygame as pg
from kogler.gui.button.button import Button
from datetime import datetime
from sys import exit
from math import pi, cos, sin


class Clock(object):
    # Constants
    #   Design - Color Guidelines

    #: Teal Color / Design Guideline
    CLR_SCHEMA_TEAL = {
        "bg": "#FAFAFA",
        "a-cl-bg": "#B2DFDB",
        "a-cl-bd": "#00796B",
        "a-cl-tick-cl": "#FAFAFA",
        "a-cl-center": "#004D40",
        "tick_min": 190,
        "tick_min_5": 180,
        "accent": "#263238",
        "accent2": "#78909C",
        "tick_min_15": 165
    }

    hc = (0,77,64)
    cc = (0,121,107)
    cfc = (250,250,250)

    BUTTON_STYLE = {"hover_color": hc,
                    "clicked_color": cc,
                    "clicked_font_color": cfc,
                    "hover_font_color": cfc
    }

    def __init__(self, size=(600, 800), clr_schema=CLR_SCHEMA_TEAL, time=datetime.now().time().strftime("%H:%M:%S")):
        """ Initialize all necessary attributes and elements

        Setting all Attributes
        Initialize drawing process

        :param size:
        :param clr_schema:
        """

        # Check parameter
        if type(size[0]) != int or type(size[1]) != int:
            raise TypeError("Incompatible types for size please use int instead of >>", type(size[0]), "<<")

        if clr_schema is not Clock.CLR_SCHEMA_TEAL:
            raise TypeError("Incompatible Colour design")

        # Set attributes and values
        self.size = size;
        self.width = size[0]
        self.height = size[1]
        self.center = self.Wcenter, self.Hcenter = int(size[0] / 2), int(size[1] / 2)
        self.schema = clr_schema;
        self.analog = True
        self.time = time
        self.radius = int(self.width / 3.0)
        self.mode = 0

        # Initialize pygame
        # Same outcome as initializing every module by itself
        # -> pygame.font.init()
        pg.init()
        # Set screen
        self.screen = pg.display.set_mode(size)

        self.screen_rect = self.screen.get_rect()
        self.button = Button((0, 0, 200, 50), self.cc, self.change_mode,
                             text="SHOW / HIDE INFO TEXT", **self.BUTTON_STYLE)
        self.button.rect.center = (self.screen_rect.centerx, 700)

        # Call Method responsible for drawing the content
        self.initiate_drawing()

    def change_mode(self):
        self.mode = 0 if self.mode == 1 else 1
        print("asd")

    def initiate_drawing(self):
        """ Initiate Drawing

        This method

        :return:
        """

        clock = pg.time.Clock()
        seconds = 0
        font = pg.font.Font(None, 36)
        pg.time.set_timer(pg.USEREVENT + 1, 1000)
        self.mode = 0;

        while 1:
            clock.tick(60)

            self.screen.fill(self.hex_to_rgb(self.schema.get("bg")))
            self.button.update(self.screen)
            if self.mode == 0:
                self.draw_clock()

            fps_display = font.render("FPS: " + str(clock.get_fps()), 1, (0, 0, 0))
            self.screen.blit(fps_display, (10, 60))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()
                elif event.type == pg.USEREVENT + 1:
                    seconds += 1
                self.button.check_event(event)

            pg.display.flip()

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def draw_clock(self):
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0 + 13), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0 + 8), 3)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bg")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-center")), (self.Wcenter, self.Hcenter),
                       int(8), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter), int(2), 0)
        for i in range(60):
            cl = self.hex_to_rgb(self.schema.get("bg"))
            if i % 15 == 0:
                length = self.schema.get("tick_min_15")
                thickness = 5
                cl = self.hex_to_rgb(self.schema.get("accent2"))
            elif i % 5 == 0:
                length = self.schema.get("tick_min_5")
                thickness = 8
            else:
                length = self.schema.get("tick_min")
                thickness = 3

            current_tick = self.calc_tick(i, length)
            pg.draw.line(self.screen, cl, current_tick.get("p1"), current_tick.get("p2"), thickness)

    def calc_tick(self, pos, length):
        angle = (360 * pos / 60) / 180 * pi
        return {
            "p1": (round(cos(angle) * self.radius + self.Wcenter), round(sin(angle) * self.radius + self.Hcenter)),
            "p2": (round(cos(angle) * length + self.Wcenter), round(sin(angle) * length + self.Hcenter))
        }


c = Clock()
