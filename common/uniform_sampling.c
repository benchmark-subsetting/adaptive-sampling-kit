/* Copyright (c) 2011-2012, Universite de Versailles St-Quentin-en-Yvelines

  This file is part of ASK.  ASK is free software: you can redistribute
  it and/or modify it under the terms of the GNU General Public
  License as published by the Free Software Foundation, version 2.

  This program is distributed in the hope that it will be useful, but WITHOUT
  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
  details.

  You should have received a copy of the GNU General Public License along with
  this program; if not, write to the Free Software Foundation, Inc., 51
  Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
*/

#include <stdio.h>
#include <assert.h>

#define RESOLUTION 0.00000000001

int
try_delta(double delta, int vs, int ss, int *variance,
	  int *samples, double *dist)
{
    int i, j;
    /* Always select the first sample (largest variance) */
    samples[0] = variance[0] - 1;
    int count = 1;

    for (i = 1; i < vs; i++) {
	int next = variance[i] - 1;
	/* Check that the next point distance to all other sampled points
	 * is above the threshold */
	int ok = 1;
	for (j = 0; j < count; j++) {
	    if (dist[next + samples[j] * vs] < delta) {
		ok = 0;
		break;
	    }
	}

	/* If that is not the case continue to next point */
	if (!ok)
	    continue;

	/* If that is the case, add the point to the selected samples list */
	samples[count] = next;
	count++;

	/* Did we select all the needed samples ? */
	if (count == ss) {
	    printf("last position = %d\n", i);
	    if (i == vs - 1)
		return 0;
	    else
		return 1;
	    /* We reached ss points, we need to increase delta */
	}
    }

    /* We did not reach enough points, we need to decrease delta */
    return -1;
}

void
uniform_sampling(int *vsize, int *ssize, int *variance,
		 int *samples, double *dist, double *max_distance)
{
    int vs = vsize[0];
    int ss = ssize[0];
    double max_delta = max_distance[0];
    double min_delta = 0;

    /* Find optimal delta by dichotomy */
    while (1) {

	double delta = (max_delta + min_delta) / 2.0;
	if ((max_delta - min_delta) < RESOLUTION) {
	    int decision =
		try_delta(min_delta, vs, ss, variance, samples, dist);
	    assert(decision >= 0);
	    return;
	}
	printf("Trying delta %lE\n", delta);
	int decision = try_delta(delta, vs, ss, variance, samples, dist);
	if (decision == 0) {	/* All done */
	    break;
	} else if (decision == -1) {	/* decrease delta */
	    max_delta = delta;
	} else if (decision == 1) {	/* increase delta */
	    min_delta = delta;
	}
    }
}
