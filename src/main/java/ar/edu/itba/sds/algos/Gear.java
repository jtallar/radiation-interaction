package ar.edu.itba.sds.algos;

import ar.edu.itba.sds.objects.Step;

import java.lang.reflect.MalformedParameterizedTypeException;
import java.util.function.BiFunction;

public class Gear extends StepAlgorithm {
    protected double[] r3;
    protected double[] r4;
    protected double[] r5;
    protected double[] alpha;
    int R0 = 0;

    public Gear(BiFunction<Double, Double, Double> f, double deltaT, double tf, double r0, double v0, double mass, double k) {
        super(f, deltaT, tf, r0, v0, mass);
        this.alpha = new double[]{(3.0 / 16.0), (251.0 / 360), 1.0, (11.0 / 18.0), (1.0 / 6.0), (1.0 / 60.0)};
        this.acc[1] = (-k/mass) * (pos[1] - R0);
        this.r3 = new double[pos.length];
        this.r3[1] = (-k/mass) * vel[1];
        this.r4 = new double[pos.length];
        this.r4[1] = (-k/mass) * acc[1];
        this.r5 = new double[pos.length];
        this.r5[1] = (-k/mass) * r3[1];
    }

    @Override
    public Step next() {
        if (!hasNext()) throw new IndexOutOfBoundsException("No more timesteps!");

        double [][] r = {pos, vel, acc, r3, r4, r5};

        // Predict every r
        /*
        for (int i=0; i < r.length+1; i++)
            r[0][lastIndex+1] += r[i][lastIndex]*factor(deltaT,i);
        for (int i=1; i < r.length+1; i++)
            r[1][lastIndex+1] += r[i][lastIndex]*factor(deltaT,i-1);
        for (int i=2; i < r.length+1; i++)
            r[2][lastIndex+1] += r[i][lastIndex]*factor(deltaT,i-2);
        for (int i=3; i < r.length+1; i++)
            r[3][lastIndex+1] += r[i][lastIndex]*factor(deltaT,i-3);
        for (int i=4; i < r.length+1; i++)
            r[4][lastIndex+1] += r[i][lastIndex]*factor(deltaT,i-4);
        r[5][lastIndex+1] += r[5][lastIndex]*factor(deltaT,0);
        */

        for(int j = 0; j < r.length+1; j++)
            for (int i = j; i < r.length+1; i++)
                r[j][lastIndex+1] += r[i][lastIndex]*factor(deltaT,i-j);

        update(r);

        // Estimation Delta R2
        double deltaR2 = ((f.apply(pos[lastIndex + 1], vel[lastIndex + 1]) / mass ) - acc[lastIndex+1])
                        * factor(deltaT, 2);

        // Correct every r
        for(int i = 0; i < r.length+1; i++)
            r[i][lastIndex+1] = r[i][lastIndex+1] + alpha[i] * deltaR2 * factor(deltaT,i);

        update(r);

        // Update lastTime and lastIndex
        lastTime += deltaT;
        lastIndex++;
        return new Step(lastTime, pos[lastIndex], vel[lastIndex], acc[lastIndex]);
    }

    private double factor(double deltaT, int k){
        if(k==0) return 1;
        return Math.pow(deltaT,k)/factorial(k);
    }

    public int factorial (double n) {
        if (n==0)
            return 1;
        else
            return (int)(n * factorial(n-1));
    }

    public void update (double[][] r){
        pos[lastIndex+1] = r[0][lastIndex+1];
        vel[lastIndex+1] = r[1][lastIndex+1];
        acc[lastIndex+1] = r[2][lastIndex+1];
        r3[lastIndex+1] = r[3][lastIndex+1];
        r4[lastIndex+1] = r[4][lastIndex+1];
        r5[lastIndex+1] = r[5][lastIndex+1];
    }
}
