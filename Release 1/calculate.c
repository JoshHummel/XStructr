#include <stdio.h>
#include <math.h>
#include <stdlib.h>

const double PI = 3.141592653589793238463;
const double ELEC_CONST = 8.99 * 10e9;
const double ELEC_CHRG = 1.602176634 * 10e-19;

typedef struct Vector {
    double x;
    double y;
    double z;
}Vector;

Vector vec_add(Vector one, Vector two) {
    Vector result;
    double xr = one.x + two.x;
    double yr = one.y + two.y;
    double zr = one.z + two.z;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

Vector vec_sub(Vector one, Vector two) {
    Vector result;
    double xr = one.x - two.x;
    double yr = one.y - two.y;
    double zr = one.z - two.z;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

Vector vec_mul(Vector one, Vector two) {
    Vector result;
    double xr = one.x * two.x;
    double yr = one.y * two.y;
    double zr = one.z * two.z;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

Vector vec_div(Vector one, Vector two) {
    Vector result;
    double xr = one.x / two.x;
    double yr = one.y / two.y;
    double zr = one.z / two.z;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

Vector vec_scale_div(Vector one, double two) {
    Vector result;
    double xr = one.x / two;
    double yr = one.y / two;
    double zr = one.z / two;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

Vector vec_scale_mul(Vector one, double two) {
    Vector result;
    double xr = one.x * two;
    double yr = one.y * two;
    double zr = one.z * two;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

double vec_len(Vector one) {
    return pow(pow(one.x, 2) + pow(one.y, 2) + pow(one.z, 2), 0.5);
}

Vector vec_norm(Vector one) {
    Vector result;
    double length = vec_len(one);
    result = vec_scale_div(one, length);
    return result;
}

Vector vec_abs(Vector one) {
    Vector result;
    result.x = fabs(one.x);
    result.y = fabs(one.y);
    result.z = fabs(one.z);
    return result;
}

void print_vec(Vector one) {
    printf("(%e, %e, %e)", one.x, one.y, one.z);
}

typedef struct Particle {
    double mass;
    double radius;
    double charge;
    Vector pos;
    Vector vel;
    Vector acc;
    Vector netf;
    Vector min_e_loc;
}Particle;

// Particle functions:

double distanceTo(Particle one, Particle two) {
    return sqrt((pow((one.pos.x - two.pos.x), 2) + pow((one.pos.y - two.pos.y), 2) + pow((one.pos.z - two.pos.z), 2)));
}

Vector vectorDist(Particle one, Particle two) {
    Vector result;
    double xr = one.pos.x - two.pos.x;
    double yr = one.pos.y - two.pos.y;
    double zr = one.pos.z - two.pos.z;
    result.x = xr;
    result.y = yr;
    result.z = zr;
    return result;
}

int isClose(Vector one, Vector two, double tol) {
    if (fabs(one.x - two.x) <= tol && fabs(one.y - two.y) <= tol && fabs(one.z - two.z) <= tol) {
        return 1;
    }
    else {
        return 0;
    }
}

/* Catch zero div issues
double get_ratio(double a, double b) {
    if (b == 0.0) {
        return 1.0;
    }
    else {return (a / b);}
}
*/

double get_phi(double x, double y){
    double phi;
    if (x == 0.0) {
        phi = PI / 2;
    }
    else {
        phi = atan2(y, x);
    }
    return phi;
}

double get_theta(double x, double y, double z) {
    double hyp = sqrt(pow(x, 2) + pow(y, 2));
    double theta;
    if (hyp == 0.0) {
        theta = PI / 2;
    }
    else {
        theta = atan2(z, hyp);
    }
    return theta;
}


int calculate_forces(char* filename, Particle particles[], int arr_len, double dt, double t) {
    FILE* file = fopen(filename, "w");
    if (file == NULL) {
        printf("File could not be opened for writing.\n");
        return 1;
    }

    unsigned long int time = 0;
    unsigned long int sim_len = (unsigned long int)(t / dt);
    
    if (log10(sim_len) > 5) {
        printf("Simulation length too long, keep Sim Length and CDT less than 6 orders of magnitude apart.\n");
        return 1;
    }

    int write_error;
    Vector netF, rvec, new_acc, new_vel, new_pos;
    double r, radius, sigma, A=0.9999999999999999, rho = 0.0000894873938456;
    double epsilon = 1.6567788 * 10e-21;
    double F, Fx, Fy, Fz;

    for (; time <= sim_len; time++) {

        for (int i = 0; i < arr_len; i++) {
            netF.x = 0.0, netF.y = 0.0, netF.z = 0.0;
            write_error = fprintf(file, "%e,%e,%e,", particles[i].pos.x, particles[i].pos.y, particles[i].pos.z);
            if (write_error < 1) {
                printf("Write error encountered.\n");
                return -1;
            }

            for (int j = 0; j < arr_len; j++) {
                if (i == j) {
                    continue;
                }

                r = distanceTo(particles[i], particles[j]);
                
                radius = (particles[i].radius + particles[j].radius);
                sigma = radius * 0.8908987181403393;

                // ionic interactions
                if (particles[j].charge != 0.0 && particles[i].charge != 0.0) {
                    F = ELEC_CONST * (particles[i].charge * particles[j].charge) * ((pow(r, -2))) - (A/rho) * exp((sigma-r)/rho);
                }
                else { // Van Der Waals interactions
                    F = (24 * epsilon / (pow(r, 2))) * (2*pow((sigma/r), 11) - pow((sigma/r), 5));
                }

                rvec = vectorDist(particles[i], particles[j]);

                netF.x += F * cos(get_phi(rvec.x, rvec.y));
                netF.y += F * sin(get_phi(rvec.x, rvec.y));
                netF.z += F * cos(get_theta(rvec.x, rvec.y, rvec.z));

            }
            particles[i].netf = netF;
        }

        for (int k = 0; k < arr_len; k++) {            
            // Verlet Integration Method
            new_pos = vec_add(vec_add(particles[k].pos, vec_scale_mul(particles[k].vel, dt)), vec_scale_mul(particles[k].acc, dt * dt * 0.5));
            new_acc = vec_scale_div(particles[k].netf, particles[k].mass);
            new_vel = vec_add(particles[k].vel, vec_scale_mul(vec_add(particles[k].acc, new_acc), dt * 0.5));

            particles[k].acc = new_acc;
            particles[k].vel = new_vel;
            particles[k].pos = new_pos;
        }

    write_error = fprintf(file, "\n");
    if (write_error < 1) {
        printf("Write error encountered.\n");
        return -1;
        }
    }
    fclose(file);
    return 0;
}   

int main(int argc, char* argv[]) {

    // ./calculate <dt> <t> <# of particles>

    if (argc != 4) {
        printf("Correct usage: ./calculate <dt> <t> <# of particles>");
        return 1;
    }

    float dt = pow(10, atof(argv[1]));
    float t = pow(10, atof(argv[2]));
    int num_part = atoi(argv[3]);
    printf("%lf, %lf, %d\n", dt, t, num_part);

    Vector pos;
    Vector vel;
    Vector acc;
    double mass;
    double radius;
    double charge;

    FILE* cfile = fopen("config.txt", "r");
    if (cfile == NULL) {
        printf("File could not be opened for reading.");
        return 1;
    }

    Particle* arr = malloc(num_part * sizeof(Particle));

    int i = 0;
    while (fscanf(cfile, "%lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf\n", &mass, &radius, &charge, &(pos.x), &(pos.y), &(pos.z), &(vel.x), &(vel.y), &(vel.z), &(acc.x), &(acc.y), &(acc.z)) == 12) {
        arr[i].mass = mass;
        arr[i].radius = radius;
        arr[i].charge = charge;
        arr[i].pos = pos;
        arr[i].vel = vel;
        arr[i].acc = acc;
        // fprintf(stdout, "Particle %d: (Mass: %lf), (Radius: %lf), (Charge: %d), (Pos: [%lf, %lf, %lf])\n", i, arr[i].mass, arr[i].radius, arr[i].charge, arr[i].pos.x, arr[i].pos.y, arr[i].pos.z);
        i++;
    }

    calculate_forces("data.txt", arr, num_part, dt, t);

    free(arr);

    return 0;
}