import utils

# 1. Turn off plotting in config --> plot: false
# 2. Run multiple simulations with different v0s
#   ./target/tp4-simu-1.0/radiation-interaction.sh -Ddt=1.00000E-14 -Dv0=10000 -DdynamicSuf=_1 --> BEEMAN_1.00000E-14_10000_1.txt
#   python analysisRad.py BEEMAN_1.00000E-14_10000_1.txt BEEMAN_1.00000E-14_10000_2.txt BEEMAN_1.00000E-14_10000_3.txt
# 3. Replace v0s values and other values below with obtained values
# 4. Run python aux_analysisRadVel.py

# Values obtained by runnning
#   ./multipleDt.sh 0.00001 0.00001 0.00010;
# Replace with repetition count
rep_count = 10
# Replace delta_t values here (delta_t_sim = delta_t_print)
v0s = [10000, 100000]
# Replace l_tot values here
l_tot_mean = [8e-08, 10e-08,]
l_tot_std = [8e-08, 6e-08]
# Replace ending values here
top_wall_count = [x / rep_count for x in [1, 3]]
right_wall_count = [x / rep_count for x in [2, 0]]
bot_wall_count = [x / rep_count for x in [3, 2]]
left_wall_count = [x / rep_count for x in [2, 4]]
collision_count = [x / rep_count for x in [2, 1]]

# Initialize plotting
utils.init_plotter()

utils.plot_multiple_values(
    [v0s, v0s, v0s, v0s, v0s], 'v0 (m/s)', 
    [top_wall_count, right_wall_count, bot_wall_count, left_wall_count, collision_count], 'frequency', 
    ['top wall', 'right wall', 'bottom wall', 'left wall', 'collision'], legend_loc='upper right',
    sci_y=False, min_val_y=0, max_val_y=1)

# Plot errorbars for trajectory length = f(v0)
utils.plot_error_bars(v0s, 'v0 (m/s)', l_tot_mean, 'longitud de trayectoria (m)', l_tot_std, 0, 2)

# Hold execution
utils.hold_execution()