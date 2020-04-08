import matplotlib

matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.figure import Figure

import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, id, trial_values, outsider_points, channel_number, trial_number, channel_mean,
                 channel_std_der, y_min, y_max, stdX):
        wx.Frame.__init__(self, parent, id, 'scrollable plot',
                          style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER,
                          size=(800, 400))
        self.panel = wx.Panel(self, -1)

        self.fig = Figure((5, 4), 75)
        self.canvas = FigureCanvasWxAgg(self.panel, -1, self.fig)

        self.scroll_range = len(trial_values)
        self.canvas.SetScrollbar(wx.HORIZONTAL, 0, 5,
                                 self.scroll_range)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, -1, wx.EXPAND)

        self.panel.SetSizer(sizer)
        self.panel.Fit()

        self.outsider_points = outsider_points
        self.bursts_x = list(map(lambda x: x[0], self.outsider_points))
        self.bursts_y = list(map(lambda x: x[1], self.outsider_points))
        self.stdX = stdX
        self.y_min = y_min
        self.y_max = y_max
        self.channel_mean = channel_mean
        self.channel_std_der = channel_std_der
        self.trial_values = trial_values
        self.init_data()
        self.init_plot(channel_number, trial_number)

        self.canvas.Bind(wx.EVT_SCROLLWIN, self.OnScrollEvt)

    def init_data(self):
        self.x = []
        for i in range(len(self.trial_values)):
            self.x.append(i)

        # Extents of data sequence:
        self.i_min = 0
        # self.i_max = len(self.t)
        self.i_max = len(self.trial_values)

        # Size of plot window:
        self.i_window = len(self.trial_values)

        # Indices of data interval to be plotted:
        self.i_start = 0
        self.i_end = self.i_start + self.i_window

    def init_plot(self, channel_number, trial_number):
        self.axes = self.fig.add_subplot(111)
        self.plot_data = \
            self.axes.plot(self.x[self.i_start:self.i_end],
                           self.trial_values[self.i_start:self.i_end])[0]

        self.axes.set_ylim(min(self.y_min, -self.stdX * self.channel_std_der), self.y_max)

        self.axes.axhline(y=self.channel_mean, linewidth=0.3, color='r')
        self.axes.axhline(y=self.stdX * self.channel_std_der, linewidth=0.3, color='g', linestyle='--')
        self.axes.axhline(y=-self.stdX * self.channel_std_der, linewidth=0.3, color='g', linestyle='--')

        self.axes.set_ylabel('Amplitudes')
        self.axes.set_xlabel('Relative Timestamp')
        self.axes.set_title('Channel ' + str(channel_number) + ' Trial ' + str(trial_number) + ' Snapshot')

    def draw_plot(self):

        # Update data in plot:
        self.plot_data.set_xdata(self.x[self.i_start:self.i_end])
        self.plot_data.set_ydata(self.trial_values[self.i_start:self.i_end])

        # Adjust plot limits:
        self.axes.set_xlim((min(self.x[self.i_start:self.i_end]),
                            max(self.x[self.i_start:self.i_end])))

        self.axes.set_ylim(min(self.y_min, -self.stdX * self.channel_std_der), self.y_max)

        self.axes.axhline(y=self.channel_mean, linewidth=0.3, color='r')
        self.axes.axhline(y=self.stdX * self.channel_std_der, linewidth=0.3, color='g', linestyle='--')
        self.axes.axhline(y=-self.stdX * self.channel_std_der, linewidth=0.3, color='g', linestyle='--')

        # self.axes.scatter(self.bursts_x, self.bursts_y, c='black')
        for i in range(0, len(self.bursts_x), 2):
            point1 = [self.bursts_x[i], self.bursts_y[i]]
            point2 = [self.bursts_x[i + 1], self.bursts_y[i + 1]]
            x_values = [point1[0], point2[0]]
            y_values = [point1[1], point2[1]]
            if (all(i > self.channel_mean for i in y_values)):
                y_values = [self.stdX * self.channel_std_der, self.stdX * self.channel_std_der]
            else:
                y_values = [-self.stdX * self.channel_std_der, -self.stdX * self.channel_std_der]
            self.axes.plot(x_values, y_values, color='black')
            self.axes.scatter(x_values, y_values, c='black')

        # Redraw:
        self.canvas.draw()

    def update_scrollpos(self, new_pos):
        self.i_start = self.i_min + new_pos
        self.i_end = self.i_min + self.i_window + new_pos
        self.canvas.SetScrollPos(wx.HORIZONTAL, new_pos)
        self.draw_plot()

    def OnScrollEvt(self, event):
        evtype = event.GetEventType()

        if evtype == wx.EVT_SCROLLWIN_THUMBTRACK.typeId:
            pos = event.GetPosition()
            self.update_scrollpos(pos)
        elif evtype == wx.EVT_SCROLLWIN_LINEDOWN.typeId:
            pos = self.canvas.GetScrollPos(wx.HORIZONTAL)
            self.update_scrollpos(pos + 1)
        elif evtype == wx.EVT_SCROLLWIN_LINEUP.typeId:
            pos = self.canvas.GetScrollPos(wx.HORIZONTAL)
            self.update_scrollpos(pos - 1)
        elif evtype == wx.EVT_SCROLLWIN_PAGEUP.typeId:
            pos = self.canvas.GetScrollPos(wx.HORIZONTAL)
            self.update_scrollpos(pos - 10)
        elif evtype == wx.EVT_SCROLLWIN_PAGEDOWN.typeId:
            pos = self.canvas.GetScrollPos(wx.HORIZONTAL)
            self.update_scrollpos(pos + 10)
        else:
            print("unhandled scroll event, type id:", evtype)


class MyApp(wx.App):
    def __init__(self, trial_values, outsider_points, channel_number, trial_number, channel_mean, channel_std_der,
                 y_min, y_max, stdX):
        self.trial_values = trial_values
        self.outsider_points = outsider_points
        self.channel_number = channel_number
        self.trial_number = trial_number
        self.channel_mean = channel_mean
        self.channel_std_der = channel_std_der
        self.y_min = y_min
        self.y_max = y_max
        self.stdX = stdX
        wx.App.__init__(self)

    def OnInit(self):
        self.frame = MyFrame(parent=None, id=-1, trial_values=self.trial_values, outsider_points=self.outsider_points,
                             channel_number=self.channel_number, trial_number=self.trial_number,
                             channel_mean=self.channel_mean, channel_std_der=self.channel_std_der,
                             y_min=self.y_min, y_max=self.y_max, stdX=self.stdX)
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True
