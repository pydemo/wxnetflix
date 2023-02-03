import wx
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter, LogFormatter


class Graph(wx.BoxSizer):
    """
    This holds a curve plot with associated toolbar
    keyword arguments:
    parent -- reference to the panel or context the plot should be created in.
    style -- (optional) wx.BoxSizer style. This also sets the deafult expand
        direction for Graph.add_subplot (default: wx.VERTICAL)
    title -- (optional) sets the title of the plot window (default: '').
    dpi -- (optional) sets dots per inch of plot window.
    params -- (optional) set matplotlib rcParams, should be a dictionary.
    (default: sets font size of: ticks, legend, axes label, font)
    **kwargs -- any keyword argument to matplotlib.Figure
    """
    def __init__(self, parent
                , style= wx.VERTICAL
                , title=''
                , dpi=None
                , params = None
                , **kwargs):
        
        super(Graph, self).__init__(style)
        #initialize some font settings for matplotlib
        if params == None:
            params = {'axes.labelsize': 16,
              'font.size': 14,
              'legend.fontsize': 14,
              'xtick.labelsize': 12,
              'ytick.labelsize': 12}
        matplotlib.rcParams.update(params)
        
        self.figure = Figure(dpi=dpi, figsize=(2,2), **kwargs)
        self.canvas = FigureCanvas(parent, wx.NewId(), self.figure)
        self.sub_plots = [self.figure.add_subplot(111)]
        self.toolbar = NavigationToolbar2Wx(self.canvas)
        
        ###Create some controls for the toolbox###
        self.cb_grid = wx.CheckBox(self.toolbar, wx.NewId(), 'Show Grid')
        btn_mark = wx.Button(self.toolbar, wx.NewId(), 'Mark selection')
        #btn_rem = wx.Button(parent, wx.NewId(), 'Remove_graph')
        
        ####add extra controls to toolbar####
        self.toolbar.AddControl(self.cb_grid)
        self.toolbar.AddControl(btn_mark)
        ####create and set toolbar sizer####
        toolbar_sizer = wx.BoxSizer(wx.HORIZONTAL)
        toolbar_sizer.Add(self.toolbar, 0, wx.ALIGN_LEFT)
        toolbar_sizer.Add(self.cb_grid, 0, wx.LEFT | wx.ALIGN_CENTER,30)
        toolbar_sizer.Add(btn_mark, 0, wx.LEFT | wx.ALIGN_CENTER_VERTICAL, 20)
        self.toolbar.SetSizer(toolbar_sizer)
        #needed to update the layout
        self.toolbar.Layout()

        
        #######Main layout#######
        v_sizer = wx.BoxSizer(wx.VERTICAL)
        v_sizer.Add(self.canvas, 1, wx.EXPAND)
        v_sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)
        #Add to self
        self.Add(v_sizer, 1, wx.EXPAND)
        
        ###Set title and other things###
        self.xlabel = ''
        self.ylabel = ''
        self.style = style
        self.titles = [title]
        #layout of plots (height, width, count)
        self.layout = (1,1,1)
        self.cb_grid.SetValue(True)
        self.sub_plots[0].set_title(title)
        self.sub_plots[0].grid(True)
        #list to store all plot lines
        self.plot_lines = [[]]
        #initialize formatter
        self.xformat = [None]
        self.yformat = [None]
        self.set_formatter()
        
        #connect the buttons to event handlers
        self.cb_grid.Connect(-1, -1, wx.wxEVT_COMMAND_CHECKBOX_CLICKED, self.on_cb_grid)
        btn_mark.Connect(-1, -1, wx.wxEVT_COMMAND_BUTTON_CLICKED, self.on_mark)
        #btn_rem.Connect(-1, -1, wx.wxEVT_COMMAND_BUTTON_CLICKED, self.on_rem)
        
    
    ############Event handlers############
    def on_cb_grid(self, evt):
        #toggle if grid should be shown on plot
        for plot in self.sub_plots:
            plot.grid(self.cb_grid.IsChecked())
        self.canvas.draw()
        
    def on_mark(self, evt):
        #draw or remove a selection outline
        if hasattr(self, 'selection'):
            #delete markers
            for plot, markers in zip(self.sub_plots, self.selection):
                for line in markers:
                    plot.lines.remove(line)
            del self.selection
            self.canvas.draw()
        else:
            self.selection =[]
            for i, plot in enumerate(self.sub_plots):
                x1, x2, y1, y2 = plot.axis()
                x = [x1, x2, x2, x1, x1]
                y = [y1, y1, y2, y2, y1]
                self.selection.append(self.redraw(x,y, hold = True
                                        , limits = (x1,x2,y1,y2)
                                        , index = i
                                        ,color = 'k', linewidth = 2.0))
    
    
    def on_rem(self, evt):
        """
        Test function for Graph.remove_subplot
        """
        self.remove_subplot()
        
    ############Event handlers############
    def on_cb_grid(self, evt):
        """
        Toggles if grid should be shown on sub-plots
        """
        for plot in self.sub_plots:
            plot.grid(self.cb_grid.IsChecked())
        self.canvas.draw()
        
    def on_mark(self, evt):
        """
        Draws or removes a selection outline on current sub-plot selection
        """
        if hasattr(self, 'selection'):
            #delete markers
            for plot, lines in zip(self.sub_plots, self.selection):
                for line in lines:
                    plot.lines.remove(line)
            del self.selection
            self.canvas.draw()
        else:
            self.selection =[]
            for i, plot in enumerate(self.sub_plots):
                x1, x2, y1, y2 = plot.axis()
                x = [x1, x2, x2, x1, x1]
                y = [y1, y1, y2, y2, y1]
                self.selection.append(self.redraw(x,y, hold = True
                                        , limits = (x1,x2,y1,y2)
                                        , index = i
                                        ,color = 'k', linewidth = 2.0))
    
    
    ############Worker functions############
    def add_secondary_y_axis(self, label = ''):
        """
        Creates a secondary y_axis on all current sub-plots
        If Graph.add_subplot is called after this function, then
            Graph.redraw_secondary_y will fail
        
        keyword arguments:
        label -- (optional) axis label of the second y-axis (default: '')
        """
        self.sub_plots_ax2 = []
        for plot in self.sub_plots:
            self.sub_plots_ax2.append(plot.twinx())
            self.sub_plots_ax2[-1].set_ylabel(label)
            self.sub_plots_ax2[-1].label = label
        
    
    def add_subplot(self, title='', style=None):
        """
        Adds an additional subplot. If more than one row exists and it will
        not be filled, than the plots on the last row will be expanded to
        fill all horizontal space.
        
        keyword arguments:
        title -- (optional) title text of new subplot (default: '')
        style -- (optional) direction to add subplot, valid data is: wx.VERTICAL
            or wx.HORIZONTAL (default: Graph.style)
        
        return -- index of created plot
        """
        
        style = self.style if style == None else style
        self.titles.append(title)
        count = self.layout[-1] + 1
        size = self.layout[0] * self.layout[1]
        #check if there is room for another subplot
        if size >= count:
            self.layout = self.layout[:2] + (count, )
        else:
            #expand layout
            if style == wx.VERTICAL:
                self.layout = (self.layout[0] + 1, self.layout[1], count)
            else:
                self.layout = (self.layout[0], self.layout[1] + 1, count)
            
        for plot in self.sub_plots:
            self.figure.delaxes(plot)
        self.figure.clear()
            
        self.sub_plots = []
        size = self.layout[0] * self.layout[1]
        for i in range(1,count+1):
            if count < size and i > self.layout[1] * (self.layout[0]-1):
                #expand graphs on last row
                exp_layout = (self.layout[0], self.layout[1] - (size-count))
                exp_i = exp_layout[0] * exp_layout[1] - (count - i)
                self.sub_plots.append(self.figure.add_subplot(*exp_layout + (exp_i,)))
            else:
                self.sub_plots.append(self.figure.add_subplot(*self.layout[:2] + (i, )))
            
        #reinitialze some stuff
        self.plot_lines.append([])
        self.xformat.append(None)
        self.yformat.append(None)
        self.set_formatter(index=-1)
        self.reload_data()
        
        #return sub-plot index
        return count - 1
                
        
    def cleanse_fontcache(self):
        """
        Shouldn't be used. Can fix bug when using frozen programs under windows.
        Better to modify the setup script so that font files are left out of the
        matplotlib data files.
        """
        file_path = path.join(path.expanduser('~'), \
                    '.matplotlib', \
                    'fontList.cache')
        if path.exists(file_path):
            remove(file_path)
    
    
    def redraw(self, x, y
            , index = 0
            , hold=False
            , xmin = None
            , ymin = None
            , limits=None
            , alpha = 1.0
            , **kwarg):
        """
        Updates plot with new vectors
        keyword arguments:
        x -- the x-axis values
        y -- the y-axis values
        index -- (optional) index of subplot to plot the vector in (default: 0)
        hold -- (optional) should old vextors be kept (default: False)
        xmin -- (optional) set minimum value of x-axis (default: None)
        ymin -- (optional) set minimum value of y-axis (default: None)
        limits -- (optional) tuple to set limits of x and y-axis (default: None)
        alpha -- (optional) sets the alpha of the line (default: 1.0)
        
        **kwarg -- all extra keyword arguments are sent to the plot function
        """
        #set plot to update
        try:
            plot = self.sub_plots[index]
        except IndexError:
            raise(IndexError
                , "The sub-plot of index:{0:d} doesn't exist".format(index))
            
        plot.hold(hold)
        lines = plot.plot(x,y, alpha = alpha, **kwarg)
        ####Formatter####
        plot.xaxis.set_major_formatter(self.xformat[index])
        plot.yaxis.set_major_formatter(self.yformat[index])
        
        #redo the labels
        plot.grid(self.cb_grid.IsChecked())
        self.set_label(self.xlabel, self.ylabel)
        plot.set_title(self.titles[index])
        #Create a legend if label was given
        if not lines[0].get_label()[0] == "_":
            plot.legend() #label must be sent through kwarg
        
        #if not ymin == None:
        x1, x2, y1, y2 = plot.axis()
        ymin = y1 if ymin == None else ymin
        xmin = x1 if ymin == None else xmin
        plot.axis((x1, x2, ymin, y2))
        if not limits == None:
            plot.axis(limits)
        
        #plot it
        self.canvas.draw()
        #store lines in a list
        self.plot_lines[index] = plot.lines
        #return line pointer
        return lines
        
        

    def redraw_secondary_y(self, x,y, style = 'r.', **kwarg):
        """
        Update secondary y-axis with a new vector
        keyword arguments:
        x -- the x-axis values
        y -- the y-axis values
        style -- (optional) line style (default: 'r.')
        **kwarg -- all extra keyword arguments are sent to the plot function
        """
        for ax2 in self.sub_plots_ax2:
            ax2.plot(x,y, style, **kwarg)
            ax2.set_ylabel(self.ax2.label)
    
    
    def reload_data(self):
        """
        Reloads grid settings, labels, formatters and titles of sub-plots.
        """
        self.set_label(self.xlabel, self.ylabel)
        for plot, title, xfrm, yfrm in zip(self.sub_plots, self.titles
        , self.xformat, self.yformat):
            plot.set_title(title)
            plot.xaxis.set_major_formatter(xfrm)
            plot.yaxis.set_major_formatter(yfrm)
        self.on_cb_grid(None)
        
        self.canvas.draw()
        
        
    def reload_lines(self):
        """
        Reloads plot lines, in-case sub-plots were recreated
        Doesn't work
        """
        return None
        for plot, lines in zip(self.sub_plots, self.plot_lines):
            for i in range(len(lines)):
                plot.cla() #clear
                lines[i].set_axes(plot)
                plot.add_line(lines[i])
        self.canvas.draw()
    
    def remove_subplot(self):
        """
        Removes the last sub-plot.
        Note that plots in the last row aren't expanded to fill the entire row.
        """
        count = self.layout[-1] - 1
        if count < 0:
            raise ValueError #as  "There is no sub-plot to remove"
        
        self.layout = (self.layout[0], self.layout[1], count)
        
        if count > 0:
            layout_change = True
            #check if layout of plots can be decreased
            if self.layout[0] > 1 and self.layout[1] > 1:
                if self.layout[0] < self.layout[1]:
                    lrg = 1
                    sml = 0
                else:
                    lrg = 0
                    sml = 1
                #check if a decrease is possible on the major axis
                size = (self.layout[lrg] - 1) * (self.layout[sml])
                if size >= count:
                    if lrg == 0:
                        self.layout = (self.layout[0] - 1, self.layout[1], count)
                    else:
                        self.layout = (self.layout[0], self.layout[1] - 1, count)
                else:
                    #check the minor axis
                    size = (self.layout[lrg]) * (self.layout[sml] - 1)
                    if size >= count:
                        if sml == 0:
                            self.layout = (self.layout[0] - 1, self.layout[1], count)
                        else:
                            self.layout = (self.layout[0], self.layout[1] - 1, count)
                    else:
                        layout_change = False
            else:
                if self.layout[0] > self.layout[1]:
                    self.layout = (self.layout[0] - 1, self.layout[1], count)
                else:
                    self.layout = (self.layout[0], self.layout[1] - 1, count)
        else:
            layout_change = False
        
        
        #pop some data
        self.plot_lines.pop(-1)
        self.titles.pop(-1)
        self.xformat.pop(-1)
        self.yformat.pop(-1)
         #check if selection was marked
        if hasattr(self, 'selection'):
            #Remove selection data as it is gone
            #del self.selection
            self.selection.pop(-1)
            if len(self.selection) == 0:
                del self.selection
        
        #clear figure and recreate plots
        if layout_change:
            for plot in self.sub_plots:
                self.figure.delaxes(plot)
            self.figure.clear()
            self.sub_plots = []
            
            for i in range(1,count+1):
                self.sub_plots.append(self.figure.add_subplot(*self.layout[:2] + (i, )))
            self.reload_lines()
        else:
            self.figure.delaxes(self.sub_plots[-1])
            self.sub_plots.pop(-1)
            
       
        #reinitialze some stuff
        self.reload_data()
    
    def set_label(self, xlabel=None, ylabel=None):
        """
        Set labels of the plots axis
        
        keyword arguments:
        xlabel -- (optional) sets the label of the x-axis (default: None)
        ylabel -- (optional) sets the label of the y-axis (default: None)
        """
        self.xlabel = xlabel
        self.ylabel = ylabel
        
        for plot in self.sub_plots:
            plot.set_xlabel(xlabel)
            plot.set_ylabel(ylabel)
        
        self.canvas.draw()
        
        
    def set_formatter(self, frmt = 'sci', axes = 'all', useOffset = True
    , limits = (-3, 3), index=None):
        """
        Should the axis use scientific notation
        
        keyword arguments:
        frmt -- Sets the type of formatter used, valid values are:
            'sci', 'log', 'plain' (default: 'sci')
        axes -- which axes should the formatter be used for, valid values are:
            'all', 'x', 'y' (default: 'all')
        useOffset -- Should offset be used to make the tickers more meaningful 
            (default: True)
        limits -- Limits for scientific notation as a tuple (default: (-3, 3))
        index -- a integer or list of integers with the index of sub-plots for
            which the formatter should set. When None the formatter is set for
            all sub-plots (default: None)
        """
        
        frmt = frmt.lower()
        axes = axes.lower()
        
        if frmt == 'log':
            formatter = LogFormatter()
        else:
            sci = frmt == 'sci'
            formatter = ScalarFormatter(useOffset = useOffset)
            formatter.set_powerlimits(limits)
            formatter.set_scientific(sci)
            
        #format axes
        if type(index) == list:
            for i in index:
                self.set_formatter_axes(axes, formatter, i)
        elif type(index) == int:
            self.set_formatter_axes(axes, formatter, index)
        else:
            count = self.layout[-1]
            self.xformat = [formatter]*count
            self.yformat = [formatter]*count
        
        for plot, xfrm, yfrm in zip(self.sub_plots, self.xformat, self.yformat):
            plot.xaxis.set_major_formatter(xfrm)
            plot.yaxis.set_major_formatter(yfrm)
        self.canvas.draw()
        
    def set_formatter_axes(self, axes, formatter, index):
        """
        Sets the formatter of the sub-plot index for the specified axes.
        The canvas in not redrawn automatically, also note that some functions
        may break if a FormatStrFormatter is used e.g. self.on_mark
        
        keyword arguments:
        axes -- which axes should the formatter be used for, valid values are:
            'all', 'x', 'y' (default: 'all')
        formatter -- a formatter object
        index -- a integer with the index of the sub-plot to set the formatter
        """
        if axes == 'x':
            self.xformat[index] = formatter
        elif axes == 'y':
            self.yformat[index] = formatter
        else:
            self.xformat[index] = formatter
            self.yformat[index] = formatter
        
    def set_title(self, titles = ''):
        """
        Set titles of the sub-plots
        
        keyword arguments:
        titles -- (optional) should be a list of size == sub_plots or a single
            string, which will set all titles (default: None)
        """
        if type(titles) == list:
            if len(titles) == len(self.sub_plots):
                self.titles = titles
            else:
                raise IndexError #, "length of tiles must be the same as sub_plots"
        else:
            self.titles = [titles] * len(self.sub_plots)
        
        for plot, title in zip(self.sub_plots, self.titles):
            plot.set_title(title)
        
        self.canvas.draw()