##Visualisation with BOKEH
import bokeh
from bokeh.plotting import figure, output_file, show
from bokeh.io import show, output_notebook
from bokeh.palettes import Blues9
from bokeh.palettes import RdBu3
from bokeh.models import ColumnDataSource, CategoricalColorMapper, ContinuousColorMapper
from bokeh.palettes import Spectral11

output_notebook()

def bokehplot(stock):
    dataset = dict(stock=stock['Close'], Date=stock.index)
  
    plot = figure(plot_width=800, plot_height=250,  title = 'time series for {}' .format(stock.name), x_axis_type="datetime")
    plot.line(stock.index, stock['Close'], color='blue', alpha=0.5)
    
    #show price shock w/o vol shock
    
    plot.circle(stock.index, stock.Close*stock["priceshock_w/0_volshock"], size=4, legend='price shock without vol shock')
    show(plot)
output_file("timeseries.html")
