
easy-plot
=========

**easyplot:** A thin matplotlib wrapper written in Python to enable fast
and easy creation of reusable plots.

by `Sudeep Mandal <http://www.sudeepmandal.com>`__

.. raw:: html

   <hr>

I'd love to hear your comments and/or suggestions. You can get in touch
with me via `twitter <https://twitter.com/hamsterhuey>`__,
`email <mailto:sudeepmandal@gmail.com>`__ or
`google+ <https://plus.google.com/u/0/105292596991480463202/>`__

.. raw:: html

   <hr>



Sections
--------

-  `Requirements <#requirements>`__
-  `Installation <#installation>`__
-  `Motivation and Background <#motivation>`__
-  `Features <#features>`__
-  `Usage and Examples <#usage>`__

   -  `Simple Plot <#simple_plot>`__
   -  `Multiple plots in the same figure
      (Interactive) <#multiple_plots>`__
   -  `Using EasyPlot object as template for new
      plots <#easyplot_template>`__
   -  `Autoscaling Plots <#autoscale>`__
   -  `Setting background grid <#grid>`__
   -  `Log/Linear/Symlog plots <#log_linear_scale>`__
   -  `Modifying Plot color cycle <#colorcycle>`__
   -  `Multiple plots in same figure iteratively using
      iter\_plot <#iter_plot>`__

-  `Advanced plotting <#advanced_plotting>`__

   -  `Using easyplot with subplots <#subplots>`__



Requirements
------------

Python 2.7.2+, matplotlib





Installation
============

[`back to section overview <#sections>`__\ ]

You can use the following commands to install EasyPlot:

``pip install easyplot``

or

``easy_install easyplot``

Alternatively, you could download the package manually from the Python
Package Index **[TODO]**, unzip it, navigate into the package, and use
the command:

``python setup.py install``

or

``pip install .``

Motivation and background
-------------------------

[`back to section overview <#sections>`__\ ]

Setting up aesthetically pleasing plots with plot titles, axes labels,
etc requires several lines of boilerplate code in vanilla matplotlib. As
an example, creating a basic plot in matplotlib requires the following
lines of code:

.. code:: python

    fig, ax = plt.subplots()
    ax.plot(x, x**2, label="y = x**2")
    ax.plot(x, x**3, label="y = x**3")
    ax.legend(loc='best');
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('title');

Pylab alleviates some of this, but still requires calls to a number of
different functions that are commonly used (such as xlabel, xlim, etc.).
More complicated plots can require several more lines of code. Typing
all this code every time to generate plots gets tedious very quickly.
This situation is further exacerbated when working in an IPython
Notebook where all plots typically need to be labeled, annotated and
looking their best. Having several lines of code preceeding every plot
in a notebook can break the flow of the document and distract from the
code/concepts being presented by the author. Furthermore, oftentimes,
plots with similar labels and formatting need to be generated repeatedly
with different datasets. Generating these sets of plots would require
retyping these same lines of boilerplate code across different sections
of your code/notebook.

Easyplot is my attempt to address these issues and make generating
quick, pleasant looking, annotated plots a bit easier. In keeping with
`DRY
philosophy <http://en.wikipedia.org/wiki/Don%27t_repeat_yourself>`__,
``easyplot`` enables the creation of an ``EasyPlot`` object that
maintains state information of all plot parameters passed to it in order
to generate a plot. This can then be easily reused to generate new plots
with the user only having to supply any additional plot parameters, or
those parameters he or she wishes to overwrite from the previous plot.

Easyplot supports a large number of standard plot parameters that most
users typically deal with when plotting in matplotlib. Additionally, it
provides methods to access the figure and axes instance for the latest
plot, enabling users to perform more custom plot modifications that are
not directly supported by easyplot. It also supports interactive
plotting where additional plot parameters can be passed to the current
plot using the ``update_plot`` method. The plot above can be generated
using ``easyplot`` as follows:

.. code:: python

    eplot = EasyPlot(x, x**2, label="y = x**2", showlegend=True, xlabel='x', ylabel='y', title='title')
    eplot.add_plot(x, x**3, label="y = x**3")

Along with the reduced typing, easyplot enables the consolidation and
passing of all plot parameters into a single plot call. This is already
quite handy, but the real benefit is evident when you then need to
generate a new plot with the same plot parameters (such as axis labels
and title) but with new data:

.. code:: python

    eplot.new_plot(x, 1/x, label="y = 1/x")



Features
========

[`back to section overview <#sections>`__\ ] - Plot parameter aliases
supported. Can be extended by user for arbitrary alias definitions for
various plot parameters - ``iter_plot()`` method to easily iterate
through x, y datasets and plot multiple plots with a single method call
- Access to underlying figure, axes and line2D objects for advanced
customization - Draggable legend when using GUI backends (eg: qt, wx,
etc.)



Usage and Examples
==================

[`back to section overview <#sections>`__\ ]



Simple plot
-----------

.. code:: python

    # Import modules and setup
    %matplotlib inline
    import matplotlib.pyplot as plt
    import numpy as np
    import sys
    sys.path.append('../')
    from easyplot import EasyPlot
    
    x = np.linspace(0, 10, 10)
.. code:: python

    eplot = EasyPlot(x, x**2, 'g--o', label=r"$y = x^2$", showlegend=True, xlabel='x', ylabel='y', title='title', fontsize=14)


.. image:: images%5Ceasyplot_docs_16_0.png




Multiple plots in same figure (Interactive)
-------------------------------------------

[`back to section overview <#sections>`__\ ]

.. code:: python

    #Note the use of plot parameter aliases and the figsize parameter
    eplot = EasyPlot(x, x**2, label=r"$y = x^2$", figsize=(8,4), showlegend=True, ncol=2, ms=9, markeredgewidth=1.5,
                     xlabel='x', ylabel='y', title='title', color='b', linestyle=':', marker='s')
    eplot.add_plot(x, 0.15*x**3, label=r"$y = 0.15x^3$", c='c', ls='-', alpha=0.6, marker='D')


.. image:: images%5Ceasyplot_docs_19_0.png




Using EasyPlot object as template for new plots
-----------------------------------------------

[`back to section overview <#sections>`__\ ]

The previous example defined an ``EasyPlot`` object ``eplot`` with
various plot parameters set - ``xlabel``, ``ylabel``, ``title``,
``alpha``, ``ncol``, ``markersize`` and ``markeredgewidth`` . We can
examine the current set plot parameters for an ``EasyPlot`` object by
accessing its ``kwargs`` instance variable

.. code:: python

    #Examine set plot parameters for eplot
    eplot.kwargs



.. parsed-literal::

    {'alpha': 0.6,
     'ax': <matplotlib.axes.AxesSubplot at 0x57f74d0>,
     'fancybox': True,
     'fig': <matplotlib.figure.Figure at 0x57955f0>,
     'figsize': (8, 4),
     'framealpha': 1.0,
     'loc': 'best',
     'markeredgewidth': 1.5,
     'markersize': 9,
     'ncol': 2,
     'numpoints': 1,
     'showlegend': True,
     'title': 'title',
     'xlabel': 'x',
     'ylabel': 'y'}



Note that certain plot parameters such as ``linestyle``, ``marker``,
``label`` and ``color`` are considered **unique parameters** and do not
carry over from one plot to another as they are typically unique to a
specific plot.

It is easy to use ``eplot`` as a template to generate a new plot:

.. code:: python

    eplot.new_plot(x, 1/(1+x), '-s', label=r"$y = \frac{1}{1+x}$", c='#fdb462')
    # Note that the plot reuses the axis labels, title, transparency and marker formatting from the previous eplot template


.. image:: images%5Ceasyplot_docs_24_0.png




Autoscaling plots
-----------------

EasyPlot objects have an ``autoscale()`` instance method that can be
called on the instance to reset the ``xlim`` and ``ylim`` properties to
``None`` and autoscale the axes. The method signature is listed below
along with the default parameter values.

.. code:: python

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



Setting background grid
-----------------------

[`back to section overview <#sections>`__\ ]

easyplot provides two ways to display the background grid for the axes.
- To display a simple grid without any custom formatting, the plot
parameter ``grid='on'`` can be passed to the easyplot object. Setting
``grid='off'`` turns the grid off.

.. code:: python

    eplot.new_plot(x, 1/(1+x), '-s', label=r"$y = \frac{1}{1+x}$", c='#fdb462', grid='on')


.. image:: images%5Ceasyplot_docs_29_0.png


-  For more advanced control of the grid, the easyplot ``grid()``
   instance method is provided with a call signature of
   ``grid(self, b=None, which='major', axis='both', **kwargs)`` where
   ``**kwargs`` are passed to linespec of grid lines (eg: linewidth=2)

.. code:: python

    eplot.new_plot(x, 1/(1+x), '-s', label=r"$y = \frac{1}{1+x}$", c='#fdb462')
    eplot.grid(which='major', axis='x', linewidth=2, linestyle='--', color='b', alpha=0.5)
    eplot.grid(which='major', axis='y', linewidth=2, linestyle='-', color='0.85', alpha=0.5)


.. image:: images%5Ceasyplot_docs_31_0.png




Log/Linear/Symlog plots
-----------------------

[`back to section overview <#sections>`__\ ]

Plot parameters ``xscale`` and ``yscale`` can be passed to easyplot
instances with any of the following values:
``['linear'|'log'|'symlog']``

.. code:: python

    eplot.new_plot(x, 1/(1+x), '-s', label=r"$y = \frac{1}{1+x}$", c='#fdb462', yscale='log')
    eplot.grid(which='minor', axis='both')


.. image:: images%5Ceasyplot_docs_34_0.png




Modifying Plot color cycle
--------------------------

[`back to section overview <#sections>`__\ ]

easyplot provides the ``colorcycle`` plot parameter to specify the plot
color cycle. If the ``colorcycle`` parameter is passed with every
``add_plot`` command, it will result in all plots using the first color
of ``colorcycle``. To avoid this, the ``colorcycle`` parameter should be
set as shown below, prior to adding plots to the ``EasyPlot`` instance.

.. code:: python

    # Setup
    colors = ["#66c2a5","#fc8d62","#8da0cb","#e78ac3","#a6d854","#ffd92f","#e5c494","#b3b3b3"] #Colorbrewer colors
    x = np.linspace(0,10,200)
    
    # Demo of color cycle
    # Note the use of EasyPlot constructor with no x,y data to initialize colorcycle prior to adding plots to the figure
    sinplot = EasyPlot(xlabel=r'$\sin (3\pi x/L)$', ylabel='$Amplitude$', fontsize=16, colorcycle=colors, figsize=(10,5))
    
    for index, color in enumerate(colors):
        sinplot.add_plot(x, np.sin(3*np.pi*x/10 + index*np.pi/8), lw=2)


.. image:: images%5Ceasyplot_docs_37_0.png




Multiple plots in same figure iteratively using iter\_plot
----------------------------------------------------------

[`back to section overview <#sections>`__\ ]

``EasyPlot`` objects have a very useful ``iter_plot()`` method to
iterate through ``x``, ``y`` data stored in dictionaries or 2D arrays
and plot them in a figure using a single method call to ``iter_plot``.
The method signature of ``iter_plot`` is as follows:

.. code:: python

    def iter_plot(self, x, y, mode='dict', **kwargs):
        """
        Plot multiple plots by iterating through x, y and parameter lists

        Arguments:
        ==========
          x : x values. 1D List/Array, Dictionary or Numpy 2D Array
          y : y values. Dictionary or Numpy 2D Array
          mode : y, labels and other parameters should either be a Dictionary
                 or a 2D/1D Numpy array where each value/row/element corresponds to a single plot
                 ['dict'|'numpy']
          **kwargs : Plot params as defined in __init__ documentation.
             Params can either be:
               scalars (same value applied to all plots),
               dictionaries (mode='dict', key[val] value applies to each plot)
               1D Lists/Numpy Arrays (mode='numpy', param[index] applies to each
               plot)
        """

The examples below demonstrate the use of ``iter_plot`` to generate
multiple plots from a dataset using both ``mode`` settings, i.e.,
``mode='dict'`` and ``mode='numpy'``. Note that single value plot
parameters that are passed to ``iter_plot`` (such as ``linewidth``) are
applied to all plots in the figure.

.. code:: python

    # Setup the x, y data and plot parameters for both modes
    x = np.linspace(0, 10, 11)
    dict_keys = ['x2', 'x3', 'x4']
    labels_list = ['$y = x^2$', '$y = 0.1x^3$', '$y = 0.01x^4$']
    markers_list = ['s', 'o', 'D']
    linestyle_list = ['-', '--', ':']
    y_dict, marker_dict, labels_dict, linestyle_dict = {}, {}, {}, {}
    y_numpy = np.empty((len(dict_keys), x.shape[0]))
    for ind, key in enumerate(dict_keys):
        marker_dict[key] = markers_list[ind]
        labels_dict[key] = labels_list[ind]
        linestyle_dict[key] = linestyle_list[ind]
        y_dict[key] = (0.1**ind)*x**(ind+2)
        y_numpy[ind][:] = (0.1**ind)*x**(ind+2)
        
.. code:: python

    # Demonstrate iter_plot using mode='dict'
    eplot = EasyPlot(xlabel=r'$x$', ylabel='$y$', fontsize=16, colorcycle=["#66c2a5","#fc8d62","#8da0cb"], figsize=(8,5))
    eplot.iter_plot(x, y_dict, linestyle=linestyle_dict, marker=marker_dict, label=labels_dict, 
                    linewidth=3, ms=10, showlegend=True, grid='on')


.. image:: images%5Ceasyplot_docs_41_0.png


.. code:: python

    # Demonstrate iter_plot using mode='numpy'
    eplot = EasyPlot(xlabel=r'$x$', ylabel='$y$', fontsize=16, colorcycle=["#66c2a5","#fc8d62","#8da0cb"], figsize=(8,5))
    eplot.iter_plot(x, y_numpy, mode='numpy', linestyle=linestyle_list, marker=markers_list, 
                    label=labels_list, linewidth=3, ms=10, showlegend=True, grid='on')


.. image:: images%5Ceasyplot_docs_42_0.png




Advanced plotting
=================

[`back to section overview <#sections>`__\ ]

easyplot objects provide access to their ``figure`` and ``axes`` objects
via the ``get_figure()`` and ``get_axes()`` methods. These methods can
be used in conjunction with regular object oriented matplotlib plotting
methods (for example the set and get methods on the axes object) to
build more complex and elaborate plots as shown in the examples below.
The ``line_list`` instance variable can also be accessed to obtain a
list of ``Line2D`` items corresponding to the plots in the figure. These
can also then be manipulated externally using standard matplotlib
methods. **The ``redraw()`` method must be called on the easyplot object
after any manipulation of the axes and figure objects in order to update
the plot display with the latest changes.**



Using easyplot with subplots
----------------------------

[`back to section overview <#sections>`__\ ]

To create figures with subplots while taking advantage of an easyplot
instance, the axes and figure can be created by the user using
``pyplot.subplots``, ``gridspec`` or other common methods. The reference
to the figure and and one of the subplot axes can be passed to the
easyplot instance method - ``new_plot()`` to obtain the desired results
as demonstrated below.

.. code:: python

    # Reuses sinplot template from one of the previous examples for labels, linewidth and fontsize
    x = np.linspace(0, 10, 200)
    fig, axes = plt.subplots(2, 1, figsize=(10,6)) # Create fig and axes for subplots externally
    sinplot.new_plot(x, np.sin(3*np.pi*x/10 + np.pi/8), fig=fig, ax=axes[0], color="#fc8d62") 
    sinplot.new_plot(x, np.sin(3*np.pi*x/10 + 9*np.pi/8), fig=fig, ax=axes[1], color="#66c2a5")
    fig.set_tight_layout(True)


.. image:: images%5Ceasyplot_docs_47_0.png


