'''
Units
time = years
distance = AU
'''

import math
import plotly
import plotly.graph_objs as go

# CONSTANTS
start_pos_1 = (1, 0)
start_vel_1 = (0, 6.28)  # Starting velocity of Earth needed for circular orbit
start_pos_2 = (5.2, 0)  # Jupiter average distance from sun
start_vel_2 = (0, 6.28*5.2/12)  # Starting velocity of Jupiter for almost circular orbit
mass_1 = 0.0001185538  # Earth relative coefficient to sun (4pi^2) in AU^3/years^2
mass_2 = 0.0377001105 * 100 # Jupiter relative coefficient to sun (4pi^2) in AU^3/years^2
duration = 12

class Kinematic:
    px = 0
    py = 0
    vx = 0
    vy = 0
    def __init__(self, pos_x, pos_y, vel_x, vel_y):
        self.px = pos_x
        self.py = pos_y
        self.vx = vel_x
        self.vy = vel_y

planet1 = [Kinematic(start_pos_1[0], start_pos_1[1], start_vel_1[0], start_vel_1[1])]
planet2 = [Kinematic(start_pos_2[0], start_pos_2[1], start_vel_2[0], start_vel_2[1])]

dt = 0.001  # time step
steps = int(duration/dt)

for t in range(0, steps, 1):
    r1 = math.sqrt(planet1[t].px ** 2 + planet1[t].py ** 2)
    r2 = math.sqrt(planet2[t].px ** 2 + planet2[t].py ** 2)
    r12 = math.sqrt((planet1[t].px - planet2[t].px) ** 2 + (planet1[t].py - planet2[t].py) ** 2)

    vx = planet1[t].vx - 4 * math.pi ** 2 * planet1[t].px * dt / (r1 ** 3) - mass_2 * (planet1[t].px - planet2[t].px) * dt / (r12 ** 3)
    vy = planet1[t].vy - 4 * math.pi ** 2 * planet1[t].py * dt / (r1 ** 3) - mass_2 * (planet1[t].py - planet2[t].py) * dt / (r12 ** 3)

    px = planet1[t].px + vx * dt
    py = planet1[t].py + vy * dt

    planet1.append(Kinematic(px, py, vx, vy))

    vx2 = planet2[t].vx - 4 * math.pi ** 2 * planet2[t].px * dt / (r2 ** 3) - mass_1 * (planet2[t].px - planet1[t].px) * dt / (r12 ** 3)
    vy2 = planet2[t].vy - 4 * math.pi ** 2 * planet2[t].py * dt / (r2 ** 3) - mass_1 * (planet2[t].py - planet1[t].py) * dt / (r12 ** 3)

    px2 = planet2[t].px + vx2 * dt
    py2 = planet2[t].py + vy2 * dt

    planet2.append(Kinematic(px2, py2, vx2, vy2))


graph1_x = []
graph1_y = []
color1 = []
graph2_x = []
graph2_y = []

i = 0
j = 0

for k in planet1:
    graph1_x.append(k.px)
    graph1_y.append(k.py)
    color1.append(j)
    i += 1
    if i > (duration/dt)/512:
        j += 1
        i = 0

for k in planet2:
    graph2_x.append(k.px)
    graph2_y.append(k.py)

trace_planet1 = go.Scatter(
    x = graph1_x,
    y = graph1_y,
    marker=dict(
        size=2,
        cmax=512,
        cmin=0,
        color=color1,
        colorbar=dict(
            title='Colorbar'
        ),
        colorscale='Viridis'
    ),
    mode='markers',
    name = 'Earth'
)

trace_planet2 = go.Scatter(
    x = graph2_x,
    y = graph2_y,
    mode = 'lines',
    name = 'Jupiter'
)

graph = [trace_planet1, trace_planet2]

layout = go.Layout(
    xaxis=dict(
        range=[-14, 14]
    ),
    yaxis=dict(
        range=[-6, 6]
    )
)

fig = go.Figure(data=graph, layout=layout)

plot_url = plotly.offline.plot(fig, filename='orbit.html')




