package ar.edu.itba.sds.algos;

import java.util.function.BiFunction;

public class Beeman {
    private final double[] pos;
    private final double[] vel;
    private final double[] acc;
    private final BiFunction<Double, Double, Double> f;
    private final double deltaT;
    private double time;
    private int nextIndex;

    public Beeman(BiFunction<Double, Double, Double> f, double deltaT, double tf, double r0, double v0) {
        int size = (int) Math.round(tf / deltaT) + 1;

        this.pos = new double[size];
        this.pos[0] = r0;
        this.vel = new double[size];
        this.vel[0] = v0;
        this.acc = new double[size];
        this.acc[0] = f.apply(r0, v0);

        this.f = f;
        this.deltaT = deltaT;
        this.time = 0.0;
        this.nextIndex = 1;
    }


}
