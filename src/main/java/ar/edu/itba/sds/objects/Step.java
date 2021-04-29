package ar.edu.itba.sds.objects;

public class Step {
    private final double time;
    private final double pos;
    private final double vel;
    private final double acc;

    public Step(double time, double pos, double vel, double acc) {
        this.time = time;
        this.pos = pos;
        this.vel = vel;
        this.acc = acc;
    }

    public double getTime() {
        return time;
    }

    public double getPos() {
        return pos;
    }

    public double getVel() {
        return vel;
    }

    public double getAcc() {
        return acc;
    }
}
