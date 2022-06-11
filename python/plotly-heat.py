from audioop import reverse
import os
import numpy as np
import plotly.graph_objects as go

if not os.path.exists("images"):
    os.mkdir("images")

import plotly.express as px

def discrete_colorscale(bvals, colors):
    """
    bvals - list of values bounding intervals/ranges of interest
    colors - list of rgb or hex colorcodes for values in [bvals[k], bvals[k+1]],0<=k < len(bvals)-1
    returns the plotly  discrete colorscale
    """
    if len(bvals) != len(colors)+1:
        raise ValueError('len(boundary values) should be equal to  len(colors)+1')
    bvals = sorted(bvals)     
    nvals = [(v-bvals[0])/(bvals[-1]-bvals[0]) for v in bvals]  #normalized values
    
    dcolorscale = [] #discrete colorscale
    for k in range(len(colors)):
        dcolorscale.extend([[nvals[k], colors[k]], [nvals[k+1], colors[k]]])
    return dcolorscale  

arr = [[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0.22819223, 0.0199342,  0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 200.004966,   3.83061039, 2.34548223, 1.82483715, 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 150., 0., 0., 0., 0.,  180., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 6., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 0.],
[0., 0., 0., 0., 0., 0.,  0., 0., 0., 0., 0., 0.,  0., 0., 0., 500.]
]

fig = px.imshow(img=arr, zmin=5, zmax=255,cmap='red', labels=dict(color="mmHg"))
# fig.show()

fig.update_layout(width=400, height=400, margin=dict(l=10, r=10, b=10, t=10))
fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
})
fig.write_image("images/fig1.png")
# fig.write_html('first_figure.html', auto_open=True)


# Colouring

bvals = [2, 5, 150, 300, 450, 500]
colors = ['#ffffff', '#7db0f0', '#1eeb44' , '#de8a23', '#de3923']
dcolorsc = discrete_colorscale(bvals, colors)

bvals = np.array(bvals)
tickvals = [np.mean(bvals[k:k+2]) for k in range(len(bvals)-1)] #position with respect to bvals where ticktext is displayed
ticktext = [f'<{bvals[1]}'] + [f'{bvals[k]}-{bvals[k+1]}' for k in range(1, len(bvals)-2)]+[f'>{bvals[-2]}']



heatmap = go.Heatmap(z=arr,colorscale = dcolorsc, 
                     colorbar = dict(thickness=25, 
                                     tickvals=tickvals, 
                                     ticktext=ticktext))
fig2 = go.Figure(data=[heatmap])
fig2.update_layout(width=300, height=400, margin=dict(l=10, r=10, b=10, t=10))
fig2.update_yaxes(autorange="reversed")
fig2.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
fig2.write_image("images/fig2.png")
# fig2.show()                                    