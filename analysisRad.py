import sys
import json

import utils
import analyzerFun as anl

import statistics as sts
import objects as obj

def build_error_mult(dt, err_list):
    err_mean = []
    err_std = []
    time_list = []
    finished = False
    time_index = 0
    while not finished:
        cur_t_err_list = []
        for i in range(len(err_list)):
            if time_index >= len(err_list[i]):
                finished = True
                break
            cur_t_err_list.append(err_list[i][time_index])
        
        if not finished:
            err_mean.append(sts.mean(cur_t_err_list))
            err_std.append(sts.stdev(cur_t_err_list))
            time_list.append(dt * (time_index + 1))

        time_index += 1
    
    return time_list, err_mean, err_std

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

if dynamic_files is None or len(dynamic_files) == 1:
    # Perform one analysis
    # python analysisRad.py
    anl.analyze_rad(dynamic_filename, algo, mass, k, N, D, Q, v0, plot_boolean, delta_t)
else:
    # Analyze multiple dts with same v0 --> |ET(0)-ET(t)| = f(t)
    #   python analysisRad.py BEEMAN_1.00000E-15_100000_1.txt BEEMAN_1.00000E-14_100000_2.txt
    # Or perform multiple iterations of same params (dt & v0)
    #   python analysisRad.py BEEMAN_1.00000E-15_10000_1.txt BEEMAN_1.00000E-15_10000_2.txt
    err_x_superlist = []
    err_y_superlist = []
    dt_legend_list = []

    pos_x_superlist = []
    pos_y_superlist = []

    dt_err_dic = {}

    ending_dict = {
        obj.EndingReason.TopWall: 0,
        obj.EndingReason.RightWall: 0,
        obj.EndingReason.BottomWall: 0,
        obj.EndingReason.LeftWall: 0,
        obj.EndingReason.Collision: 0
    }
    err_sum_list = []
    l_tot_list = []
    step_list = []
    for filename in dynamic_files:
        # Expected filename format: ALGO_dt_v0.txt
        print(filename)
        name_data = filename[:-4].split('_') # Take filename without .txt extension
        metric = anl.analyze_rad(filename, name_data[0].lower(), mass, k, N, D, Q, float(name_data[2]), False, float(name_data[1]))
        # Save specific value vars
        err_sum_list.append(metric.energy_diff_sum)
        l_tot_list.append(metric.trajectory_total)
        step_list.append(len(metric.time_vec) - 1)
        ending_dict[metric.ending_motive] += 1
        # Save plotting value vars
        err_x_superlist.append(metric.time_vec[1:])
        err_y_superlist.append(metric.energy_diff_vec)
        dt_legend_list.append(metric.dt)
        pos_x_superlist.append(metric.pos_x_list)
        pos_y_superlist.append(metric.pos_y_list)
        # Save energy_diff_vec per dt
        if metric.dt not in dt_err_dic:
            dt_err_dic[metric.dt] = []
        dt_err_dic[metric.dt].append(metric.energy_diff_vec)
    
    err_sum = obj.FullValue(sts.mean(err_sum_list), sts.stdev(err_sum_list))
    l_tot = obj.FullValue(sts.mean(l_tot_list), sts.stdev(l_tot_list))
    steps = obj.FullValue(sts.mean(step_list), sts.stdev(step_list))

    multiple_rep_dt = True
    dt_sum_err_x_superlist = []
    dt_sum_err_mean_superlist = []
    dt_sum_err_std_superlist = []
    dt_sum_legend_list = []
    for dt, err_list in dt_err_dic.items():
        if len(err_list) == 1:
            multiple_rep_dt = False
            break
        time_list, err_mean, err_std = build_error_mult(dt, err_list)
        dt_sum_err_x_superlist.append(time_list)
        dt_sum_err_mean_superlist.append(err_mean)
        dt_sum_err_std_superlist.append(err_std)
        dt_sum_legend_list.append(dt)

    print(f'Last V0 = {metric.v0} ; Last dt = {metric.dt}\n'
          f'Error sum = {err_sum}\n'
          f'L total = {l_tot}\n'
          f'Steps = {steps}\n'
          f'Ending dictionary: {ending_dict}\n')
    
    if plot_boolean:
        # Initialize plotting
        utils.init_plotter()

        # Plot multiple |ET(0)-ET(t)| = f(t) for different dts
        utils.plot_multiple_values(
            err_x_superlist, 'tiempo (s)',
            err_y_superlist, 'diferencia de ET(t) con ET(0) (J)',
            dt_legend_list, sci_x=True, log_y=True, precision=0
        )

        if multiple_rep_dt:
            # Plot errorbars for |ET(0)-ET(t)| = f(t) for different dts
            utils.plot_multiple_error_bars(
                dt_sum_err_x_superlist, 'tiempo (s)', 
                dt_sum_err_mean_superlist, 'diferencia de ET(t) con ET(0) (J)', 
                dt_sum_err_std_superlist, dt_sum_legend_list,
                sci_x=True, log_y=True, x_prec=1, y_prec=0
            )

        Lx, Ly = 16 * D, 15 * D
        # Build static particle list
        static_x = []
        static_y = []
        static_c = []
        for i in range(N):
            for j in range(N):
                static_x.append((i + 1) * D)
                static_y.append(j * D)
                static_c.append('red' if (i + j) % 2 == 0 else 'black')

        # Plot multiple particle trajectories full box size
        utils.plot_multiple_values_with_scatter(
            pos_x_superlist, 'X partícula incidente (m)', 
            pos_y_superlist, 'Y partícula incidente (m)', 
            dt_legend_list, precision=1, sci_x=True, min_val_x=0, max_val_x=Lx, min_val_y=0, max_val_y=Ly,
            scatter_superlist=[static_x, static_y, static_c]
        )

        # Hold execution
        utils.hold_execution()
