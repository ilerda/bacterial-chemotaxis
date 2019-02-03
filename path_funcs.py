'''Functions to set up the energy field and bacterial trajectory are provided here'''

from __future__ import division
import numpy
import random

N_bacteria = 60
t_total = 300 # sec
t_step = 0.1 # sec
speed = 1 # microns/sec
k = 1 # sensitivity

R0 = numpy.array([30,30]) # microns
N_steps = int(t_total / t_step)

def f(R):
    '''
    Describes the energy density in the field around the origin
    '''
    return 200 - numpy.sqrt(R[0]**2 + R[1]**2)


def bacterium_trajectory(r0,theta0):
    '''
    Inputs:
    r0 - starting coordinates of the bacteria.
    theta0 - initial angular directions.

    Output: Final bacterial trajectories.

    K determines how sensitively the bacterium reacts to the energy field which surrounds it.\
    If k is large the bacterium will not tumble as much while moving towards high energy and will also\
    tumble more often while moving away from an energy source. Bacteria with a higher value of k will reach\
    an energy source more quickly.
    '''
    r = r0
    r_history = numpy.zeros([N_steps,2])
    initial_energy = f(r0)
    i_e = initial_energy
    energy_list = [i_e,i_e,i_e,i_e,i_e,i_e,i_e,i_e,i_e,i_e]
    theta = theta0
    P_tumble = 0 # For the first step, none of them tumble.
    for i in range(N_steps):
        r_history[i,:] = r
        if random.random() > P_tumble:
            r = r + numpy.array([numpy.cos(theta), numpy.sin(theta)]) * speed * t_step
            energy_list.append(f(r))
            energy_grad = energy_list[-1] - energy_list.pop(0)
            t_half = 1 + k * energy_grad
            if t_half >= 0.2:
                P_tumble = 1 - numpy.exp(-numpy.log(2)*t_step/t_half)
            else:
                P_tumble = 1 - numpy.exp(-numpy.log(2)*t_step/0.2)
        else:
            theta = random.random() * 2 * numpy.pi

    return r_history
