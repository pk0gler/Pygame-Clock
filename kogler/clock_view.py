"""
This Module represents the View of the Simple Game.
Its main purpose is the creation of View and Model as well as connecting
those components in one single Application
"""

from datetime import datetime
from math import cos, sin, pi

import pygame as pg


class View(object):
    """ View for setting up the Clocks Look and Feel

    Responsible for setting up pygames view components

    """
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

    #: Indigo Color / Design Guideline
    CLR_SCHEMA_INDIGO = {
        "bg": "#FAFAFA",
        "a-cl-bg": "#C5CAE9",
        "a-cl-bd": "#303F9F",
        "a-cl-tick-cl": "#FAFAFA",
        "a-cl-center": "#1A237E",
        "tick_min": 190,
        "tick_min_5": 180,
        "accent": "#DD2C00",
        "accent2": "#FF6E40",
        "tick_min_15": 165
    }

    #: Indigo Color / Design Guideline
    CLR_SCHEMA_BROWN = {
        "bg": "#FAFAFA",
        "a-cl-bg": "#BCAAA4",
        "a-cl-bd": "#5D4037",
        "a-cl-tick-cl": "#FAFAFA",
        "a-cl-center": "#3E2723",
        "tick_min": 190,
        "tick_min_5": 180,
        "accent": "#827717",
        "accent2": "#CDDC39",
        "tick_min_15": 165
    }

    #: Indigo Color / Design Guideline
    CLR_SCHEMA_ORANGE = {
        "bg": "#FAFAFA",
        "a-cl-bg": "#FFCC80",
        "a-cl-bd": "#F57C00",
        "a-cl-tick-cl": "#FAFAFA",
        "a-cl-center": "#E65100",
        "tick_min": 190,
        "tick_min_5": 180,
        "accent": "#1B5E20",
        "accent2": "#4CAF50",
        "tick_min_15": 165
    }

    #: BTN Teal
    BUTTON_STYLE_TEAL = {"hover_color": (0, 77, 64),
                         "clicked_color": (0, 121, 107),
                         "clicked_font_color": (250, 250, 250),
                         "hover_font_color": (250, 250, 250)
                         }

    #: BTN Brown
    BUTTON_STYLE_BRWN = {"hover_color": (62, 39, 35),
                         "clicked_color": (93, 64, 55),
                         "clicked_font_color": (250, 250, 250),
                         "hover_font_color": (250, 250, 250)
                         }

    #: BTN Indigio
    BUTTON_STYLE_INDIGO = {"hover_color": (26, 35, 126),
                           "clicked_color": (48, 63, 159),
                           "clicked_font_color": (250, 250, 250),
                           "hover_font_color": (250, 250, 250)
                           }

    #: BTN Orange
    BUTTON_STYLE_ORANGE = {"hover_color": (230, 81, 0),
                           "clicked_color": (245, 124, 0),
                           "clicked_font_color": (250, 250, 250),
                           "hover_font_color": (250, 250, 250)
                           }

    def __init__(self, schema, screen, size):
        """ init Method

        Sets all necessary Attributes

        :param dict schema:
        :param pygame.screen screen:
        :param tuple size:
        """
        self.schema = schema
        self.screen = screen
        self.size = self.width, self.height = size[0], size[1]
        self.center = self.Wcenter, self.Hcenter = int(size[0] / 2), int(size[1] / 2)
        self.radius = int(self.width / 3.0)
        self.startQuad_w = 0
        self.startQuad_h = 0

    @staticmethod
    def hex_to_rgb(value):
        """ Converts a hex to a rgb tuple

        :param str value: passed hex
        :return: RGB Tuple
        :rtype: tuple
        """
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def update_view(self, clock):
        """ Update View

        Updates the View
        all static components which wont be effected by the view

        :param pygame.clock clock:
        """
        # Draw static Objects / Always the same Position
        self.screen.fill(self.hex_to_rgb(self.schema.get("bg")))
        # static header
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")), (0, 50, self.width, 46))
        # draw fps to top right corner
        fps = "FPS: " + str(clock.get_fps())
        fps_display = pg.font.Font(None, 36).render(fps[:8], 1, self.hex_to_rgb(self.schema.get("bg")))
        self.screen.blit(fps_display, (self.width - 120, 60))

    def show_analog_clock(self, smooth=False):
        """ Show analog Clock

        Shows the analog clock with
        all necessary components

        :param bool smooth: if smooth or not
        """
        # static text for analog clock mode
        text = "ANALOG UHR" if not smooth else "ANALOG UHR SMOOTH"
        fps_display = pg.font.Font(None, 36).render(text, 1, self.hex_to_rgb(self.schema.get("bg")))
        self.screen.blit(fps_display, (20, 60))
        # draw clock body
        self.draw_clock_body()
        # draw the hands
        self.draw_hands(smooth)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("bg")), (self.Wcenter, self.Hcenter),
                       int(2), 0)

    def show_digital_clock(self):
        """ Show difital clock

        """
        # static text for analog clock mode
        text = "DIGITAL CLOCK"
        fps_display = pg.font.Font(None, 36).render(text, 1, self.hex_to_rgb(self.schema.get("bg")))
        self.screen.blit(fps_display, (20, 60))
        # Clock Body
        font = pg.font.Font(None, 85)
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     (self.Wcenter - self.radius, self.Hcenter - self.radius / 2, self.radius * 2, self.radius))
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("accent")), (
            self.Wcenter - self.radius + 15, self.Hcenter - self.radius / 2 + 15, self.radius * 2 - 30,
            self.radius - 30),
                     3)
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("accent2")),
                     (self.Wcenter - self.radius, self.Hcenter - self.radius / 2, self.radius * 2, self.radius), 3)
        fps_display = font.render(datetime.now().time().strftime("%H : %M : %S"), 1, View.hex_to_rgb(self.schema.get("bg")))
        self.screen.blit(fps_display, (self.Wcenter - self.radius + 50, self.Hcenter - 30))

    def show_help(self, change):
        """ Show help

        :param bool change: for moving the tiles
        """
        # static text for analog clock mode
        text = "HELP TEXT"
        fps_display = pg.font.Font(None, 36).render(text, 1, self.hex_to_rgb(self.schema.get("bg")))
        self.screen.blit(fps_display, (20, 60))
        # help body
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("accent")), (
            self.Wcenter - (self.Wcenter - 50) / 2, self.Hcenter - (self.Hcenter - 120) / 2, self.Wcenter - 50,
            self.Hcenter - 80), 14)
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")), (
            self.Wcenter - (self.Wcenter - 43) / 2, self.Hcenter - (self.Hcenter - 115) / 2, self.Wcenter - 43,
            self.Hcenter - 75), 5)

        font = pg.font.Font(None, 26)

        self.screen.blit(font.render(" K E Y S / C O N T R O L S", 1, (0, 0, 0)), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 20, (self.Hcenter - (self.Hcenter - 115) / 2) + 20))
        self.screen.blit(font.render("- - - - - - - - - - - - - - - - - - - -", 1, (0, 0, 0)), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 20, (self.Hcenter - (self.Hcenter - 115) / 2) + 40))
        self.screen.blit(font.render("A . . . Analog Clock", 1, self.hex_to_rgb(self.schema.get("a-cl-bd"))), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 28, (self.Hcenter - (self.Hcenter - 115) / 2) + 65))
        self.screen.blit(font.render("D . . . Digital Clock", 1, self.hex_to_rgb(self.schema.get("a-cl-bd"))), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 28, (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 25))
        self.screen.blit(font.render("S . . . Toggle Smooth", 1, self.hex_to_rgb(self.schema.get("a-cl-bd"))), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 28, (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50))
        self.screen.blit(font.render("- - - - - - - - - - - - - - - - - - - -", 1, (0, 0, 0)), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 20, (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 30))

        temp = self.schema

        self.screen.blit(font.render("AVAILABLE / C O L O R S", 1, (0, 0, 0)), (
            (self.Wcenter - (self.Wcenter - 43) / 2) + 20, (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 55))

        self.schema = View.CLR_SCHEMA_TEAL
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50+35, 10, 10))
        self.schema = View.CLR_SCHEMA_INDIGO
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50 + 15 + 35, 10, 10))
        self.schema = View.CLR_SCHEMA_BROWN
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50 + 30 + 35, 10, 10))
        self.schema = View.CLR_SCHEMA_ORANGE
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50 + 45 + 35, 10, 10))

        self.schema = temp

        if change is True:
            if self.startQuad_w < 190:
                self.startQuad_w += 15
            elif self.startQuad_h < 30:
                self.startQuad_w = 0

    def draw_clock_body(self):
        """ Draw Clock Body

        """
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0 + 13), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0 + 8), 3)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bg")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-center")), (self.Wcenter, self.Hcenter),
                       int(8), 0)

        count = 0
        for i in range(0,360,6):
            rad = i / 180 * pi
            cl = self.hex_to_rgb(self.schema.get("bg"))

            if count % 15 == 0:
                length = self.schema.get("tick_min_15")
                thickness = 5
                cl = self.hex_to_rgb(self.schema.get("accent2"))
            elif count % 5 == 0:
                length = self.schema.get("tick_min_5")
                thickness = 8
            else:
                length = self.schema.get("tick_min")
                thickness = 3

            p1 = round(cos(rad) * self.radius + self.Wcenter), round(sin(rad) * self.radius + self.Hcenter)
            p2 = round(cos(rad) * length + self.Wcenter), round(sin(rad) * length + self.Hcenter)
            pg.draw.line(self.screen, cl, p1, p2, thickness)
            count += 1

    def draw_hands(self, smooth=False):
        """ Draw Hands

        If smooth it will be smooth

        :param bool smooth: is true its smooth
        """
        # sec hand
        pg.draw.line(self.screen, (183, 28, 28), (self.Wcenter, self.Hcenter),
                     self.calc_pos("%S", self.radius, smooth), 2)
        # min hand
        pg.draw.line(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                     self.calc_pos("%M", 160, smooth), 5)

        # std hadn
        pg.draw.line(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                     self.calc_pos("%H", 125, smooth), 9)

    def calc_pos(self, time_format, size=0, smooth=False):
        """ Calc Tic Pos

        Calcs the pos for the specified tic

        :param str time_format: bsp.: "%S", "%H"
        :param int size: size
        :param bool smooth: if smooth
        :return: tuple
        """
        if smooth is False:
            time = int(datetime.now().time().strftime(time_format))
            if time_format == "%H":
                angle = (360 * (time - 15) * 5 / 60) / 180 * pi
            else:
                angle = (360 * (time - 15) / 60) / 180 * pi
            return round(cos(angle) * size + self.Wcenter), round(sin(angle) * size + self.Hcenter)
        elif time_format == "%S":
            milli = int(datetime.now().time().microsecond / 1000)
            sec = int(datetime.now().time().strftime("%S")) + milli / 1000
            angle = (360 * (sec - 15) / 60) / 180 * pi
            temp = (round(cos(angle) * self.radius + self.Wcenter), round(sin(angle) * self.radius + self.Hcenter))
            return temp
        elif time_format == "%M":
            sec = int(datetime.now().time().strftime("%S"))
            temp = sec / 60
            mi = int(datetime.now().time().strftime("%M"))
            angle = (360 * (mi + temp - 15) / 60) / 180 * pi
            return round(cos(angle) * 160 + self.Wcenter), round(sin(angle) * 160 + self.Hcenter)
        elif time_format == "%H":
            mi = int(datetime.now().time().strftime("%M"))
            temp = mi / 60
            st = int(datetime.now().time().strftime("%H"))
            angle = (360 * (st + temp - 15) * 5 / 60) / 180 * pi
            return round(cos(angle) * 125 + self.Wcenter), round(sin(angle) * 125 + self.Hcenter)