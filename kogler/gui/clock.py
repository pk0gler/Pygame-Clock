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

    hc = (0, 77, 64)
    cc = (0, 121, 107)
    cfc = (250, 250, 250)

    BUTTON_STYLE_TEAL = {"hover_color": (0, 77, 64),
                         "clicked_color": (0, 121, 107),
                         "clicked_font_color": cfc,
                         "hover_font_color": cfc
                         }

    BUTTON_STYLE_BRWN = {"hover_color": (62,39,35),
                         "clicked_color": (93,64,55),
                         "clicked_font_color": cfc,
                         "hover_font_color": cfc
                         }

    BUTTON_STYLE_INDIGO = {"hover_color": (26,35,126),
                           "clicked_color": (48,63,159),
                           "clicked_font_color": cfc,
                           "hover_font_color": cfc
                           }

    BUTTON_STYLE_ORANGE = {"hover_color": (230,81,0),
                           "clicked_color": (245,124,0),
                           "clicked_font_color": cfc,
                           "hover_font_color": cfc
                           }

    def __init__(self, size=(600, 700), clr_schema=CLR_SCHEMA_TEAL, time=datetime.now().time().strftime("%H:%M:%S")):
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
        self.smooth = False
        self.startQuad_w = 0;
        self.startQuad_h = 0;

        # Initialize pygame
        # Same outcome as initializing every module by itself
        # -> pygame.font.init()
        pg.init()
        # Set screen
        self.screen = pg.display.set_mode(size)

        self.screen_rect = self.screen.get_rect()
        self.button = Button((self.Wcenter - 85, 615, 170, 50), self.cc, self.change_mode,
                             text="SHOW / HIDE INFO TEXT", **self.BUTTON_STYLE_TEAL)
        # self.button.rect.center = (self.screen_rect.centerx, 630)

        self.btn_cl_orange = Button((50, 615, 60, 50), self.BUTTON_STYLE_ORANGE.get("clicked_color"), self.set_o,
                                    text="Orange", **self.BUTTON_STYLE_ORANGE)
        self.btn_cl_indigo = Button((70 + 60, 615, 60, 50), self.BUTTON_STYLE_INDIGO.get("clicked_color"), self.set_i,
                                    text="Indigo", **self.BUTTON_STYLE_INDIGO)
        self.btn_cl_brown = Button((self.width - 50 - 60 - 20 - 60, 615, 60, 50), self.BUTTON_STYLE_BRWN.get("clicked_color"), self.set_b,
                                   text="Brown", **self.BUTTON_STYLE_BRWN)
        self.btn_cl_teal = Button((self.width - 50 - 60, 615, 60, 50), self.BUTTON_STYLE_TEAL.get("clicked_color"), self.set_t,
                                  text="Teal", **self.BUTTON_STYLE_TEAL)

        # self.button.rect.center = (self.screen_rect.centerx, 630)

        # Call Method responsible for drawing the content
        self.initiate_drawing()

    def set_o(self):
        self.schema = Clock.CLR_SCHEMA_ORANGE

    def set_t(self):
        self.schema = Clock.CLR_SCHEMA_TEAL

    def set_b(self):
        self.schema = Clock.CLR_SCHEMA_BROWN

    def set_i(self):
        self.schema = Clock.CLR_SCHEMA_INDIGO


    def change_mode(self):
        self.mode = 0 if self.mode == 1 else 1

    def initiate_drawing(self):
        """ Initiate Drawing

        This method

        :return:
        """

        clock = pg.time.Clock()
        self.seconds = 0
        font = pg.font.Font(None, 36)
        pg.time.set_timer(pg.USEREVENT + 1, 1000)
        self.mode = 0;

        while 1:
            self.change = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        exit()
                    elif event.key == pg.K_s:
                        self.smooth = not self.smooth
                    elif event.key == pg.K_d:
                        self.mode = 2
                    elif event.key == pg.K_a:
                        self.mode = 0
                    elif event.key == pg.K_h:
                        self.mode = 1
                elif event.type == pg.USEREVENT + 1:
                    self.change = True
                    self.seconds += 1

                self.button.check_event(event)
                self.btn_cl_orange.check_event(event)
                self.btn_cl_brown.check_event(event)
                self.btn_cl_indigo.check_event(event)
                self.btn_cl_teal.check_event(event)

            clock.tick()
            self.screen.fill(self.hex_to_rgb(self.schema.get("bg")))
            self.button.update(self.screen)
            self.btn_cl_orange.update(self.screen)
            self.btn_cl_brown.update(self.screen)
            self.btn_cl_teal.update(self.screen)
            self.btn_cl_indigo.update(self.screen)
            pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),(0,50,self.width,46))
            if self.mode == 0 and self.smooth is False:
                fps_display = font.render("ANALOG UHR", 1, self.cfc)
                self.screen.blit(fps_display, (20, 60))
                self.draw_clock()
                self.draw_min_hand()
                self.draw_sec_hand()
                self.draw_std_hand()
                pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("bg")), (self.Wcenter, self.Hcenter),
                               int(2), 0)
            elif self.mode == 0 and self.smooth is True:
                fps_display = font.render("ANALOG UHR", 1, self.cfc)
                self.screen.blit(fps_display, (20, 60))
                self.draw_clock()
                self.draw_min_hand_smooth()
                self.draw_sec_hand_smooth()
                self.draw_std_hand()
                pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("bg")), (self.Wcenter, self.Hcenter),
                               int(2), 0)
                self.screen.blit(fps_display, (20, 60))

            elif self.mode == 1:
                fps_display = font.render("HELP SCREEN", 1, self.cfc)
                self.screen.blit(fps_display, (20, 60))
                self.draw_help()

            elif self.mode == 2:
                fps_display = font.render("DIGITAL UHR", 1, self.cfc)
                self.screen.blit(fps_display, (20, 60))
                self.draw_clock_dig()
            fps = "FPS: " + str(clock.get_fps())
            fps_display = font.render(fps[:7], 1, self.cfc)
            self.screen.blit(fps_display, (self.width-120, 60))

            pg.display.flip()

    @staticmethod
    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def draw_clock_dig(self):
        font = pg.font.Font(None, 85)
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),(self.Wcenter-self.radius,self.Hcenter-self.radius/2,self.radius*2,self.radius))
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("accent")),(self.Wcenter-self.radius+15,self.Hcenter-self.radius/2+15,self.radius*2-30,self.radius-30),3)
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("accent2")),(self.Wcenter-self.radius,self.Hcenter-self.radius/2,self.radius*2,self.radius),3)
        fps_display = font.render(datetime.now().time().strftime("%H : %M : %S"), 1, self.cfc)
        self.screen.blit(fps_display, (self.Wcenter-self.radius+50, self.Hcenter-30))

    def draw_help(self):
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("accent")), (
            self.Wcenter - (self.Wcenter - 50) / 2, self.Hcenter - (self.Hcenter - 120) / 2, self.Wcenter - 50,
            self.Hcenter - 120), 14)
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")), (
            self.Wcenter - (self.Wcenter - 43) / 2, self.Hcenter - (self.Hcenter - 115) / 2, self.Wcenter - 43,
            self.Hcenter - 115), 5)

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

        temp = self.schema;

        self.schema = Clock.CLR_SCHEMA_TEAL
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50, 10, 10))
        self.schema = Clock.CLR_SCHEMA_INDIGO
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50 + 15, 10, 10))
        self.schema = Clock.CLR_SCHEMA_BROWN
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50 + 30, 10, 10))
        self.schema = Clock.CLR_SCHEMA_ORANGE
        pg.draw.rect(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")),
                     ((self.Wcenter - (self.Wcenter - 43) / 2) + 20 + self.startQuad_w,
                      (self.Hcenter - (self.Hcenter - 115) / 2) + 65 + 50 + 50 + 45, 10, 10))

        self.schema = temp

        # print(int(datetime.now().time().microsecond / 1000)/1000)

        if self.change is True:
            print("drin")
            if self.startQuad_w < 190:
                self.startQuad_w += 15
            elif self.startQuad_h < 30:
                self.startQuad_w = 0

    def draw_sec_hand(self):
        pg.draw.line(self.screen, (183,28,28), (self.Wcenter, self.Hcenter),
                     self.calc_sec_pos(), 2)

    def draw_sec_hand_smooth(self):
        pg.draw.line(self.screen, (183,28,28), (self.Wcenter, self.Hcenter),
                     self.calc_sec_pos_smooth(), 2)

    def draw_min_hand(self):
        pg.draw.line(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                     self.calc_min_pos(), 5)

    def draw_min_hand_smooth(self):
        pg.draw.line(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                     self.calc_min_pos_smooth(), 5)

    def draw_std_hand(self):
        pg.draw.line(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                     self.calc_std_pos(), 9)

    def draw_clock(self):
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bd")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0 + 13), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("accent")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0 + 8), 3)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-bg")), (self.Wcenter, self.Hcenter),
                       int(self.width / 3.0), 0)
        pg.draw.circle(self.screen, self.hex_to_rgb(self.schema.get("a-cl-center")), (self.Wcenter, self.Hcenter),
                       int(8), 0)
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

    def calc_sec_pos(self):
        sec = int(datetime.now().time().strftime("%S"))
        angle = (360 * (sec - 15) / 60) / 180 * pi
        temp = (round(cos(angle) * self.radius + self.Wcenter), round(sin(angle) * self.radius + self.Hcenter))
        return temp
        # return (self.Wcenter, self.Hcenter-self.radius)

    def calc_sec_pos_smooth(self):
        milli = int(datetime.now().time().microsecond / 1000)
        sec = int(datetime.now().time().strftime("%S")) + milli / 1000
        angle = (360 * (sec - 15) / 60) / 180 * pi
        temp = (round(cos(angle) * self.radius + self.Wcenter), round(sin(angle) * self.radius + self.Hcenter))
        return temp
        # return (self.Wcenter, self.Hcenter-self.radius)

    def calc_min_pos_smooth(self):
        """milli = int(datetime.now().time().microsecond / 1000)
        sec = int(datetime.now().time().strftime("%S")) + milli / 1000
        min = int(datetime.now().time().strftime("%S")) + (sec /100)
        print(min)
        angle = (360 * (min - 15) / 60) / 180 * pi
        temp = (round(cos(angle) * self.radius + self.Wcenter), round(sin(angle) * 160 + self.Hcenter))
        return temp
        # return (self.Wcenter, self.Hcenter-self.radius)"""
        return self.calc_min_pos()

    def calc_min_pos(self):
        mi = int(datetime.now().time().strftime("%M"))
        angle = (360 * (mi - 15) / 60) / 180 * pi
        return round(cos(angle) * 160 + self.Wcenter), round(sin(angle) * 160 + self.Hcenter)

    def calc_std_pos(self):
        st = int(datetime.now().time().strftime("%H"))
        angle = (360 * (st - 15) * 5 / 60) / 180 * pi
        return round(cos(angle) * 125 + self.Wcenter), round(sin(angle) * 125 + self.Hcenter)


c = Clock()
