package ar.edu.itba.sds;

import ar.edu.itba.sds.objects.Event;
import ar.edu.itba.sds.objects.Particle;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.*;
import java.util.*;
import java.util.function.BiFunction;
import java.util.function.Predicate;
import java.util.stream.Collectors;

public class DampedOscillation {
    private static final String DEFAULT_CONFIG = "config.json";
    private static final String CONFIG_PARAM = "config";

    private static final String STATIC_CONFIG_KEY = "static_file";
    private static final String DYNAMIC_CONFIG_KEY = "dynamic_file";

    private static final String DELTA_T_SIM_CONFIG_KEY = "delta_t_sim";
    private static final String DELTA_T_PRINT_CONFIG_KEY = "delta_t_print";

    private static final String OSC_OBJECT_CONFIG_KEY = "osc";
    private static final String OSC_MASS_CONFIG_KEY = "mass";
    private static final String OSC_K_CONFIG_KEY = "k";
    private static final String OSC_GAMMA_CONFIG_KEY = "gamma";
    private static final String OSC_TF_CONFIG_KEY = "tf";
    private static final String OSC_R0_CONFIG_KEY = "r0";
    private static final String OSC_A_CONFIG_KEY = "A";

    private static final int ERROR_STATUS = 1;

    private static String staticFilename, dynamicFilename;
    private static double mass, k, gamma, amp;
    private static double r0, v0;
    private static double time = 0.0, timeFinal;
    private static double deltaTimeSim, deltaTimePrint;

    public static void main(String[] args) {
        // Get simulation params
        try {
            argumentParsing();
        } catch (ArgumentException e) {
            System.err.println(e.getMessage());
            System.exit(ERROR_STATUS);
            return;
        }
        v0 = -amp * gamma  / (2.0 * mass);

        final BiFunction<Double, Double, Double> f = (r, v) -> -k * r - gamma * v;

        // Measure simulation time
        long startTime = System.currentTimeMillis();

        // Simulation
        // TODO: Simulation

        // Print simulation time
        long endTime = System.currentTimeMillis();
        System.out.printf("Simulation time \t\t ⏱  %g seconds\n", (endTime - startTime) / 1000.0);
    }

    private static void argumentParsing() throws ArgumentException {
        Properties properties = System.getProperties();
        String configFilename = properties.getProperty(CONFIG_PARAM, DEFAULT_CONFIG);

        try(BufferedReader reader = new BufferedReader(new FileReader(configFilename))) {
            JSONObject config = new JSONObject(reader.lines().collect(Collectors.joining()));
            staticFilename = config.getString(STATIC_CONFIG_KEY);
            dynamicFilename = config.getString(DYNAMIC_CONFIG_KEY);
            deltaTimeSim = getConfigDouble(config, DELTA_T_SIM_CONFIG_KEY, v -> true);
            deltaTimePrint = getConfigDouble(config, DELTA_T_PRINT_CONFIG_KEY, v -> v % deltaTimeSim == 0);

            final JSONObject oscObject = config.getJSONObject(OSC_OBJECT_CONFIG_KEY);
            mass = getConfigDouble(oscObject, OSC_MASS_CONFIG_KEY, v -> v > 0);
            k = getConfigDouble(oscObject, OSC_K_CONFIG_KEY, v -> v > 0);
            gamma = getConfigDouble(oscObject, OSC_GAMMA_CONFIG_KEY, v -> v > 0);
            timeFinal = getConfigDouble(oscObject, OSC_TF_CONFIG_KEY, v -> v > 0);
            r0 = getConfigDouble(oscObject, OSC_R0_CONFIG_KEY, v -> true);
            amp = getConfigDouble(oscObject, OSC_A_CONFIG_KEY, v -> v > 0);
        } catch (FileNotFoundException e) {
            throw new ArgumentException(String.format("Config file %s not found", configFilename));
        } catch (IOException e) {
            throw new ArgumentException("Error parsing config file");
        } catch (JSONException e) {
            throw new ArgumentException("Missing configurations in config file. Must define \"static_file\", \"dynamic_file\" and \"osc\".");
        }
    }

    private static double getConfigDouble(JSONObject config, String key, Predicate<Double> validator) throws ArgumentException {
        double value;
        try {
            value = config.getDouble(key);
            if (!validator.test(value)) throw new NumberFormatException();
        } catch (NumberFormatException e) {
            throw new ArgumentException(String.format("Invalid %s number", key));
        }
        return value;
    }
}
