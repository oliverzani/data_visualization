# Command to run bokeh server
# bokeh serve --show example_data_visualization_with_bokeh.py

# Import the necessary modules
from bokeh.io import curdoc, show
from bokeh.models import ColumnDataSource, Slider, CategoricalColorMapper, HoverTool, Select
from bokeh.plotting import figure
from bokeh.palettes import Spectral6
from bokeh.layouts import widgetbox, row, column
from bokeh.models.widgets import Tabs, Panel, DataTable, TableColumn

#Import the Data
import pandas
data = pandas.read_csv("C:\\Users\\olive\\Documents\\Class\\Data Mining\\Bokeh\\airline_data.csv")

# Creating the source data
source = ColumnDataSource(data={
    'time'         : data['ActualElapsedTime'][data['Month']==1],
    'depdelay'     : data['DepDelay'][data['Month']==1],
    'carrier'      : data['Carrier_Name'][data['Month']==1],
    'air'          : data['AirTime'][data['Month']==1],
    'arrdelay'     : data['ArrDelay'][data['Month']==1],
    'origin'       : data['Origin'][data['Month']==1],
    'dest'         : data['Dest'][data['Month']==1]
})

# Initial creation of Plot to display Total Time of Flight to Departure Delay time
xmin, xmax = min(data.ActualElapsedTime) -50 , max(data.ActualElapsedTime) +50
ymin, ymax = min(data.DepDelay) -50, max(data.DepDelay) +50

plot = figure(title='Airline Delay Data ', plot_height=800, plot_width=1400,
              x_range=(xmin, xmax), y_range=(ymin, ymax), 
              tools = "lasso_select, reset, box_select, pan")

plot.xaxis.axis_label ='Total Time of Flight'
plot.yaxis.axis_label = 'Departure Delay'

# Creation of coloring assigned to data points based on carrier
carrier_list = data.Carrier_Name.unique().tolist()
color_mapper = CategoricalColorMapper(factors=carrier_list , palette=Spectral6)

plot.circle(x='time', y='depdelay', fill_alpha=0.8, source=source,
            color=dict(field='carrier', transform=color_mapper), legend='carrier')

plot.legend.location = 'top_right'
show(plot)

# Function to update the data presented when the Month selected, X, or Y values change
def update_plot(attr, old, new):

    month = slider.value
    x = x_select.value
    y = y_select.value
    
    new_data = {
        'time'       : data[x][data['Month']==month],
        'depdelay'       : data[y][data['Month']==month],
        'carrier'      : data['Carrier_Name'][data['Month']==month],
        'air'          : data['AirTime'][data['Month']==month],
        'arrdelay'     : data['ArrDelay'][data['Month']==month],
        'origin'       : data['Origin'][data['Month']==month],
        'dest'         : data['Dest'][data['Month']==month]
    }
    source.data = new_data
    
    
    plot.title.text = 'Airline data for month %d' % month

# Function to update the range of the plot based on the X andd Y values selected
def update_range(attr, old, new):
    
    x = x_select.value
    y = y_select.value
    month = slider.value
    
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    
    new_data = {
        'time'         : data[x][data['Month']==month],
        'depdelay'     : data[y][data['Month']==month],
        'carrier'      : data['Carrier_Name'][data['Month']==month],
        'air'          : data['AirTime'][data['Month']==month],
        'arrdelay'     : data['ArrDelay'][data['Month']==month],
        'origin'       : data['Origin'][data['Month']==month],
        'dest'         : data['Dest'][data['Month']==month]
    }
    source.data = new_data
    
    plot.x_range.start = min(data[x]) - .1*abs(max(data[x]))
    plot.x_range.end = max(data[x]) +.1*abs(min(data[x]))
    plot.y_range.start = min(data[y]) -.1*abs(max(data[y]))
    plot.y_range.end = max(data[y]) +.1*abs(min(data[y]))

# Creation of a slider to change the month selected
slider = Slider(start=1,end=5,step=1,value=1,title='Month')
slider.on_change('value',update_plot)

# Creation of Hover tooltip
hover = HoverTool(tooltips=[('Air Time','@air'), 
                            ('Origin', '@origin'),
                            ('Destination', '@dest')])
plot.add_tools(hover)

# Creation of X and Y selection tool boxes
x_select = Select(
    options=['ActualElapsedTime', 'DepDelay', 'ArrDelay', 'Distance', 'AirTime'],
    value='ActualElapsedTime',
    title='x-axis data'
)
x_select.on_change('value', update_range)

y_select = Select(
    options=['ActualElapsedTime', 'DepDelay', 'ArrDelay', 'Distance', 'AirTime'],
    value='DepDelay',
    title='y-axis data'
)
y_select.on_change('value',update_range)

#Summarizing the above plot into a single panel
layout = row(widgetbox(slider, x_select, y_select), plot)
Last_Big_Advanced = Panel(child = layout, title = "Larger Data Set")

#Creation of Second data source
source2 = ColumnDataSource(data={
    'time'         : data['ActualElapsedTime'][data['Month']==1],
    'depdelay'     : data['DepDelay'][data['Month']==1],
    'carrier'      : data['Carrier_Name'][data['Month']==1],
    'air'          : data['AirTime'][data['Month']==1],
    'arrdelay'     : data['ArrDelay'][data['Month']==1],
    'origin'       : data['Origin'][data['Month']==1],
    'dest'         : data['Dest'][data['Month']==1]
})

# Creation of 3 simple scatter plots with associated labels
# Sources are identical to ensure each plot refers to the same data and enable linked selection
p1 = figure(title='Total Time vs Air Time', tools=[hover, 'box_select', 'lasso_select', 'pan', 'reset'])
p1.circle('time', 'air',
          color = 'blue', source = source2)
p1.xaxis.axis_label ='Total Time of Flight'
p1.yaxis.axis_label = 'Air Time'

p2 = figure(title='Total Time vs Departure Delay', tools=[hover, 'box_select', 'lasso_select', 'pan', 'reset'])
p2.circle('time', 'depdelay',
          color = 'green', source = source2)
p2.xaxis.axis_label ='Total Time of Flight'
p2.yaxis.axis_label = 'Departure Delay'

p3 = figure(title='Total Time vs Arrival Delay', tools=[hover, 'box_select', 'lasso_select', 'pan', 'reset'])
p3.circle('time', 'arrdelay',
          color = 'red', source = source2)
p3.xaxis.axis_label ='Total Time of Flight'
p3.yaxis.axis_label = 'Arrival Delay'

# Linking the ranges to allow for linked dragging
p3.x_range = p2.x_range = p1.x_range
p3.y_range = p2.y_range = p1.y_range

#Summarizing the above plot into a single panel
layout_drag = row(p1,p2,p3)
Drag_and_Select = Panel(child = layout_drag, title = 'Dragging and Selecting')


# Creation of a simple flight delay recommendation system

#Initial creation of variables used to created the following data source
carrier_list_tbd = carrier_list
counts_of_delays = [0,0,0,0,0,0]
source3 = ColumnDataSource(data={
    'car_list'     : carrier_list_tbd,
    'avg_delay'    : counts_of_delays
})

origins = pandas.unique(data['Origin']).tolist()
dests = pandas.unique(data['Dest']).tolist()
origins.sort()
dests.sort()

# Creation of two selection tools to alter the data displayed in the chart
starting_place = Select(options = origins,
                        value = origins[0], title = 'Origin')
ending_place = Select(options = dests,
                      value = dests[0], title = 'Destination')

# Actual creation of the initial figure
plot_selections = figure(x_range = carrier_list_tbd, title='Airlines vs Average Delay Times', 
                         toolbar_location=None, tools="")
plot_selections.vbar(x='car_list', top='avg_delay', width=0.9, source = source3,
                     color=dict(field='car_list', transform=color_mapper), legend='car_list')
plot_selections.y_range.start = 0
plot_selections.xaxis.axis_label ='Airline Carrier'
plot_selections.yaxis.axis_label = 'Expected Arrival Delay Time'

# Function to alter data presented based on origin location
def change_dest_options(attr, old, new):
    og = starting_place.value
    
    dest_list = (data.loc[(data['Origin'] == og),'Dest'])
    dest_list = pandas.unique(dest_list).tolist()
    dest_list.sort()
    
    ending_place.options = dest_list
    ending_place.value = dest_list[0]
    
starting_place.on_change('value', change_dest_options)

# Function to change available destinations based on origin selected
def change_inputs_graph(attr, old, new):
    
    og = starting_place.value
    dt = ending_place.value

    new_carriers = pandas.unique(data.loc[(data['Origin'] == og) & (data['Dest'] == dt),'Carrier_Name']).tolist()
    new_carriers.sort()
    
    carrier_list_tbd = new_carriers
    
    length_of_carriers = []
    for car in carrier_list_tbd:
        temp_delays_per_airline = (#sum(data.loc[(data['Origin'] == og) & (data['Dest'] == dt) & (data['Carrier_Name'] == car),'DepDelay']) +
                                   sum(data.loc[(data['Origin'] == og) & (data['Dest'] == dt) & (data['Carrier_Name'] == car),'ArrDelay'])) / (
                                  # len(data.loc[(data['Origin'] == og) & (data['Dest'] == dt) & (data['Carrier_Name'] == car),'DepDelay']) + 
                                    len(data.loc[(data['Origin'] == og) & (data['Dest'] == dt) & (data['Carrier_Name'] == car),'ArrDelay']))
        length_of_carriers = length_of_carriers + [temp_delays_per_airline]
            
    new_data = {
        'car_list'     : carrier_list_tbd,
        'avg_delay'    : length_of_carriers
    }
    source3.data = new_data
    
    plot_selections.x_range = carrier_list_tbd
    
ending_place.on_change('value', change_inputs_graph)

# Summarization of chart into a single panel
layout_selections = row(widgetbox(starting_place, ending_place), plot_selections)
Selection_and_Bar = Panel(child = layout_selections, title = "Selecting an Airline")

# Combining the above 3 panels into a 3 tabs on a single webpage
tabs = Tabs(tabs=[Drag_and_Select, Last_Big_Advanced, Selection_and_Bar])
curdoc().add_root(tabs)
curdoc().title = 'AirPlanes'