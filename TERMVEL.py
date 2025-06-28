import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Terminal Velocity Calculator", layout="centered")
st.title("🪂 Terminal Velocity & Drag Coefficient Calculator")

st.markdown("Simulate how far and how fast an object falls through air.")

# User Inputs
rho = st.number_input("Air Density (kg/m³)", value=1.225, min_value=0.1, max_value=2.0, step=0.01)
mass = st.number_input("Mass of the Object (kg)", value=10000, min_value=1)
area = st.number_input("Cross-sectional Area (m²)", value=1.5, min_value=0.01)
height = st.number_input("Initial Height (m)", value=10000, min_value=1)
dt = st.select_slider("Time Step (s)", options=[0.001, 0.005, 0.01, 0.05, 0.1], value=0.01)

# Constants
g = 9.81
t = 0
v = 0
y = height

# Lists for plotting
velocities = []
times = []

# Run simulation
steps = int(100 / dt)

for i in range(steps):
    drag_force = 0.5 * rho * area * v * abs(v)
    net_force = mass * g - drag_force
    acc = net_force / mass
    v += acc * dt
    y -= v * dt
    t += dt

    velocities.append(v)
    times.append(t)

    if i > int(1/dt) and abs(velocities[-1] - velocities[-int(1/dt)]) < 1e-3:
        break

# Final results
terminal_velocity = velocities[-1]
Cd = (2 * mass * g) / (rho * area * terminal_velocity ** 2)

# Output
st.subheader("Results")
st.markdown(f"**Terminal Velocity:** {terminal_velocity:.2f} m/s")
st.markdown(f"**Estimated Drag Coefficient:** {Cd:.2f}")

# Plotting
fig, ax = plt.subplots()
ax.plot(times, velocities, color='blue')
ax.set_xlabel("Time (s)")
ax.set_ylabel("Velocity (m/s)")
ax.set_title("Velocity vs Time")
ax.grid(True)
st.pyplot(fig)
