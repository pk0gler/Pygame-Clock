from kogler.gui.clock import Clock
from datetime import datetime

class Controller(object):

    def __init__(self, size=(600, 700), clr_schema=Clock.CLR_SCHEMA_TEAL, time=datetime.now().time().strftime("%H:%M:%S")):
        