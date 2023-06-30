#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double dist(double u[], double v[], int dim) {
  double d = 0;
  for (int i = 0; i < dim; i++)
    d += (u[i] - v[i]) * (u[i] - v[i]);
  return sqrt(d);
}

void write_vector(double v[], int dim) {
  for (int i = 0; i < dim; i++) printf("%lf ", v[i]);
  puts(" ");
}

double* com(int dim, int num_steps, int n_bodies, double r[], double mass[]) {
  double* com = (double*)calloc(dim * num_steps, sizeof(double));  // initialize to 0
  double M = 0;
  for (int i = 0; i < n_bodies; i++) M += mass[i];
  for (int i = 0; i < num_steps; i++) {
    for (int j = 0; j < dim; j++) {
      for (int k = 0; k < n_bodies; k++)
        com[i * dim + j] += mass[k] * r[i * dim * n_bodies + k * dim + j];
      com[i * dim + j] /= M;
    }
  }
  return com;
}
