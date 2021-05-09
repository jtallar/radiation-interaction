# Damped Oscillator + Radiation Interaction

## What to Install
- `python3 -m pip install numpy`
- `python3 -m pip install matplotlib`
- Download and install OVITO from: https://www.ovito.org/
### Versions
`python 3.8`

## Configuration
Everything is configured by modifying `config.json`. Available configuration keys are:
   - `dynamic_file`: dynamic file filepath
   - `simulation_file`: animation file filepath
   - `osc`: configurations for damped oscillator
      - `algo`: name of the algorithm to use
      - `mass`: particle mass
      - `k`: coefficient of the restoring force
      - `gamma`: characteristic gamma quantity
      - `tf`: end time of simulation
      - `r0`: initial position
      - `A`: oscillator amplitude
   - `rad`: configurations for radiation interaction system
      - `algo`: name of the algorithm to use
      - `mass`: particle mass
      - `k`: Coulomb's constant
      - `N`: number of static particles per dimension (NxN matrix)
      - `D`: distance between static particles
      - `Q`: particle charge
      - `v0`: particle initial horizontal velocity
      - `use_seed`: if true use fixed seed, if false use nanoseconds
      - `seed`: fixed seed value
   - `delta_t_sim`: timestep between simulation measurements
   - `delta_t_print`: timestep between simulation prints to file
   - `delta_t_anim`: timestep between animation prints to file
   - `plot`: determines whether to plot or not single analysis, must be true or false

# Damped Oscillator

## Simulation
To generate executable and run damped oscillator simulation
1. Run `./prepare.sh` in root to generate executables (only required once).
2. Run `./target/tp4-simu-1.0/damped-osc.sh -Dalgo=algo -Ddt=dt`. Parameters from `config.json` can be overwritten by using `algo` and `dt` properties.

Output will be printed to `dynamic_file`, showing time and particle position and velocity for each timestep.

## Analysis Tools

### analysisOsc.py
Generate plots and metrics given a single simulation file as input.
Run `python3 analysisOsc.py [file_1 file_2 ...]`, using parameters from `config.json`.

If one or more filenames are provided, analysis will be performed individually and then condensed for multiple simulations. This can be used to provide one simulation file for each available algorithm. If plot is false, then no graphs are plotted.

Metrics calculated for each simulation are:
- ECM

Plots shown are:
- Analytic trajectory + estimated trajectory for each simulation file.

### multipleDtOsc.sh
This script can be used to run simulation multiple times, given a starting timestep value, a step to increase dt each iteration and a maximum dt.
`./multipleDtOsc.sh dt_start dt_step dt_end`

The script runs three simulations for each available dt from `dt_start` to the highest `dt_start + K * dt_step` that is lower or equal than `dt_end` using Verlet, Beeman and Gear Predictor-Corrector 5 respectively. Then, it runs `analysisOsc.py` with the three output datafiles as parameters.

### aux_analysisOscDelta.py
Contains obtained values using the previously mentioned script. It is used to plot ECM = f(dt) for the three algorithms at once. Values should be copied manually to the corresponding lists.

## Animation Tool
Generates `simu.xyz` using information from `static_file` and `dynamic_file`.
Run `python3 animator.py`, using the following parameters from `config.json`:

   `static_file`, `dynamic_file`, `delta_time_animation`, `max_v_mod`

To view the animation, you must open `simu.xyz` with Ovito:
`./bin/ovito simu.xyz`. 

Particles will be colored in a scale of colors from cian (static particles) to red (high velocity module), showing how fast each particle is going.

### Column Mapping 
Configure the file column mapping as follows:
   - Column 1 - Radius
   - Column 2 - Position - X
   - Column 3 - Position - Y
   - Column 4 - Particle Identifier
   - Column 5 - Color - R
   - Column 6 - Color - G
   - Column 7 - Color - B

# Analysis Tools
Analysis can be performed in multiple ways.

## analysis.py
Generate plots and metrics given a single simulation file as input.
Run `python3 analysis.py [out_filename]`, using the following parameters from `config.json`:

   `static_file`, `dynamic_file`, `delta_time_analysis`, `delta_time_intercollition`, `delta_v_mod`, `max_v_mod`, `small_dcm_count`, `plot`

If a filename is provided, some metrics will be written to filename. If plot is false, then no graphs are plotted.

Metrics calculated are:
- Small DCM D (single simulation)
- Collision count
- Collision frequency
- Average time between collisions
- Kinetic energy

Plots shown are:
- Small particles DCM dependant on time for last half
- Probability distribution of times between collisions
- Initial probability distribution of |v|
- Probability distribution of |v| in last third of simulation
- Big particle trajectory (with and without zooming in)

## multipleAnalysis.py
Run analysis on multiple simulation files to plot metrics according to the different iterations or values. It receives a root directory, where each folder should correspond to a parameter value (eg: `101`) with multiple data simulations of that value.
`python3 multipleAnalysis.py root_directory (N|T) [save_dir]`

The second parameter indicates mode, whether simulations have a varying number of small particles (N) or temperature (T, by changing initial `max_v_mod`). If save_dir is provided, the plots are saved as `.png` in that directory.

If mode is N, plots shown are:
- Big particle trajectory, taking one repetition for each N
- Collision count dependant on N
- Collision frequency dependant on N
- Average time between collisions dependant on N

If mode is T, plots shown are:
- Big particle trajectory, taking one repetition for each T
- Small particles DCM D value dependant on initial max_v_mod
- Big particle DCM dependant on time for `max_v_mod` = 2.0, for last half of simulation
- Big particle DCM D value dependant on initial max_v_mod
- Small particles DCM dependant on time for `max_v_mod` = 2.0, for last half of simulation
- Small particles DCM D value dependant on initial max_v_mod

### multipleN.sh
This script can be used to run generation and simulation multiple times, given a starting N value, a step to increase N each iteration and the number of repetitions (>= 2) to run for each N in range.
`./multipleN.sh N_start N_step repetitions`

The script runs the simulation for each available N from `N_start` to the highest `N_start + K * N_step` that is lower or equal than 136. Then, it runs `multipleAnalysis.py` with the output data directory. The plots can be found at directory `pics_N`. Values corresponding to each plot can also be found at file `pics_N/outN.txt`.

### multipleT.sh
This script can be used to run generation and simulation multiple times, given a starting max velocity module value, a step to increase module each iteration, a maximum module and the number of repetitions (>= 2) to run for each module in range.
`./multipleT.sh max_v_mod_start max_v_mod_step max_v_mod_stop repetitions`

The script runs the simulation for each available velocity module from `max_v_mod_start` to the highest `max_v_mod_start + K * max_v_mod_step` that is lower or equal than `max_v_mod_stop`. Then, it runs `multipleAnalysis.py` with the output data directory. The plots can be found at directory `pics_T`. Values corresponding to each plot can also be found at file `pics_T/outN.txt`.