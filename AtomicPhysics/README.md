Version History and all files for the atomic physics engine

--- v0.0.1 (05/16/24) ---
- Quick rough mockup
- Uses Python and pygame to simulate the physics of charged particles in free space
- Updates positions/velocities with Euler's method (to be improved later)
- Many errors in force calculation and position/velocity/acceleration updates

--- v0.0.2 (05/17/24) ---
- Collision functionality for particles (inconsistent)
- Corrected force application function

--- v0.0.3 (05/18/24) ---
- Updates positions/velocities with Verlet Integration
- Properties of atoms?
- Fixed collision functionality

--- v0.0.4 (05/23/24) ---
- Estimating Van der Waals forces/potentials of noble gases with Lennard Jones Potential
- Running into limitations with the real-time calculation of forces
- Script for pre-calculating positions of atoms to make simulation more accurate

--- v0.0.6 (9/13/24) ---
- Pre-calculate particle positions using C (faster than Python)
- Config file for better declaration of particles in pre-calculation and simulation
- First implementation of ionic bonding

--- v0.0.7 (in progress) ---
- Utilize Molecular Orbitals to improve electron repulsion
- Calculate covalent bond potentials using MO Theory
