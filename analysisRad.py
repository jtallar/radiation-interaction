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

if "rad" not in config:
    invalid_param("rad")

dynamic_filename = utils.read_config_param(
    config, "dynamic_file", lambda el : el, lambda el : True)
plot_boolean = utils.read_config_param(
    config, "plot", lambda el : bool(el), lambda el : True)
delta_t = utils.read_config_param(
    config, "delta_t_sim", lambda el : float(el), lambda el : el > 0)
# Read RAD params
algo = utils.read_config_param(
    config["rad"], "algo", lambda el : el, lambda el : True)
mass = utils.read_config_param(
    config["rad"], "mass", lambda el : float(el), lambda el : el > 0)
k = utils.read_config_param(
    config["rad"], "k", lambda el : float(el), lambda el : el > 0)
N = utils.read_config_param(
    config["rad"], "N", lambda el : int(el), lambda el : el > 0)
D = utils.read_config_param(
    config["rad"], "D", lambda el : float(el), lambda el : el > 0)
Q = utils.read_config_param(
    config["rad"], "Q", lambda el : float(el), lambda el : el > 0)
v0 = utils.read_config_param(
    config["rad"], "v0", lambda el : float(el), lambda el : el > 0)

if dynamic_files is None:
    # Perform one analysis
    # python analysisRad.py
    anl.analyze_rad(dynamic_filename, algo, mass, k, N, D, Q, v0, plot_boolean, delta_t)
else:
    # 
    # python analysisRad.py beeman.txt verlet.txt gpc5.txt
    x_superlist = []
    y_superlist = []
    legend_list = []
    for filename in dynamic_files:
        # Expected filename format: ALGO-dt.txt
        name_data = filename[:-4].split('-', 1) # Take filename without .txt extension
        # TODO: Take params from filename
        metric = anl.analyze_rad(dynamic_filename, algo, mass, k, N, D, Q, v0, plot_boolean, delta_t)
        x_superlist.append(metric.time_vec)
        y_superlist.append(metric.algo_sol)
        legend_list.append(metric.algo)

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
