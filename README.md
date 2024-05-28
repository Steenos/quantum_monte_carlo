#Double Slit Interference Pattern Simulation

https://interactive-quantum-monte-carlo.onrender.com/

This project simulates the interference pattern observed in a double slit experiment using the Monte Carlo method. The simulation is implemented in Python and provides an interactive visualization using Plotly and Dash.

Description

The double slit experiment demonstrates the wave-particle duality of particles such as electrons. When particles pass through two slits, they create an interference pattern on a screen, characteristic of wave behavior. This project aims to numerically simulate this interference pattern using the Monte Carlo method.

Problem Statement

The goal is to simulate the interference pattern produced by a double slit experiment. Traditional analytical methods are complex and limited in handling large-scale simulations. A numerical approach using the Monte Carlo method provides a flexible and scalable solution.

Numerical Technique

Monte Carlo Method

The Monte Carlo method is a statistical technique that uses random sampling to solve numerical problems. It is suitable for this simulation because:

	•	It efficiently handles a large number of particles.
	•	Its stochastic nature mimics the randomness observed in quantum experiments.
	•	It is flexible and can be adapted to different scenarios and complexities.

Diffraction Function

The function calculates the probability distribution of particle positions using the interference pattern formula:

 $P(x) \propto \left( \cos \left( \frac{\pi d x}{\lambda l} \right) \right)^2 $

Monte Carlo Simulation

	•	Random Sampling: Generate random x positions for particles passing through the slits.
	•	Probability Calculation: Use the diffraction function to calculate the probability of each position.
	•	Acceptance-Rejection: Accept or reject positions based on calculated probabilities to simulate the actual distribution on the screen.

Visualization

The project uses Plotly and Dash to create interactive plots for real-time parameter adjustments and visualization. The outputs include:

	•	Scatter Plot: Displays individual particle positions.
	•	Histogram: Shows the distribution of particle positions.
	•	Theoretical Model Overlay: Compares simulated data with theoretical predictions.




