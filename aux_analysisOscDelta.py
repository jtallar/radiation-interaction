import utils

# Replace delta_t values here (delta_t_sim = delta_t_print)
dts = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.05, 0.1]
# Replace ecm values for beeman here
ecms_beeman = [3.4817385E-14, 2.1685357E-11, 3.4546452E-10, 2.0853237E-07, 3.1937059E-06, 1.4876862E-03, 1.8503093E-02]
# Replace ecm values for verlet here
ecms_verlet = [3.4817385E-14, 2.1685357E-11, 3.4546452E-10, 2.0853237E-07, 3.1937059E-06, 1.4876862E-03, 1.8503093E-02]
# Replace ecm values for gpc5 here
ecms_gpc5 = [3.4817385E-14, 2.1685357E-11, 3.4546452E-10, 2.0853237E-07, 3.1937059E-06, 1.4876862E-03, 1.8503093E-02]

# Initialize plotting
utils.init_plotter()

utils.plot_multiple_values([dts, dts, dts], 'dt (s)', [ecms_beeman, ecms_verlet, ecms_gpc5], 'ecm (m^2)', ['beeman', 'verlet', 'gpc5'], log=True, legend_loc='lower right')

# Hold execution
utils.hold_execution()