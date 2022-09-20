#include <math.h>
#include <stdio.h>
#include <stdlib.h>

double dist(double u[], double v[], int dim) {
  double d = 0;
  for (int i = 0; i < dim; i++)
    d += pow(u[i] - v[i], 2);
  return sqrt(d);
}

// double* zero_vect(int dim) {
//   double* v = (double*)malloc(sizeof(double) * dim);
//   for (int i = 0; i < dim; i++)
//     v[i] = 0;
//   return v;
// }

double* n_body_eq(int dim, int n, double r_state[n * 2 * dim], double mass[n], double EPS) {
  int ncol = 2 * dim;
  double* X_dot = (double*)malloc(sizeof(double) * n * ncol);
  double xi[3], xk[3];
  for (int i = 0; i < n; i++) {    // bucle for the number of particles
    for (int r = 0; r < dim; r++)  // assignation of the position vector of the body i
      xi[r] = r_state[i * ncol + 2 * r];
    for (int j = 0; j < dim; j++) {                             // assignation of the rhs of the differential system
      X_dot[i * ncol + 2 * j] = r_state[i * ncol + 2 * j + 1];  // x_dot, y_dot or z_dot
      X_dot[i * ncol + 2 * j + 1] = 0;                          // vx_dot, vy_dot or vz_dot
      for (int k = 0; k < n; k++) {                             // sum of all the particles forces
        if (k == i)                                             // skip the particle itself
          continue;
        else {
          for (int r = 0; r < dim; r++)  // assignation of the position vector of the body k
            xk[r] = r_state[k * ncol + 2 * r];
          // if (i == 0 && p == 0) {
          //   printf("%i, %i, %i----%lf\n", i, j, k, -mass[k] * (xi[j] - xk[j]) / (pow(dist(xi, xk, dim), 3) + EPS));
          //   // printf("  mass = %lf\n  pos = %lf\n  denom = %lf\n", mass[k], xi[j] - xk[j], pow(dist(xi, xk, dim), 3) + EPS);
          // }
          X_dot[i * ncol + 2 * j + 1] += -mass[k] * (xi[j] - xk[j]) / (pow(dist(xi, xk, dim), 3) + EPS);
        }
      }
      // if (i == 0 && p == 0)
      //   printf("%lf\n\n", X_dot[i * ncol + 2 * j + 1]);
    }
  }
  return X_dot;
}

void write_vector(int dim, double v[]) {
  for (int i = 0; i < dim; i++)
    printf("%lf ", v[i]);
  puts(" ");
}

double* rk4(int num_steps, int dim, int n, double r_state[n * 2 * dim], double mass[n], double dt, double EPS) {
  int len = n * 2 * dim;
  // printf("dim = %i \n n = %i \n len = %i\n dt = %lf\n", dim, n, len, dt);
  // write_vector(n, mass);
  // write_vector(n * 2 * dim, r_state);
  double* r = (double*)malloc(sizeof(double) * (num_steps + 1) * len);
  double ri1[len], ri2[len], ri3[len], ri4[len];
  for (int i = 0; i < len; i++)  // assignation of the initial state
    r[i] = r_state[i];
  for (int i = 0; i < num_steps; i++) {  // loop for each state of the system
    // assignation of the k1 value from the rk4 method
    for (int j = 0; j < len; j++)
      ri1[j] = r[i * len + j];
    double* k1 = n_body_eq(dim, n, ri1, mass, EPS);

    // assignation of the k2 value from the rk4 method
    for (int j = 0; j < len; j++)
      ri2[j] = r[i * len + j] + dt * k1[j] / 2;
    double* k2 = n_body_eq(dim, n, ri2, mass, EPS);

    // assignation of the k3 value from the rk4 method
    for (int j = 0; j < len; j++)
      ri3[j] = r[i * len + j] + dt * k2[j] / 2;
    double* k3 = n_body_eq(dim, n, ri3, mass, EPS);

    // assignation of the k4 value from the rk4 method
    for (int j = 0; j < len; j++)
      ri4[j] = r[i * len + j] + dt * k3[j];
    double* k4 = n_body_eq(dim, n, ri4, mass, EPS);
    // ---------------------------------------------
    for (int j = 0; j < len; j++)  // assignation of the new state
      r[(i + 1) * len + j] = r[i * len + j] + dt / 6 * (k1[j] + 2 * k2[j] + 2 * k3[j] + k4[j]);
  }
  return r;
}

double* com(int num_steps, int dim, int n, double r[(num_steps + 1) * 2 * dim * n], double mass[n]) {
  int len = n * 2 * dim;
  double* com = (double*)malloc(sizeof(double) * (num_steps + 1) * dim);
  double M = 0;
  for (int i = 0; i < n; i++)
    M += mass[i];
  for (int i = 0; i < num_steps + 1; i++) {
    for (int j = 0; j < dim; j++) {
      com[i * dim + j] = 0;
      for (int k = 0; k < n; k++)
        com[i * dim + j] += r[i * len + k * 2 * dim + 2 * j] * mass[k] / M;
    }
  }
  return com;
}