from functinos import *
from math import asin, pi

# Constants
CAT_NUM = 16

DIAMETER_LOWER = 0.6
DENSITY = 600
BETA_MAX = pi / 2

G = 9.81

# Parameters
DIAMETER_UPPER = 0.2 - CAT_NUM / 300
HEIGHT_TREE = 33 + CAT_NUM / 3
LIFTING_TIME = 33 + CAT_NUM * 3

START_HEIGHT = 1

print("Calculations: ")

# Calculation
v_col = cone_vol(DIAMETER_UPPER / 2, DIAMETER_LOWER / 2, HEIGHT_TREE)
m_tree = v_col * DENSITY

print("Volume:", v_col, "m³")
print("Mass:", m_tree, "kg")

h_s = 12.26 # cone_point(DIAMETER_UPPER / 2, DIAMETER_LOWER / 2, HEIGHT_TREE)

print("Center of mass height:", h_s, "m")

beta_0 = asin(1 / h_s)
delta_z_s = h_s - START_HEIGHT

e_req = m_tree * G * delta_z_s
p_req = e_req / LIFTING_TIME

print("Required energy:", p_req, "W")

delta_beta = BETA_MAX - beta_0
omega_av = delta_beta / LIFTING_TIME
omega_max = omega_av * 2

