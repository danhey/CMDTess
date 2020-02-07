from bokeh.transform import factor_cmap
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, ColorBar
from bokeh.palettes import Viridis
from bokeh.transform import linear_cmap
import bokeh
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import HoverTool,  WheelZoomTool

import pandas as pd
import numpy as np

plot_df = pd.read_csv('plot_df.csv')

output_file("index.html", title='TESS in the Southern Hemisphere')

source = ColumnDataSource(
        data=dict(
            x=plot_df['b-r'].values,
            y=plot_df['absmag'].values,
            imgs = plot_df['files'].values,
            desc = plot_df['ID'].values,
            color = plot_df['GAIAmag']
        )
    )

hover = HoverTool(# height="200" alt="@imgs" width="500"
        tooltips="""
        <div>
            <div>
                <img
                    src="@imgs"
                    border="2"
                ></img>
            </div>
            <div>
                <span style="font-size: 17px; font-weight: bold;">TIC @desc</span>
            </div>
        </div>
        """
    )

wheel = WheelZoomTool()
p = figure(#plot_width=900, plot_height=900, 
           tools=[hover, 'zoom_in', 'undo', wheel, 'reset', 'box_zoom'],
           title="TESS in the Southern Hemisphere", 
           toolbar_location="above",
           sizing_mode='stretch_both',
           x_range=(-1,6), y_range=(16,-5),
            output_backend="webgl"
          )

mapper = linear_cmap(field_name='color', palette=bokeh.palettes.Viridis256,low=min(plot_df['GAIAmag']) ,high=max(plot_df['GAIAmag']))


p.circle('x', 'y', 
         radius=0.001,
#          size=8,
         line_color=mapper,color=mapper, 
         fill_alpha=0.6,
         source=source)

p.xaxis.axis_label = 'Gaia BP - RP'
p.yaxis.axis_label = 'Gaia G absolute magnitude'
p.xaxis.axis_label_text_font_size = "18pt"
p.yaxis.axis_label_text_font_size = "18pt"
p.xaxis.major_label_text_font_size = "15pt"
p.yaxis.major_label_text_font_size = "15pt"
p.title.text_font_size = "15pt"

p.xaxis.axis_label_text_font_style = 'normal'
p.yaxis.axis_label_text_font_style = 'normal'

p.toolbar.active_scroll=wheel

color_bar = ColorBar(color_mapper=mapper['transform'], width=8,  location=(0,0))
p.add_layout(color_bar, 'right')

show(p)