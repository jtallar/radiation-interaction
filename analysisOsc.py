import sys
import json

import utils
import analyzerFun as anl

# Read out filename param if provided
dynamic_files = None
if len(sys.argv) >= 2:
    dynamic_files = sys.argv[1:]

# Read params from config.json
with open("config.json") as file:
    config = json.load(file)

if "osc" not in config:
    invalid_param("osc")

dynamic_filename = utils.read_config_param(
    config, "dynamic_file", lambda el : el, lambda el : True)
plot_boolean = utils.read_config_param(
    config, "plot", lambda el : bool(el), lambda el : True)
delta_t = utils.read_config_param(
    config, "delta_t_sim", lambda el : float(el), lambda el : el > 0)
# Read OSC params
algo = utils.read_config_param(
    config["osc"], "algo", lambda el : el, lambda el : True)
mass = utils.read_config_param(
    config["osc"], "mass", lambda el : float(el), lambda el : el > 0)
k = utils.read_config_param(
    config["osc"], "k", lambda el : float(el), lambda el : el > 0)
gamma = utils.read_config_param(
    config["osc"], "gamma", lambda el : float(el), lambda el : el > 0)
amp = utils.read_config_param(
    config["osc"], "A", lambda el : float(el), lambda el : el > 0)

if dynamic_files is None:
    # Perform one analysis, analytic vs one algorithm
    # python analysisOsc.py
    anl.analyze_osc(dynamic_filename, algo, mass, k, gamma, amp, plot_boolean, delta_t)
else:
    # Same dt, different algorithms + analytic
    # python analysisOsc.py beeman.txt verlet.txt gpc5.txt
    x_superlist = []
    y_superlist = []
    legend_list = []
    for filename in dynamic_files:
        # TODO: Change file format (ALGO-dt.txt)
        algo = filename[:-4] # Take filename without .txt extension
        metric = anl.analyze_osc(filename, algo, mass, k, gamma, amp, False, delta_t)
        x_superlist.append(metric.time_vec)
        y_superlist.append(metric.algo_sol)
        legend_list.append(metric.algo)
    x_superlist.append(metric.time_vec)
    y_superlist.append(metric.exact_sol)
    legend_list.append("analítica")

    if plot_boolean:
        # Initialize plotting
        utils.init_plotter()

        # Plot real trajectory with estimated one
        utils.plot_multiple_values(
            x_superlist,
            'tiempo (s)',
            y_superlist,
            'posición (m)',
            legend_list,
            sci=False
        )

        # Hold execution
        utils.hold_execution()    
