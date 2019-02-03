'''Functions to plot bacterium paths are provided and implemented.'''

import matplotlib.pyplot as pyplot
import matplotlib.cm
from path_funcs import *


def make_plot():
    pyplot.plot(trajectory[:,0], trajectory[:,1])

def make_simplified_plot():
    x_points = numpy.array([trajectory[0,0],trajectory[-1,0]])
    y_points = numpy.array([trajectory[0,1],trajectory[-1,1]])
    pyplot.plot(x_points, y_points,marker='o')


if __name__ == '__main__':
    # bounds
    x0 = -10
    x1 = 40
    y0 = -10
    y1 = 40
    N_POINTS = 100
    dx = (x1 - x0) / N_POINTS
    dy = (y1 - y0) / N_POINTS

    y_axis = numpy.arange(y0, y1, dy)
    x_axis = numpy.arange(x0, x1, dx)

    dat = numpy.zeros((len(y_axis), len(x_axis)))

    for iy, y in enumerate(y_axis):
        for ix, x in enumerate(x_axis):
            dat[iy, ix] = f(numpy.array([x,y]))

    msds_start = []
    msds_origin = []
    pyplot.figure()
    pyplot.subplot(2,2,1)
    pyplot.title('bacteria paths')
    pyplot.xlabel('x-position / microns')
    pyplot.ylabel('y-position / microns')
    pyplot.xlim(x0, x1)
    pyplot.ylim(y0, y1)

    im = pyplot.imshow(dat,extent=(x0,x1,y0,y1),origin = 'lower',cmap=matplotlib.cm.gray)
    pyplot.colorbar(im, orientation = 'vertical')

    for i in range(N_bacteria):
        Theta0 = i * (2 * numpy.pi) / N_bacteria
        trajectory = bacterium_trajectory(R0,Theta0)
        MSD_s = numpy.sum((trajectory-30)**2,axis=1)
        msds_start.append(MSD_s)
        MSD_o = numpy.sum(trajectory**2,axis = 1)
        msds_origin.append(MSD_o)
        pyplot.subplot(2,2,1)
        make_plot()
        pyplot.subplot(2,2,2)
        make_simplified_plot()
    pyplot.title('start and end points')
    pyplot.xlabel('x-position / microns')
    pyplot.ylabel('y-position / microns')
    MSD_from_start = numpy.average(msds_start,axis=0)
    MSD_from_origin = numpy.average(msds_origin,axis=0)
    pyplot.subplot(2,1,2)
    pyplot.xlabel('time / s')
    pyplot.ylabel('average mean square displacements / microns squared')
    pyplot.plot(numpy.linspace(0,t_total,N_steps),MSD_from_origin,label='from origin')
    pyplot.plot(numpy.linspace(0,t_total,N_steps),MSD_from_start,label='from starting point')
    pyplot.legend(loc=7)
    pyplot.show()
