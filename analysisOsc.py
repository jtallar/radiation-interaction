import sys
import json

import utils
import analyzerFun as anl

# Read out filename param if provided
out_filename = None
if len(sys.argv) >= 2:
    out_filename = sys.argv[1]

# Read params from config.json
with open("config.json") as file:
    config = json.load(file)

if "osc" not in config:
    invalid_param("osc")

dynamic_filename = utils.read_config_param(
    config, "dynamic_file", lambda el : el, lambda el : True)
plot_boolean = utils.read_config_param(
    config, "plot", lambda el : bool(el), lambda el : True)
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

metrics = anl.analyze_osc(dynamic_filename, algo, mass, k, gamma, amp, plot_boolean)

# If out filename provided, print to file
if out_filename:
    with open(out_filename, "w") as file:
        file.write(
            f'{metrics.N}\n'
            f'{init_max_v_mod}\n'
            f'{metrics.collision_count}\n'
            f'{metrics.collision_freq}\n'
            f'{metrics.avg_intercollision_time:.7E}\n'
            f'{metrics.kinetic_energy:.7E}\n'
        )