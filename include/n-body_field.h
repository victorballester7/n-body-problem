#ifndef N_BODY_FIELD_H
#define N_BODY_FIELD_H

typedef struct n_body_params {
  int dim;     // dimension of the space (2 or 3)
  double *m;   // masses
  double G;    // gravitational constant
  double EPS;  // softening parameter
} n_body_params;

// -----------------------------------------------------
// integration
// -----------------------------------------------------
// Purpose:
// 	Compute the flow of a system of n bodies numSteps times using the RK78 method
//
// Parameters:
// 	numSteps: number of times the flow is computed at times 0, h, 2h, ..., (numSteps - 1)h
// 	x: initial conditions
// 	m: masses
// 	h: initial step size
// 	hmin: minimum step size
// 	hmax: maximum step size
// 	tol: tolerance for the RK78 method
// 	maxNumStepsFlow: maximum number of steps for the RK78 method
// 	n_bodies: number of bodies
// 	dim: dimension of the space (2 or 3)
// 	G: gravitational constant
// 	EPS: softening parameter
//
// Returns:
// 	pointer to the array of the flow at times 0, h, 2h, ..., (numSteps - 1)h
// -----------------------------------------------------
double *integration(int numSteps, double x[], double m[], double h, double hmin, double hmax, double tol, int maxNumStepsFlow, int n_bodies, int dim, double G, double EPS);

// -----------------------------------------------------
// n-body field
// -----------------------------------------------------
// Purpose:
// 	Compute the n-body field at a given point
//
// Parameters:
// 	n: dimension of the field = 2 * 2 * n_bodies (in R^2) or 3 * 2 * n_bodies (in R^3)
// 	t: time at the integration preces (not used in the equations, but necessary to pass to the RK78)
// 	x: point at which the field is evaluated
// 	f: output field
// 	param: pointer to the parameters of the system (masses, gravitational constant)
//
// Returns:
// 	0 if everything went fine
//  1 if otherwise
// -----------------------------------------------------
int n_body_field(int n, double t, double x[], double f[], void *param);

#endif
