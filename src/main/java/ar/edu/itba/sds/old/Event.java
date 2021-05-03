package ar.edu.itba.sds.old;

public class Event implements Comparable<Event> {
    private final double time;
    private final ParticleUnused particleUnused1;
    private final ParticleUnused particleUnused2;
    private final EventType type;

    private final int collisionCount1, collisionCount2;

    /**
     * General constructor to work as helper
     * @param time time of collision
     * @param particleUnused1 first particle to collide
     * @param particleUnused2 second particle to collide (can be null)
     * @param type type of collision
     */
    private Event(double time, ParticleUnused particleUnused1, ParticleUnused particleUnused2, EventType type) {
        this.time = time;
        this.particleUnused1 = particleUnused1;
        this.particleUnused2 = particleUnused2;
        this.type = type;

        this.collisionCount1 = particleUnused1.getCollisionCount();
        this.collisionCount2 = particleUnused2 != null ? particleUnused2.getCollisionCount() : 0;
    }

    /**
     * Create event involving two particles
     * @param time time of collision
     * @param particleUnused1 first particle to collide
     * @param particleUnused2 second particle to collide
     */
    public Event(double time, ParticleUnused particleUnused1, ParticleUnused particleUnused2) {
        this(time, particleUnused1, particleUnused2, EventType.TWO_PARTICLES);
    }

    /**
     * Create event involving a single particle and a wall
     * @param time time of collision
     * @param particleUnused1 particle to collide
     * @param vertical true if collision with vertical wall; false if collision with horizontal wall
     */
    public Event(double time, ParticleUnused particleUnused1, boolean vertical) {
        this(time, particleUnused1, null, vertical ? EventType.VERTICAL_WALL : EventType.HORIZONTAL_WALL);
    }

    public double getTime() {
        return time;
    }

    public ParticleUnused getParticle1() {
        return particleUnused1;
    }

    public ParticleUnused getParticle2() {
        return particleUnused2;
    }

    public boolean isWallType() {
        return type == EventType.VERTICAL_WALL || type == EventType.HORIZONTAL_WALL;
    }

    public void performEvent() {
        switch (type) {
            case TWO_PARTICLES:
                particleUnused1.bounce(particleUnused2);
                break;
            case VERTICAL_WALL:
                particleUnused1.bounceX();
                break;
            case HORIZONTAL_WALL:
                particleUnused1.bounceY();
                break;
        }
    }

    /**
     * @return true if the event HAS NOT been invalidated since creation
     *         false if the event HAS been invalidated since creation
     */
    public boolean isValid() {
        int curCollisionCount1 = particleUnused1.getCollisionCount();
        int curCollisionCount2 = particleUnused2 != null ? particleUnused2.getCollisionCount() : 0;

        return curCollisionCount1 == this.collisionCount1 &&
                curCollisionCount2 == this.collisionCount2;
    }

    @Override
    public int compareTo(Event o) {
        return Double.compare(time, o.time);
    }

    enum EventType {
        VERTICAL_WALL,
        HORIZONTAL_WALL,
        TWO_PARTICLES
    }

}
