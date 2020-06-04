from motion_detector import df
from bokeh.plotting import figure, show, output_file
from bokeh.models import HoverTool, ColumnDataSource

#covert datetimes into strings
df["Start_string"]=df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"]=df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")


cds=ColumnDataSource(df)

#Figure Setup
p=figure(x_axis_type='datetime', height=100, width=500, sizing_mode="scale_both", title='Motion Graph')
p.yaxis.minor_tick_line_color=None
p.yaxis[0].ticker.desired_num_ticks=1

#Hovertool Setup - Pulls Start & End Times from CSV
hover=HoverTool(tooltips=[("Start","@Start_string"),("End","@End_string")])
p.add_tools(hover)

#Quadrant Setup
q=p.quad(left="Start",right="End",bottom=0,top=1,color="green", source=cds)

#Output of File and Showing The Figure
output_file("Graph.html")
show(p)

