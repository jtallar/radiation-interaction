import math
import statistics as sts
import utils
import objects as obj

def exact_solution(t, mass, k, gamma, amp):
    return amp * math.exp(-(gamma / (2 * mass)) * t) * math.cos(math.sqrt(k / mass - gamma * gamma / (4 * mass * mass)) * t)

def analyze_osc(dynamic_filename, algo, mass, k, gamma, amp, plot_boolean, delta_t):
    dynamic_file = open(dynamic_filename, "r")

    # Initial values
    restart = True
    p_id = 0
    
    time_vec = []
    exact_sol = []
    algo_sol = []
    ecms = []

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
        ecms.append((algo_sol[-1] - exact_sol[-1]) ** 2)

        p_id += 1

    # Close files
    dynamic_file.close()

    # Calculate ECM
    ecm = sts.mean(ecms)
    ecm_dev = sts.stdev(ecms)
    print(f'ECM for {algo} with dt {delta_t:.10E} = {ecm:.10E}, dev = {ecm_dev:.10E}\n')

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
            sci_y=False
        )

        # Hold execution
        utils.hold_execution()
    
    return obj.AnalysisOsc(algo, delta_t, time_vec, exact_sol, algo_sol, ecm)

######################################################################################

def analyze_rad(dynamic_filename, algo, mass, k, N, D, Q, v0, plot_boolean, delta_t):
    dynamic_file = open(dynamic_filename, "r")

    Lx, Ly = 16 * D, 15 * D
    # Build static particle list
    static_particles = []
    for i in range(N):
        for j in range(N):
            static_particles.append(obj.Particle(
                    i * N + j, 
                    (i + 1) * D,
                    j * D,
                    q=Q if (i + j) % 2 == 0 else -Q
                ))

    # Initial values
    restart = True
    
    time_vec = []
    pos_x_list = []
    pos_y_list = []
    energy_diff_vec = []
    energy_diff_sum = 0
    trajectory_sum_interdist = []
    trajectory_sumdist = 0

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

        line_vec = line.rstrip().split(' ') # x y vx vy
        # (id, x=0, y=0, vx=0, vy=0, r=0, m=0, q=0)
        part = obj.Particle(
            p_id, float(line_vec[0]), float(line_vec[1]), 
            float(line_vec[2]), float(line_vec[3]), 0, mass, Q)
        time_vec.append(time)
        pos_x_list.append(part.x)
        pos_y_list.append(part.y)

        # Save energy values
        tot_energy = part.get_kinetic_energy() + part.get_potential_energy(static_particles, k)

        # Save interdistance value if time != 0
        # Save tot_energy dif if time != 0
        if time != 0:
            # Save interdistance value
            interdist = part.center_distance(prev_part)
            trajectory_sumdist += interdist
            trajectory_sum_interdist.append(trajectory_sumdist)

            # Save energy diff value
            energy_diff = abs(init_energy - tot_energy)
            energy_diff_sum += energy_diff
            energy_diff_vec.append(energy_diff)
        else:
            init_energy = tot_energy
            trajectory_sum_interdist.append(0)
        
        prev_part = part

    ending_motive = part.get_ending_reason(Lx, Ly)

    # Close files
    dynamic_file.close()

    print(f'V0 is {v0} with dt {delta_t:.10E}\n'
          f'Init total energy is {init_energy:.10E}\n'
          f'Total trajectory length = {trajectory_sumdist:.10E}\n'
          f'Total energy diff = {energy_diff_sum:.10E}\n'
          f'Avg energy diff = {energy_diff_sum / len(time_vec):.10E}\n'
          f'Final time = {time:.10E}\n'
          f'Ended by = {ending_motive} in {len(time_vec) - 1} steps\n')

    # Plot values
    if plot_boolean:
        # Initialize plotting
        utils.init_plotter()

        # Plot |ET(t=0) - ET(t>0)| = f(t) with log scale
        utils.plot_values(
            time_vec[1:], 'tiempo (s)', 
            energy_diff_vec, 'diferencia de ET(t) con ET(0) (J)',
            log=True, sci_x=True, precision=0
        )
        
        # Plot L = f(t) --> trajectory length
        utils.plot_values(
            time_vec, 'tiempo (s)', 
            trajectory_sum_interdist, 'longitud de trayectoria (m)',
            sci_x=True, precision=1
        )

        static_x = []
        static_y = []
        static_c = []
        for sp in static_particles:
            static_x.append(sp.x)
            static_y.append(sp.y)
            static_c.append('red' if sp.q > 0 else 'black')

        # Particle trayectory full box size
        utils.plot_values_with_scatter(
            pos_x_list, 'X partícula incidente (m)', 
            pos_y_list, 'Y partícula incidente (m)', 
            1, sci_x=True, min_val_x=0, max_val_x=Lx, min_val_y=0, max_val_y=Ly,
            scatter_superlist=[static_x, static_y, static_c]
        )

        # Hold execution
        utils.hold_execution()
    return obj.AnalysisRad(algo, delta_t, v0, init_energy, trajectory_sumdist, energy_diff_sum, ending_motive, time_vec, energy_diff_vec, trajectory_sum_interdist, pos_x_list, pos_y_list)