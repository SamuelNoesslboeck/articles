from functinos import *
from math import asin, pi
import matplotlib.pyplot as plt

# Constants
CAT_NUM = 16

DIAMETER_LOWER = 0.6
DENSITY = 600
BETA_MAX = pi / 2
SPINDLE_PITCH = 8 / 1

DELTA_TIME = 0.01    # Defines accuracy

# Parameters
DIAMETER_UPPER = 0.2 - CAT_NUM / 300
HEIGHT_TREE = 33 + CAT_NUM / 3
LIFTING_TIME = 33 + CAT_NUM * 3

START_HEIGHT = 1

# General
spec_pitch = SPINDLE_PITCH / 1000 / pi / 2

# Cone
v_col = trun_cone_vol(DIAMETER_UPPER / 2, DIAMETER_LOWER / 2, HEIGHT_TREE)
m_tree = v_col * DENSITY

print("Volume: \t\t\t", v_col, "m³")
print("Mass: \t\t\t\t", m_tree, "kg")

h_com = trun_cone_com(DIAMETER_UPPER / 2, DIAMETER_LOWER / 2, HEIGHT_TREE)

print("Center of mass height:\t\t", h_com, "m")

beta_0 = asin(1 / h_com)
delta_z_s = h_com - START_HEIGHT

e_req = m_tree * G * delta_z_s
p_req = e_req / LIFTING_TIME

print("Average theoretical power:\t", p_req, "W")

delta_beta = BETA_MAX - beta_0
omega_av = delta_beta / LIFTING_TIME
omega_max = omega_av * 2

print("Average angluar velocity: \t", omega_av, "rad/s")

# Inertias
i_tree = inertia_tree(HEIGHT_TREE, m_tree)
i_rod = inertia_rod(i_tree, h_com)
i_motor = inertia_motor(i_rod, spec_pitch)

print("Tree inertia: \t\t\t", i_tree, "kgm²")
print("Rod inertia: \t\t\t", i_rod, "kg")
print("Motor inertia: \t\t\t", i_motor, "kgm²")

# Load
t_tree_max = tree_load_torque(h_com, m_tree, beta_0)
f_cyl_max = cylinder_load_force(t_tree_max, h_com, gamma_t(alpha_t(beta_0)))
t_mot_max = motor_load_force(f_cyl_max, spec_pitch)

print("Max motor torque: \t\t", t_mot_max, "Nm")

# Plotting
distance_0 = cyl_length_from_angle(h_com, alpha_t(beta_0))

velocities = [ 0.0 ]
phis = [ 0.0 ]
distances = [ distance_0 ]
accelerations = [ 0.0 ]
torques = [ 0.0 ]

betas = [ beta_0 ]
alphas = [ alpha_t(beta_0) ]
gammas = [ gamma_t(alphas[-1]) ]

xdata = [ 0.0 ]

while True:
    try:
        velocity = velocities[-1]
        torque = motor_torque(velocity) - motor_load_force(cylinder_load_force(tree_load_torque(h_com, m_tree, betas[-1]), h_com, gammas[-1]), spec_pitch)
        acceleration = torque / i_motor
        velocity = (acceleration + accelerations[-1]) / 2 * DELTA_TIME
        phi = phis[-1] + (velocity + velocities[-1]) / 2 * DELTA_TIME 
        distance = distance_0 - phi * spec_pitch
        
        alpha = cyl_angle_from_length(h_com, distance)
        beta = beta_t(alpha)
        gamma = gamma_t(alpha)
        
        if distance < 0:
            alpha = 0
            beta = pi / 2
            gamma = 0
        
        velocities.append(velocity)
        torques.append(torque)
        accelerations.append(acceleration)
        phis.append(phi)
        distances.append(distance)
        alphas.append(alpha)
        betas.append(beta)
        gammas.append(gamma)
        
        if beta >= (pi / 2):
            break
        
        xdata.append(xdata[-1] + DELTA_TIME)
    except Exception as e:
        print("Error in iteration number:", len(xdata))
        print(e)
        break


# plt.plot(xdata[0:len(velocities)], velocities, "red")
plt.plot(xdata[0:len(velocities)], betas)
plt.show()