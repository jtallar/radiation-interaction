import sys
import json

import utils
import analyzerFun as anl

import statistics as sts
import objects as obj

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
    # Perform multiple iterations of same params (dt & v0)
    #   python analysisRad.py BEEMAN_1.00000E-15_10000_1.txt BEEMAN_1.00000E-15_10000_2.txt
    ending_dict = {}
    err_sum_list = []
    l_tot_list = []
    for filename in dynamic_files:
        # Expected filename format: ALGO_dt_v0.txt
        name_data = filename[:-4].split('_') # Take filename without .txt extension
        metric = anl.analyze_rad(filename, name_data[0].lower(), mass, k, N, D, Q, float(name_data[2]), False, float(name_data[1]))
        err_sum_list.append(metric.energy_diff_sum)
        l_tot_list.append(metric.trajectory_total)
        if metric.ending_motive not in ending_dict:
            ending_dict[metric.ending_motive] = 0
        ending_dict[metric.ending_motive] += 1
    
    err_sum = obj.FullValue(sts.mean(err_sum_list), sts.stdev(err_sum_list))
    l_tot = obj.FullValue(sts.mean(l_tot_list), sts.stdev(l_tot_list))

    print(f'Error sum = {err_sum}\n'
          f'L total = {l_tot}\n'
          f'Ending dictionary: {ending_dict}\n')
