package ar.edu.itba.sds;

import ar.edu.itba.sds.objects.Event;
import ar.edu.itba.sds.objects.Particle;
import org.json.JSONObject;
import org.json.JSONException;

import java.io.*;
import java.util.*;
import java.util.stream.Collectors;

public class BrownianMotion {
    private static final String DEFAULT_CONFIG = "config.json";
    private static final String CONFIG_PARAM = "config";

    private static final String STATIC_CONFIG_KEY = "static_file";
    private static final String DYNAMIC_CONFIG_KEY = "dynamic_file";
    private static final String MAX_EVENTS_CONFIG_KEY = "max_events";

    private static final int ERROR_STATUS = 1;

    private static String staticFilename, dynamicFilename;
    private static int maxEvents;
    private static int N;
    private static double L;
    private static double time = 0.0;

    public static void main(String[] args) {
        try {
            argumentParsing();
        } catch (ArgumentException e) {
            System.err.println(e.getMessage());
            System.exit(ERROR_STATUS);
            return;
        }

        // Measure file reading time
        long startTime = System.currentTimeMillis();

        // Parse static file
        double[] particleRadius, particleMass;
        int bigParticleIndex;
        try(BufferedReader reader = new BufferedReader(new FileReader(staticFilename))) {
            N = Integer.parseInt(reader.readLine());
            L = Double.parseDouble(reader.readLine());

            particleRadius = new double[N];
            particleMass = new double[N];

            // Fill radius and mass arrays
            bigParticleIndex = fillProperties(reader, particleRadius, particleMass);

        } catch (FileNotFoundException e) {
            System.err.println("Static file not found");
            System.exit(ERROR_STATUS);
            return;
        } catch (IOException e) {
            System.err.println("Error reading static file");
            System.exit(ERROR_STATUS);
            return;
        }

        // Parse dynamic file
        List<Particle> particles;
        Particle bigParticle;
        try(BufferedReader reader = new BufferedReader(new FileReader(dynamicFilename))) {
            // Set initial time
            time = Double.parseDouble(reader.readLine());
            // Create particle list
            particles = createParticleList(reader, particleRadius, particleMass);
            bigParticle = particles.get(bigParticleIndex);
        } catch (FileNotFoundException e) {
            System.err.println("Dynamic file not found");
            System.exit(ERROR_STATUS);
            return;
        } catch (IOException e) {
            System.err.println("Error reading dynamic file");
            System.exit(ERROR_STATUS);
            return;
        }

        // Print file parsing time
        long endTime = System.currentTimeMillis();
        System.out.printf("File parsing time \t\t ⏱  %g seconds\n", (endTime - startTime) / 1000.0);

        // Measure simulation time
        startTime = System.currentTimeMillis();

        // Simulation
        final Queue<Event> eventQueue = createQueueFromList(particles);
        int eventsTriggered = 0;
        while (!eventQueue.isEmpty() && eventsTriggered < maxEvents) {
            final Event event = eventQueue.poll();
            if (event.isValid()) {
                final double eventTime = event.getTime();
                // Advance all particles delta t
                particles.forEach(p -> p.advanceTime(eventTime - time));
                time = eventTime;
                // Write particle state to dynamic file
                try {
                    writeParticleState(particles);
                } catch (IOException e) {
                    System.err.println("Error writing dynamic file");
                    System.exit(ERROR_STATUS);
                    return;
                }
                // Check if big particle hit a wall
                if (bigParticleToWall(event, bigParticle)) break;
                // Update colliding particles velocities
                event.performEvent();
                // Determine future collisions
                addFutureCollisions(eventQueue, event.getParticle1(), particles); // If p1 collides with p2, it will be added twice
                addFutureCollisions(eventQueue, event.getParticle2(), particles); // Second time will be invalid when triggered
                // Add one to counter
                eventsTriggered++;
            }
        }

        // Print simulation time
        endTime = System.currentTimeMillis();
        System.out.printf("Simulation time \t\t ⏱  %g seconds\n", (endTime - startTime) / 1000.0);

        // Add trailing *
        try {
            appendToFile(dynamicFilename, "\n*");
        } catch (IOException e) {
            System.err.println("Error writing dynamic file");
            System.exit(ERROR_STATUS);
            return;
        }

        if (eventsTriggered == maxEvents)
            System.out.printf("Reached %d events, exiting...\n", maxEvents);
        else
            System.out.println("Big particle reached border, exiting...");
    }

    private static boolean bigParticleToWall(Event event, Particle bigParticle) {
        return event.isWallType() && event.getParticle1().equals(bigParticle);
    }

    private static void addFutureCollisions(Queue<Event> queue, Particle particle, List<Particle> particles) {
        if (particle == null) return;

        // Create vertical wall collision event
        Double tc = particle.collidesX(0, L);
        if (tc != null) queue.add(new Event(time + tc, particle, true));

        // Create horizontal wall collision event
        tc = particle.collidesY(0, L);
        if (tc != null) queue.add(new Event(time + tc, particle, false));

        for (Particle other : particles) {
            tc = particle.collides(other);
            if (tc != null) queue.add(new Event(time + tc, particle, other));
        }
    }

    private static void writeParticleState(List<Particle> particles)
            throws IOException {
        StringBuilder sb = new StringBuilder();
        sb.append(String.format("\n*\n%.7E", time));
        particles.forEach(p -> sb.append(String.format("\n%.7E %.7E %.7E %.7E", p.getX(), p.getY(), p.getVx(), p.getVy())));

        appendToFile(dynamicFilename, sb.toString());
    }

    private static void appendToFile(String filename, String s) throws IOException {
        try(BufferedWriter writer = new BufferedWriter(new FileWriter(filename, true))) {
            writer.write(s);
        }
    }

    private static Queue<Event> createQueueFromList(List<Particle> particles) {
        final Queue<Event> eventQueue = new PriorityQueue<>();
        Double tc;
        for (int i = 0; i < particles.size(); i++) {
            Particle cur = particles.get(i);
            // Create vertical wall collision event
            tc = cur.collidesX(0, L);
            if (tc != null) eventQueue.add(new Event(time + tc, cur, true));

            // Create horizontal wall collision event
            tc = cur.collidesY(0, L);
            if (tc != null) eventQueue.add(new Event(time + tc, cur, false));

            // Create two particle collision events
            for (int j = i + 1; j < particles.size(); j++) {
                Particle other = particles.get(j);
                tc = cur.collides(other);
                if (tc != null) eventQueue.add(new Event(time + tc, cur, other));
            }
        }
        return eventQueue;
    }

    private static List<Particle> createParticleList(BufferedReader reader, double[] radiusArray, double[] massArray)
            throws IOException {
        if (radiusArray.length != massArray.length) throw new IllegalArgumentException("Radius and mass array must be same sized!");

        List<Particle> particles = new ArrayList<>();

        for (int i = 0; i < radiusArray.length; i++) {
            String line = reader.readLine();
            if (line == null) throw new IOException();

            // Values has format (x, y, vx, vy)
            final String[] values = line.split(" ");
            double x = Double.parseDouble(values[0]), y = Double.parseDouble(values[1]);
            double vx = Double.parseDouble(values[2]), vy = Double.parseDouble(values[3]);

            particles.add(new Particle(i, x, y, vx, vy, radiusArray[i], massArray[i]));
        }

        // Check that there are no lines remaining
        if (reader.readLine() != null) throw new IOException();

        return particles;
    }

    /**
     * @param reader buffered reader from static file
     * @param radiusArray I/O array to fill with particle radius
     * @param massArray I/O array to fill with particle mass
     * @return index corresponding to big particle
     * @throws IOException if error parsing file or not enough lines
     */
    private static int fillProperties(BufferedReader reader, double[] radiusArray, double[] massArray)
            throws IOException {
        if (radiusArray.length != massArray.length) throw new IllegalArgumentException("Radius and mass array must be same sized!");

        double maxRadius = -1.0;
        int maxRadiusIndex = -1;
        for (int i = 0; i < radiusArray.length; i++) {
            String line = reader.readLine();
            if (line == null) throw new IOException();

            String[] props = line.split(" ");
            radiusArray[i] = Double.parseDouble(props[0]);
            massArray[i] = Double.parseDouble(props[1]);

            if (radiusArray[i] > maxRadius) {
                maxRadius = radiusArray[i];
                maxRadiusIndex = i;
            }
        }

        return maxRadiusIndex;
    }

    private static void argumentParsing() throws ArgumentException {
        Properties properties = System.getProperties();
        String configFilename = properties.getProperty(CONFIG_PARAM, DEFAULT_CONFIG);

        try(BufferedReader reader = new BufferedReader(new FileReader(configFilename))) {
            JSONObject config = new JSONObject(reader.lines().collect(Collectors.joining()));
            staticFilename = config.getString(STATIC_CONFIG_KEY);
            dynamicFilename = config.getString(DYNAMIC_CONFIG_KEY);
            try {
                maxEvents = config.getInt(MAX_EVENTS_CONFIG_KEY);
                if (maxEvents <= 0) throw new NumberFormatException();
            } catch (NumberFormatException e) {
                throw new ArgumentException("max_events number must be a positive number (max_events > 0)");
            }
        } catch (FileNotFoundException e) {
            throw new ArgumentException(String.format("Config file %s not found", configFilename));
        } catch (IOException e) {
            throw new ArgumentException("Error parsing config file");
        } catch (JSONException e) {
            throw new ArgumentException("Missing configurations in config file. Must define \"static_file\", \"dynamic_file\" and \"max_events\".");
        }
    }
}
