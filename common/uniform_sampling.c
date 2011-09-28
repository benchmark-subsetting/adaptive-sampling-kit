#include <stdio.h>
#include <assert.h>

/* When finding the delta, we stop when the last selected point position is whithin
   PRECISION % of the last available point
*/
#define PRECISION 10


#define RESOLUTION 0.000000001

int try_delta(double delta, int vs, int ss, double * variance, int * samples) {
    int i;
    /* Always select the first sample (largest variance) */
    samples[0] = 0;
    int count = 1;
    /* The next point must be below variance[0] - delta */
    double below = variance[0] - delta;

    for (i = 1; i < vs; i++) {
        /* Find the next point below the threshold */
        if (variance[i] >= below) continue;

        /* Update threshold */
        below = variance[i]-delta;

        /* Add the point to the selected samples list */
        samples[count] = i;
        count++;

        /* Did we select all the needed samples ? */
        if (count == ss) {
            double within = ((float)(vs - i) * 100.0)/(float)i ;
            /* If PRECISION is reached, finish dichotomy */
            printf("within = %E\n",within);
            if (within < PRECISION) return 0;
            /* else we need to increase delta */
            else return 1;
        }
    }

    /* We did not reach enough points, we need to decrease delta */
    return -1;
}

void uniform_sampling(int * vsize, int * ssize, double * variance, int * samples) {
    int vs = vsize[0];
    int ss = ssize[0];
    double max_delta = variance[0] - variance[vs-1];
    double min_delta = 0;

    /* Find optimal delta by dichotomy */
    while(1) {

        double delta = (max_delta + min_delta) / 2.0 ;
        if ( (max_delta - min_delta)  < RESOLUTION) {
            int decision = try_delta(min_delta-RESOLUTION, vs, ss, variance, samples);
            assert(decision >= 0);
            return;
        }
        printf("Trying delta %lE\n", delta);
        int decision = try_delta(delta, vs, ss, variance, samples);
        if (decision == 0 ) /* All done */
        {
            break;
        }
        else if (decision == -1) /* decrease delta */
        {
            max_delta = delta;
        }
        else if (decision == 1) /* increase delta */
        {
            min_delta = delta;
        }
    }
}

int main() {
    int vsize = 5;
    int ssize = 3;
    double variance[] = {0.5,0.4,0.3,0.2,0.1};
    int samples[] = {-1,-1,-1};

    uniform_sampling(&vsize, &ssize, variance, samples);

    int i;
    for (i=0; i< ssize; i++) {
        printf("%d ", samples[i]);
    }

    printf("\n");

}
