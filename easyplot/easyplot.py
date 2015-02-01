# -*- coding: utf-8 -*-
"""
Author: Sudeep Mandal
"""

import matplotlib.pyplot as plt
import matplotlib as mpl

if not plt.isinteractive():
    print("\nMatplotlib interactive mode is currently OFF. It is "
          "recommended to use a suitable matplotlib backend and turn it "
          "on by calling matplotlib.pyplot.ion()\n")

class EasyPlot(object):
    """
    Class that implements thin matplotlib wrapper for easy, reusable plotting
    """
                  
    def __init__(self, *args, **kwargs):
        """
        Arguments
        =========
        *args : Support for plot(y), plot(x, y), plot(x, y, 'b-o'). x, y and
                format string are passed through for plotting
        
        **kwargs: All kwargs are optional
          Plot Parameters:
          ----------------
            fig : figure instance for drawing plots
            ax : axes instance for drawing plots (If user wants to supply axes,
                 figure externally, both ax and fig must be supplied together)
            figSize : tuple of integers ~ width & height in inches
            dpi : dots per inch setting for figure
            label : Label for line plot as determined by *args, string
            color / c : Color of line plot, overrides format string in *args if
                        supplied. Accepts any valid matplotlib color
            linewidth / lw : Plot linewidth
            linestyle / ls : Plot linestyle ['-','--','-.',':','None',' ','']
            marker : '+', 'o', '*', 's', 'D', ',', '.', '<', '>', '^', '1', '2'
            markerfacecolor / mfc : Face color of marker
            markeredgewidth / mew :
            markeredgecolor / mec : 
            markersize / ms : Size of markers
            markevery / mev : Mark every Nth marker 
                              [None|integer|(startind, stride)]
            alpha : Opacity of line plot (0 - 1.0), default = 1.0
            title : Plot title, string
            xlabel : X-axis label, string
            ylabel : Y-axis label, string
            xlim : X-axis limits - tuple. eg: xlim=(0,10). Set to None for auto
            ylim : Y-axis limits - tuple. eg: ylim=(0,10). Set to None for auto
            xscale : Set x axis scale ['linear'|'log'|'symlog']
            yscale : Set y axis scale ['linear'|'log'|'symlog']
                Only supports basic xscale/yscale functionality. Use 
                get_axes().set_xscale() if further customization is required
            grid : Display axes grid. ['on'|'off']. See grid() for more options
            colorcycle / cs: Set plot colorcycle to list of valid matplotlib
                             colors
            fontsize : Global fontsize for all plots

          Legend Parameters:
          ------------------
            showlegend : set to True to display legend
            fancybox : True by default. Enables rounded corners for legend box
            framealpha : Legend box opacity (0 - 1.0), default = 1.0
            loc : Location of legend box in plot, default = 'best'
            numpoints : number of markers in legend, default = 1.0
            ncol : number of columns for legend. default is 1
            markerscale : The relative size of legend markers vs. original. 
                          If None, use rc settings.
            mode : if mode is “expand”, the legend will be horizontally 
                   expanded to fill the axes area (or bbox_to_anchor)
            bbox_to_anchor : The bbox that the legend will be anchored. Tuple of
                             2 or 4 floats
        """
        self._default_kwargs = {'fig': None,
                                'ax': None,
                                'figsize': None,
                                'dpi': mpl.rcParams['figure.dpi'],
                                'showlegend': False,
                                'fancybox': True,
                                'loc': 'best',
                                'numpoints': 1
                               }
        # Dictionary of plot parameter aliases               
        self.alias_dict = {'lw': 'linewidth', 'ls': 'linestyle', 
                           'mfc': 'markerfacecolor', 'mew': 'markeredgewidth', 
                           'mec': 'markeredgecolor', 'ms': 'markersize',
                           'mev': 'markevery', 'c': 'color', 'fs': 'fontsize'}
        
        # List of all named plot parameters passable to plot method                   
        self._plot_kwargs = ['label', 'linewidth', 'linestyle', 'marker',
                            'markerfacecolor', 'markeredgewidth', 'markersize',
                            'markeredgecolor', 'markevery', 'alpha', 'color']
        self._legend_kwargs = ['fancybox', 'loc', 'framealpha', 'numpoints',
                              'ncol', 'markerscale', 'mode', 'bbox_to_anchor']
        # Parameters that should only be passed to the plot once, then reset                 
        self._uniqueparams = ['color', 'label', 'marker', 'linestyle',
                              'colorcycle']
        self._colorcycle = []
        # Mapping between plot parameter and corresponding axes function to call                  
        self._ax_funcs = {'xlabel': 'set_xlabel',
                          'ylabel': 'set_ylabel',
                          'xlim': 'set_xlim',
                          'ylim': 'set_ylim',
                          'title': 'set_title',
                          'colorcycle': 'set_color_cycle',
                          'grid': 'grid',
                          'xscale': 'set_xscale',
                          'yscale': 'set_yscale'}
                         
        self.kwargs = self._default_kwargs.copy() #Prevent mutating dictionary
        self.args = []
        self.line_list = [] # List of all Line2D items that are plotted
        self.add_plot(*args, **kwargs)

    def add_plot(self, *args, **kwargs):
        """
        Add plot using supplied parameters and existing instance parameters
        
        Creates new Figure and Axes object if 'fig' and 'ax' parameters not
        supplied. Stores references to all Line2D objects plotted in 
        self.line_list. 
        Arguments
        =========
            *args : Supports format plot(y), plot(x, y), plot(x, y, 'b-'). x, y 
                    and format string are passed through for plotting
            **kwargs : Plot parameters. Refer to __init__ docstring for details
        """
        self._update(*args, **kwargs)

        # Create figure and axes if needed
        if self.kwargs['fig'] is None:
            if not self.isnewargs:
                return # Don't create fig, ax yet if no x, y data provided
            self.kwargs['fig'] = plt.figure(figsize=self.kwargs['figsize'], 
                                            dpi=self.kwargs['dpi'])
            self.kwargs['ax'] = self.kwargs['fig'].gca()
            self.kwargs['fig'].add_axes(self.kwargs['ax'])

        ax, fig = self.kwargs['ax'], self.kwargs['fig']
        
        # Prevent offset notation in plots
        if type(ax.yaxis.get_major_formatter()) == mpl.ticker.ScalarFormatter:
            ax.ticklabel_format(useOffset=False, axis='y')
        if type(ax.xaxis.get_major_formatter()) == mpl.ticker.ScalarFormatter:
            ax.ticklabel_format(useOffset=False, axis='x')

        # Apply axes functions if present in kwargs
        for kwarg in self.kwargs:
            if kwarg in self._ax_funcs:
                # eg: f = getattr(ax,'set_title'); f('new title')
                func = getattr(ax, self._ax_funcs[kwarg])
                func(self.kwargs[kwarg])
        
        # Add plot only if new args passed to this instance
        if self.isnewargs:
            # Create updated name, value dict to pass to plot method
            plot_kwargs = {kwarg: self.kwargs[kwarg] for kwarg 
                                in self._plot_kwargs if kwarg in self.kwargs}
            
            line, = ax.plot(*self.args, **plot_kwargs)
            self.line_list.append(line)            
          
        # Display legend if required
        if self.kwargs['showlegend']:
            legend_kwargs = {kwarg: self.kwargs[kwarg] for kwarg 
                                in self._legend_kwargs if kwarg in self.kwargs}
            leg = ax.legend(**legend_kwargs)
            if leg is not None:
                leg.draggable(state=True)
        
        if 'fontsize' in self.kwargs:
            self.set_fontsize(self.kwargs['fontsize'])
            
        self._delete_uniqueparams() # Clear unique parameters from kwargs list
        
        if plt.isinteractive(): # Only redraw canvas in interactive mode
            self.redraw()
          
    def update_plot(self, **kwargs):
        """"Update plot parameters (keyword arguments) and replot figure
        
        Usage:
            a = EasyPlot([1,2,3], [2,4,8], 'r-o', label='label 1')
            # Update title and xlabel string and redraw plot
            a.update_plot(title='Title', xlabel='xlabel')
        """
        self.add_plot(**kwargs)
        
    def new_plot(self, *args, **kwargs):
        """
        Plot new plot using EasyPlot object and default plot parameters
        
        Pass a named argument reset=True if all plotting parameters should
        be reset to original defaults
        """
        reset = kwargs['reset'] if 'reset' in kwargs else False
        self._reset(reset=reset)
        if self._colorcycle:
            self.kwargs['colorcycle'] = self._colorcycle
        self.add_plot(*args, **kwargs)
    
    def iter_plot(self, x, y, mode='dict', **kwargs):
        """
        Plot multiple plots by iterating through x, y and parameter lists

        Arguments:
        ==========
          x : x values. 1D List/Array, Dictionary or Numpy 2D Array
          y : y values. Dictionary or 2D Python array (List of Lists where each
              sub-list is one set of y-data) or Numpy 2D Array
          mode : y, labels and other parameters should either be a Dictionary
                 or a 2D Numpy array/2D List where each row corresponds to a 
                 single plot ['dict'|'array']
          **kwargs : Plot params as defined in __init__ documentation.
             Params can either be:
               scalars (same value applied to all plots),
               dictionaries (mode='dict', key[val] value applies to each plot)
               1D Lists/Numpy Arrays (mode='array', param[index] applies to each
               plot)
        """
        if mode.lower() == 'dict':
            for key in y:
                loop_kwargs={}
                for kwarg in kwargs:
                    try: # Check if parameter is a dictionary
                        loop_kwargs[kwarg] = kwargs[kwarg][key]
                    except:
                        loop_kwargs[kwarg] = kwargs[kwarg]
                try:
                    x_loop = x[key]
                except:
                    x_loop = x
                self.add_plot(x_loop, y[key], **loop_kwargs)

        elif mode.lower() == 'array':
            for ind in range(len(y)):
                loop_kwargs={}
                for kwarg in kwargs:
                    # Do not iterate through tuple/string plot parameters
                    if isinstance(kwargs[kwarg], (basestring, tuple)):
                        loop_kwargs[kwarg] = kwargs[kwarg]
                    else:
                        try: # Check if parameter is a 1-D List/Array
                            loop_kwargs[kwarg] = kwargs[kwarg][ind]
                        except:
                            loop_kwargs[kwarg] = kwargs[kwarg]
                try:
                    x_loop = x[ind][:]
                except:
                    x_loop = x
                self.add_plot(x_loop, y[ind], **loop_kwargs)
        else:
            print('Error! Incorrect mode specification. Ignoring method call')

    def autoscale(self, enable=True, axis='both', tight=None):
        """Autoscale the axis view to the data (toggle).
        
        Convenience method for simple axis view autoscaling. It turns 
        autoscaling on or off, and then, if autoscaling for either axis is on,
        it performs the autoscaling on the specified axis or axes.
        
        Arguments
        =========
        enable: [True | False | None]
        axis: ['x' | 'y' | 'both']
        tight: [True | False | None]
        """
        ax = self.get_axes()
        ax.autoscale(enable=enable, axis=axis, tight=tight)
        # Reset xlim and ylim parameters to None if previously set to some value
        if 'xlim' in self.kwargs and (axis=='x' or axis=='both'):
            self.kwargs.pop('xlim') 
        if 'ylim' in self.kwargs and (axis=='y' or axis=='both'):
            self.kwargs.pop('ylim')
        self.redraw()

    def grid(self, **kwargs):
        """Turn axes grid on or off

        Call signature: grid(self, b=None, which='major', axis='both', **kwargs)
        **kwargs are passed to linespec of grid lines (eg: linewidth=2)
        """
        self.get_axes().grid(**kwargs)
        self.redraw()

    def get_figure(self):
        """Returns figure instance of current plot"""
        return self.kwargs['fig']
        
    def get_axes(self):
        """Returns axes instance for current plot"""
        return self.kwargs['ax']
        
    def redraw(self):
        """
        Redraw plot. Use after custom user modifications of axes & fig objects
        """
        if plt.isinteractive():
            fig = self.kwargs['fig']
            #Redraw figure if it was previously closed prior to updating it
            if not plt.fignum_exists(fig.number):
                fig.show()
            fig.canvas.draw()
        else:
            print('redraw() is unsupported in non-interactive plotting mode!')
    
    def set_fontsize(self, font_size):
        """ Updates global font size for all plot elements"""
        mpl.rcParams['font.size'] = font_size
        self.redraw()
        #TODO: Implement individual font size setting
#        params = {'font.family': 'serif',
#          'font.size': 16,
#          'axes.labelsize': 18,
#          'text.fontsize': 18,
#          'legend.fontsize': 18,
#          'xtick.labelsize': 18,
#          'ytick.labelsize': 18,
#          'text.usetex': True}
#        mpl.rcParams.update(params)
    
#    def set_font(self, family=None, weight=None, size=None):
#        """ Updates global font properties for all plot elements
#        
#        TODO: Font family and weight don't update dynamically"""
#        if family is None:
#            family = mpl.rcParams['font.family']
#        if weight is None:
#            weight = mpl.rcParams['font.weight']
#        if size is None:
#            size = mpl.rcParams['font.size']
#        mpl.rc('font', family=family, weight=weight, size=size)
#        self.redraw()
        
    def _delete_uniqueparams(self):
        """Delete plot parameters that are unique per plot
        
        Prevents unique parameters (eg: label) carrying over to future plots"""
        # Store colorcycle list prior to deleting from this instance
        if 'colorcycle' in self.kwargs:
            self._colorcycle = self.kwargs['colorcycle']

        for param in self._uniqueparams:
            self.kwargs.pop(param, None)
        
    def _update(self, *args, **kwargs):
        """Update instance variables args and kwargs with supplied values """
        if args:
            self.args = args # Args to be directly passed to plot command
            self.isnewargs = True
        else:
            self.isnewargs = False

        # Update self.kwargs with full parameter name of aliased plot parameter
        for alias in self.alias_dict:
            if alias in kwargs:
                self.kwargs[self.alias_dict[alias]] = kwargs.pop(alias)
            
        # Update kwargs dictionary
        for key in kwargs:
            self.kwargs[key] = kwargs[key]
           
    def _reset(self, reset=False):
        """Reset instance variables in preparation for new plots
        reset: True if current instance defaults for plotting parameters should
               be reset to Class defaults"""
        self.args = []
        self.line_list = []
        self.kwargs['fig'] = None
        self.kwargs['ax'] = None
        if reset:
            self.kwargs = self._default_kwargs.copy()