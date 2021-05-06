import utils

# 1. Turn off plotting in config --> plot: false
# 2. Run multiple simulations with different v0s
#   ./target/tp4-simu-1.0/radiation-interaction.sh -Ddt=1.00000E-14 -Dv0=10000 -DdynamicSuf=_1 --> BEEMAN_1.00000E-14_10000_1.txt
#   python analysisRad.py BEEMAN_1.00000E-14_10000_1.txt BEEMAN_1.00000E-14_10000_2.txt BEEMAN_1.00000E-14_10000_3.txt
# 3. Replace v0s values and other values below with obtained values
# 4. Run python aux_analysisRadVel.py

# Values obtained by runnning
#   ./multipleV0.sh 10000 3
# Replace with repetition count
rep_count = 3
# Replace delta_t values here (delta_t_sim = delta_t_print)
v0s = [10000.0, 20000.0, 30000.0, 40000.0, 50000.0, 60000.0, 70000.0, 80000.0, 90000.0, 100000.0]
# Replace l_tot values here
l_tot_mean = [8e-08, 1.5e-07, 1.602e-07, 1.5e-07, 1.6002e-07, 1.6004e-07, 1.60012e-07, 1.60007e-07, 1.6007e-07, 1.60005e-07]
l_tot_std = [5e-08, 2e-08, 1e-10, 3e-08, 2e-12, 3e-11, 2e-12, 4e-12, 8e-11, 4e-12]
# Replace ending values here
top_wall_count = [x / rep_count for x in [0, 1, 0, 1, 0, 0, 0, 0, 0, 0]]
right_wall_count = [x / rep_count for x in [0, 1, 3, 2, 3, 3, 3, 3, 3, 3]]
bot_wall_count = [x / rep_count for x in [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]]
left_wall_count = [x / rep_count for x in [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
collision_count = [x / rep_count for x in [2, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

# Initialize plotting
utils.init_plotter()

utils.plot_multiple_values(
    [v0s, v0s, v0s, v0s, v0s], 'velocidad inicial (m/s)', 
    [top_wall_count, right_wall_count, bot_wall_count, left_wall_count, collision_count], 'frecuencia', 
    ['top wall', 'right wall', 'bottom wall', 'left wall', 'collision'], legend_loc='upper right', precision=0,
    sci_x=True, sci_y=False, min_val_y=-0.1, max_val_y=1.1)

# Plot errorbars for trajectory length = f(v0)
utils.plot_error_bars(v0s, 'velocidad inicial (m/s)', l_tot_mean, 'longitud de trayectoria (m)', l_tot_std, 0, 1, sci_x=True)

# Hold execution
utils.hold_execution()