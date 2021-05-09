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
rep_count = 20
# Replace delta_t values here (delta_t_sim = delta_t_print)
v0s = [10000.0, 12500.0, 15000.0, 17500.0, 20000.0, 22500.0, 25000.0, 27500.0, 30000.0, 32500.0, 35000.0, 37500.0, 40000.0, 42500.0, 45000.0, 47500.0, 50000.0, 52500.0, 55000.0, 57500.0, 60000.0, 62500.0, 65000.0, 67500.0, 70000.0, 72500.0, 75000.0, 77500.0, 80000.0, 82500.0, 85000.0, 87500.0, 90000.0, 92500.0, 95000.0, 97500.0, 100000.0]
# Replace l_tot values here
l_tot_mean = [7.949E-08, 9.821E-08, 9.845E-08, 1.313E-07, 1.361E-07, 1.443E-07, 1.596E-07, 1.496E-07, 1.535E-07, 1.553E-07, 1.559E-07, 1.555E-07, 1.561E-07, 1.397E-07, 1.617E-07, 1.600E-07, 1.622E-07, 1.556E-07, 1.603E-07, 1.542E-07, 1.375E-07, 1.600E-07, 1.546E-07, 1.556E-07, 1.600E-07, 1.582E-07, 1.526E-07, 1.525E-07, 1.604E-07, 1.604E-07, 1.525E-07, 1.602E-07, 1.592E-07, 1.525E-07, 1.411E-07, 1.526E-07, 1.601E-07]
l_tot_std = [6.288E-08, 6.153E-08, 5.948E-08, 6.060E-08, 4.324E-08, 6.601E-08, 3.896E-08, 6.508E-08, 5.318E-08, 2.299E-08, 1.523E-08, 2.748E-08, 1.925E-08, 5.196E-08, 4.279E-09, 7.762E-09, 5.290E-09, 2.261E-08, 7.284E-10, 2.650E-08, 5.498E-08, 1.684E-11, 3.208E-08, 1.494E-08, 4.698E-11, 7.995E-09, 3.358E-08, 3.358E-08, 1.506E-09, 8.431E-10, 3.356E-08, 7.146E-10, 3.716E-09, 3.356E-08, 4.753E-08, 3.358E-08, 2.797E-10]
# Replace ending values here
top_wall_count = [x / rep_count for x in [0, 1, 1, 1, 4, 3, 3, 1, 4, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
right_wall_count = [x / rep_count for x in [0, 0, 1, 6, 12, 7, 14, 13, 14, 18, 17, 18, 18, 17, 20, 19, 18, 19, 20, 19, 17, 20, 19, 18, 20, 19, 19, 19, 20, 20, 19, 20, 19, 19, 17, 19, 20]]
bot_wall_count = [x / rep_count for x in [1, 2, 2, 5, 0, 4, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
left_wall_count = [x / rep_count for x in [11, 8, 4, 2, 2, 4, 1, 3, 2, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
collision_count = [x / rep_count for x in [8, 9, 12, 6, 2, 2, 1, 2, 0, 1, 1, 0, 1, 2, 0, 1, 1, 1, 0, 1, 3, 0, 1, 2, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 3, 1, 0]]

# Initialize plotting
utils.init_plotter()

utils.plot_multiple_values(
    [v0s, v0s, v0s, v0s, v0s], 'velocidad inicial (m/s)', 
    [top_wall_count, right_wall_count, bot_wall_count, left_wall_count, collision_count], 'probabilidad', 
    ['pared arriba', 'pared derecha', 'pared abajo', 'pared izquierda', 'colisión'], legend_loc='center right', precision=0,
    sci_x=True, sci_y=False, min_val_y=-0.1, max_val_y=1.1)

# Plot errorbars for trajectory length = f(v0)
utils.plot_error_bars(v0s, 'velocidad inicial (m/s)', l_tot_mean, 'longitud de trayectoria (m)', l_tot_std, 0, 2, sci_x=True)

# Hold execution
utils.hold_execution()