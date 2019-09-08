import wx
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
import matplotlib.cm as cm


class DicomFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        # FIXME: why here the super() function doesn't work to call superclass init maethod.
        # super().__init__(self, *args, **kwargs)
        wx.Frame.__init__(self, *args, **kwargs)

        self.createCanavs(self)
        self.createInputs(self)

        # place them in a sizer for the layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.input_panel, 1, wx.EXPAND)
        sizer.Add(self.canvas, 4, wx.EXPAND)
        self.SetSizerAndFit(sizer)

    def createInputs(self, parent):
        self.input_panel = wx.Panel(parent)
        self.input_panel.SetBackgroundColour(wx.Colour("light coral"))
        self.coordinates = wx.StaticText(self.input_panel, label="Center Coordinate")

    def createCanavs(self, parent):
        self.figure = Figure()
        self.canvas = FigureCanvasWxAgg(parent, -1, self.figure)
        # Event callback binding for matplotlib
        # TODO
        self.canvas.draw()
        self.createPlots()

    def createPlots(self):
        delta = 0.025
        steps = np.arange(-3, 3, delta)
        x, y = np.meshgrid(steps, steps)
        z2 = np.exp(-(x - 1) ** 2 - (y - 1) ** 2)
        z1 = np.exp(-x ** 2 - y ** 2)
        z = (z1 - z2) * 2
        ax = self.figure.add_subplot(111)
        im = ax.imshow(z, interpolation='bilinear', cmap=cm.RdYlGn,
                       origin='lower', extent=[-3, 3, -3, 3],
                       vmax=abs(z).max(), vmin=-abs(z).max())


class MyApp(wx.App):
    def OnInit(self):
        self.frame = DicomFrame(parent=None, title="Dicom Viewer", size=(640, 480))
        self.frame.Show()
        return True


if __name__ == "__main__":
    app = MyApp()
    app.MainLoop()
