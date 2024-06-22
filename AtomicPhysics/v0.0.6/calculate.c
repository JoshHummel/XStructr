#include <stdio.h>
#include <math.h>
#include <stdlib.h>

const double PI = 3.141592653589793238463;

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

void print_vec(Vector one) {
    printf("(%e, %e, %e)", one.x, one.y, one.z);
}

typedef struct Particle {
    double mass;
    double radius;
    Vector pos;
    Vector vel;
    Vector acc;
    Vector netf;
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

    int time = 0;
    int sim_len = (int)(t / dt);
    int write_error;
    Vector netF, rvec, new_acc, new_vel, new_pos;
    double r, radius, sigma;
    double epsilon = 10e50;
    double F, Fx, Fy, Fz;

    for (; time <= sim_len; time++) {
        write_error = fprintf(file, "%lf,", time * dt);
        if (write_error < 1) {
            printf("Write error encountered.\n");
            return -1;
        }

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
                radius = (particles[i].radius + particles[j].radius) / 2;
                sigma = radius * 0.8908987181403393;

                F = (24 * epsilon / (pow(r, 2))) * (2*pow((sigma/r), 11) - pow((sigma/r), 5));

                rvec = vectorDist(particles[i], particles[j]);

                Fx = F * cos(get_phi(rvec.x, rvec.y));
                Fy = F * sin(get_phi(rvec.x, rvec.y));
                Fz = F * cos(get_theta(rvec.x, rvec.y, rvec.z));

                netF.x += Fx;
                netF.y += Fy;
                netF.z += Fz;
            }
            particles[i].netf = netF;
        }

        for (int k = 0; k < arr_len; k++) {
            new_acc = vec_scale_div(particles[k].netf, particles[k].mass);
            new_vel = vec_add(particles[k].vel, vec_scale_mul(vec_add(particles[k].acc, new_acc), dt * 0.5));
            new_pos = vec_add(particles[k].pos, vec_scale_mul(vec_add(particles[k].vel, new_vel), dt * 0.5));

            particles[k].acc = new_acc;
            particles[k].vel = new_vel;
            particles[k].pos = new_pos;
        }

    write_error = fprintf(file, "\n");
    if (write_error < 1) {
        printf("Write error encountered.\n");
        return -1;
    }
    // FIXME: can't use decimal time for simulation length
    fprintf(stdout, "\rCalculating: %.2f%%", ((float)(100 * time) / (t/dt)));
    fflush(stdout);
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

    float dt = atof(argv[1]);
    float t = atof(argv[2]);
    int num_part = atoi(argv[3]);

    Vector pos;
    Vector vel;
    Vector acc;
    double mass;
    double radius;

    FILE* cfile = fopen("config.txt", "r");
    if (cfile == NULL) {
        printf("File could not be opened for reading.");
        return 1;
    }

    Particle* arr = malloc(num_part * sizeof(Particle));

    int i = 0;
    while (fscanf(cfile, "%lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf, %lf ", &mass, &radius, &(pos.x), &(pos.y), &(pos.z), &(vel.x), &(vel.y), &(vel.z), &(acc.x), &(acc.y), &(acc.z)) == 11) {
        arr[i].mass = mass;
        arr[i].radius = radius;
        arr[i].pos = pos;
        arr[i].vel = vel;
        arr[i].acc = acc;
        i++;
    }

    calculate_forces("data.txt", arr, num_part, dt, t);

    free(arr);

    return 0;
}