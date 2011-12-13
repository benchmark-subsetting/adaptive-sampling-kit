#include <stdio.h>
#include <assert.h>

#define RESOLUTION 0.00000000001

int try_delta(double delta, int vs, int ss, int * variance, 
	      int * samples, double * dist) {
    int i,j;
    /* Always select the first sample (largest variance) */
    samples[0] = variance[0]-1;
    int count = 1;

    for (i = 1; i < vs; i++) {
	int next = variance[i]-1;
        /* Check that the next point distance to all other sampled points
	 * is above the threshold */
	int ok = 1;
	for (j=0; j < count; j++) {
	    if (dist[next+samples[j]*vs] < delta) {
	       ok = 0;
	       break;
	    }
	}

	/* If that is not the case continue to next point */
	if (!ok) continue;

        /* If that is the case, add the point to the selected samples list */
        samples[count] = next;
        count++;

        /* Did we select all the needed samples ? */
        if (count == ss) {
	    printf("last position = %d\n", i);
	    if (i==vs-1) return 0;
	    else return 1;
            /* We reached ss points, we need to increase delta */
        }
    }

    /* We did not reach enough points, we need to decrease delta */
    return -1;
}

void uniform_sampling(int * vsize, int * ssize, int *variance,  
		      int * samples, double * dist, double *max_distance) {
    int vs = vsize[0];
    int ss = ssize[0];
    double max_delta = max_distance[0];
    double min_delta = 0;

    /* Find optimal delta by dichotomy */
    while(1) {

        double delta = (max_delta + min_delta) / 2.0 ;
        if ( (max_delta - min_delta)  < RESOLUTION) {
            int decision = try_delta(min_delta, vs, ss, variance, samples, dist);
            assert(decision >= 0);
            return;
        }
        printf("Trying delta %lE\n", delta);
        int decision = try_delta(delta, vs, ss, variance, samples, dist);
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

/*
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
*/
