import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Parameters
m = 9.1e-31  # Electron mass in kg
v = 5e5      # Electron velocity in m/s
h = 6.62e-34 # Planck's constant in J·s
wave_length = h / (m * v)  # de Broglie wavelength

# Function to calculate diffraction probability from Fraunhofer Diffraction Eq.
#   a = Slit width in meters
#   d = Distance between slits in meters
#   l = Distance to screen in meters
def Diffraction(a, d, wave_length, l, x):

    #c = (np.pi * d) / (wave_length * l)
    #k = (np.pi * a) / (wave_length * l)
    
    #probability = ((np.cos(c))**2)*(((np.sin(k*x))/(k*x))**2)

    c = (np.pi * d * x) / (wave_length * l)
    k = (np.pi * a * x) / (wave_length * l)

    sinc_term = np.sinc(k / np.pi)
    probability = (np.cos(c) ** 2) * (sinc_term ** 2)

    return probability

# Monte Carlo simulation function
def MonteCarlo(a, d, wave_length, l, num_samples):

    #Create array of random points on the screen
    x = np.random.uniform(-0.001, 0.001, num_samples)

    # Calculate the intensity at that point to get the probability
    # The p array contains probability values corresponding to each x.
    p = Diffraction(a, d, wave_length, l, x) 

    # Generate random number to decide whether to keep each particle.
    # These values are thresholds for acceptance or rejection.
    rand = np.random.uniform(0, 1, num_samples)

    # Monte Carlo threshold
    # If the Intensity result is > random number add to the list of accepted results.
    # Uses boolean array to filter the x array, keeping only the x values where the condition is True.
    accepted = x[p >= rand] 
    return accepted

# Create the Dash app
app = Dash(__name__)

#create the sliders
app.layout = html.Div([
    dcc.Graph(id='interference-graph'),
    html.Label('Slit Width (m)'),
    dcc.Slider(
        id='slit-width-slider',
        min=50e-6,
        max=300e-6,
        step=10e-6,
        value=150e-6,
        marks={i: f'{i:.0e}' for i in np.linspace(50e-6, 300e-6, 6)}
    ),
    html.Label('Slit Distance (m)'),
    dcc.Slider(
        id='slit-distance-slider',
        min=200e-6,
        max=1000e-6,
        step=50e-6,
        value=600e-6,
        marks={i: f'{i:.0e}' for i in np.linspace(200e-6, 1000e-6, 5)}
    ),
    html.Label('Screen Distance (m)'),
    dcc.Slider(
        id='screen-distance-slider',
        min=1,
        max=20,
        step=1,
        value=10,
        marks={i: f'{i}' for i in range(1, 21)}
    ),
    html.Label('Number of Particles'),
    dcc.Slider(
        id='num-particles-slider',
        min=10**3,
        max=10**6,
        step=10**4,
        value=10**6,
        marks={i: f'{i:.0e}' for i in np.linspace(10**3, 10**6, 4)}
    )
])

@app.callback(
    Output('interference-graph', 'figure'),
    Input('slit-width-slider', 'value'),
    Input('slit-distance-slider', 'value'),
    Input('screen-distance-slider', 'value'),
    Input('num-particles-slider', 'value')
)


# The update_graph function takes the values from the sliders (a, d, l, numParticles) as arguments.
#	•	Inside the fcn, these values are used to update the simulation.
#	•	returns the new figure, which updates the graph in the Dash app.

def update_graph(a, d, l, numParticles):

    # Generate array of simulated particles using Monte Carlo function
    particles_x = MonteCarlo(a, d, wave_length, l, int(numParticles))

    # Rolling a random y value as well to give our bands vertical spread
    particles_y = np.random.uniform(0, 1, len(particles_x))

    # Create scatter plot
    scatter_trace = go.Scatter(x=particles_x, y=particles_y, mode='markers',
                               marker=dict(size=2, opacity=0.5), name='Particles' )

    
    # Create histogram data
    hist_y, hist_x = np.histogram(particles_x, bins=75, density=True)
    hist_x = (hist_x[:-1] + hist_x[1:]) / 2  # Compute the bin centers

    # Create histogram trace
    hist_trace = go.Bar(x=hist_x, y=hist_y, name='Simulated Distribution', opacity=0.6)

    # Theoretical interference wave pattern
    x = np.linspace(-0.001, 0.001, 500)
    theoretical_prob = Diffraction(a, d, wave_length, l, x)
    theoretical_prob_normalized = theoretical_prob / np.max(theoretical_prob) * np.max(hist_y)
    theoretical_trace = go.Scatter(x=x, y=theoretical_prob_normalized, mode='lines', name='Theoretical Model')

    # Create subplot figure
    fig = make_subplots(rows=2, cols=1, subplot_titles=("Double Slit Interference Pattern", "Theoretical Model Over the Generated Distribution"))
    
    # Add scatter plot and histogram to fig
    fig.add_trace(scatter_trace, row=1, col=1)

    fig.add_trace(hist_trace, row=2, col=1)
    fig.add_trace(theoretical_trace, row=2, col=1)

    # Update layout title
    fig.update_layout(height=800, title_text="Interactive Double Slit Interference Monte Carlo Simulation")
    
    # Add x and y axis labels
    fig.update_xaxes(title_text="X position (meters)", row=1, col=1)
    fig.update_yaxes(title_text="Y position", row=1, col=1)
    fig.update_xaxes(title_text="X position (meters)", row=2, col=1)
    fig.update_yaxes(title_text="Probability Density", row=2, col=1)

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
