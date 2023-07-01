#include "../include/n-body_field.h"

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/misc.h"
#include "../include/rk78.h"

double *integration(int numSteps, double x[], double m[], double h, double hmin, double hmax, double tol, int maxNumStepsFlow, int n_bodies, int dim, double G, double EPS) {
  double *result = malloc(sizeof(double) * numSteps * dim * n_bodies);
  double t = 0;
  double T = h;
  int n = 2 * n_bodies * dim;
  n_body_params param = {dim, malloc(sizeof(double) * n_bodies), G, EPS};
  memcpy(param.m, m, sizeof(double) * n_bodies);  // masses
  for (int i = 0; i < n_bodies; i++)
    memcpy(result + i * dim, x + i * dim * 2, sizeof(double) * dim);
  // printf("Hola:\n");
  // for (int i = 0; i < n_bodies; i++)
  //   write_vector(result + i * dim, dim);
  for (int j = 1; j < numSteps; j++) {
    if (flow(&t, x, &h, T, hmin, hmax, tol, maxNumStepsFlow, n, n_body_field, &param)) {
      printf("Error in integration\n");
      exit(1);
    }
    for (int i = 0; i < n_bodies; i++)
      memcpy(result + j * dim * n_bodies + i * dim, x + i * dim * 2, sizeof(double) * dim);
  }
  return result;
}

int n_body_field(int n, double t, double x[], double f[], void *param) {
  // the field is ordered in x[] and f[] as x1, y1, z1, vx1, vy1, vz1, x2, y2, z2, vx2, vy2, vz2, ..., where the index i is the particle i-th. If the field is 2D, then the same order is used but without the z components.
  n_body_params *prm = (n_body_params *)param;
  // positions
  int N = 2 * prm->dim;
  int n_bodies = n / N;
  for (int i = 0; i < n_bodies; i++) {
    for (int j = 0; j < prm->dim; j++) {
      f[i * N + j] = x[i * N + prm->dim + j];  // position
      // velocity
      f[i * N + prm->dim + j] = 0;
      for (int k = 0; k < n_bodies && k != i; k++) {
        f[i * N + prm->dim + j] += -prm->G * prm->m[k] * (x[i * N + j] - x[k * N + j]) / (pow(dist(x + i * N, x + k * N, prm->dim), 3) + prm->EPS);  // velocity
      }
    }
  }
  return 0;
}
