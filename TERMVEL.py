import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Terminal Velocity Calculator", layout="centered")
st.title("🪂 Terminal Velocity & Drag Coefficient Calculator")
st.markdown("Simulate vertical free-fall of an object through air, accounting for drag force.")

with st.sidebar:
    st.header("Simulation Parameters")
    rho = st.number_input("Air Density (kg/m³)", min_value=0.1, max_value=2.0, value=1.225, step=0.01)
    mass = st.number_input("Object Mass (kg)", min_value=1.0, value=10000.0, step=100.0)
    area = st.number_input("Cross-sectional Area (m²)", min_value=0.01, value=1.5, step=0.1)
    height = st.number_input("Initial Height (m)", min_value=1.0, value=10000.0, step=100.0)
    dt = st.select_slider("Time Step (s)", options=[0.001, 0.005, 0.01, 0.05, 0.1], value=0.01)

g = 9.81
v = 0.0
y = height
t = 0
t_max = 100
steps = int(t_max / dt)

velocities = []
times = []

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

terminal_velocity = velocities[-1]
Cd = (2 * mass * g) / (rho * area * terminal_velocity ** 2)

st.subheader("📊 Results")
st.write(f"**Terminal Velocity:** `{terminal_velocity:.2f} m/s`")
st.write(f"**Estimated Drag Coefficient:** `{Cd:.2f}`")

fig, ax = plt.subplots()
ax.plot(times, velocities, label="Velocity", color="blue")
ax.set_title("Velocity vs Time")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Velocity (m/s)")
ax.grid(True)
ax.legend()
st.pyplot(fig)