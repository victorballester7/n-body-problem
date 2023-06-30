#ifndef MISC_H
#define MISC_H

// -----------------------------------------------------
// dist
// -----------------------------------------------------
// Purpose:
// 	Compute the distance between two points in R^dim
//
// Parameters:
// 	u: first point
// 	v: second point
// 	dim: dimension of the space
//
// Returns:
// 	The distance between u and v
// -----------------------------------------------------
double dist(double u[], double v[], int dim);

// -----------------------------------------------------
// write_vector
// -----------------------------------------------------
// Purpose:
// 	Write a vector to stdout
//
// Parameters:
// 	v: vector to be written
// 	dim: dimension of the vector
// ---------------------------------------------------
void write_vector(double v[], int dim);

// -----------------------------------------------------
// com
// -----------------------------------------------------
// Purpose:
// 	Compute the center of mass of a system of bodies
//
// Parameters:
// 	dim: dimension of the space
// 	num_steps: number of times the flow is computed at times 0, h, 2h, ..., (numSteps - 1)h
// 	n_bodies: number of bodies in the system
// 	r: array of positions of the bodies
// 	mass: array of masses of the bodies
//
// Returns:
// 	The center of mass of the system
// -----------------------------------------------------
double* com(int dim, int num_steps, int n_bodies, double r[], double mass[]);

#endif
