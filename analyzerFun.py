import math
import utils
import objects as obj

def exact_solution(t, mass, k, gamma, amp):
    return amp * math.exp(-t * gamma / (2 * mass)) * math.cos(t * math.sqrt(k / mass - gamma * gamma / (4 * mass * mass)))

def analyze_osc(dynamic_filename, algo, mass, k, gamma, amp, plot_boolean, delta_t):
    dynamic_file = open(dynamic_filename, "r")

    # Initial values
    restart = True
    p_id = 0
    
    time_vec = []
    exact_sol = []
    algo_sol = []
    ecm_sum = 0

    for linenum, line in enumerate(dynamic_file):
        if restart:
            time = float(line.rstrip())
            # Reset variables
            restart = False
            p_id = 0
            continue
        if "*" == line.rstrip():
            restart = True
            continue

        line_vec = line.rstrip().split(' ') # x vx
        # (id, x=0, vx=0, r=0, m=0):
        part = obj.Particle1D(p_id, float(line_vec[0]), float(line_vec[1]), 0, mass)
        time_vec.append(time)
        algo_sol.append(part.x)
        exact_sol.append(exact_solution(time, mass, k, gamma, amp))

        # Save Error cuadratico sum
        ecm_sum += (algo_sol[-1] - exact_sol[-1]) ** 2

        p_id += 1

    # Close files
    dynamic_file.close()

    # Calculate ECM
    ecm = ecm_sum / len(exact_sol)
    print(f'ECM for {algo} with dt {delta_t} = {ecm:.7E}\n')

    # Plot values
    if plot_boolean:
        # Initialize plotting
        utils.init_plotter()

        # Plot real trajectory with estimated one
        utils.plot_multiple_values(
            [time_vec, time_vec],
            'tiempo (s)',
            [exact_sol, algo_sol],
            'posición (m)',
            ['Analítica', algo],
            sci=False
        )

        # Hold execution
        utils.hold_execution()
    
    return obj.AnalysisOsc(algo, delta_t, time_vec, exact_sol, algo_sol, ecm)