import argparse
import iris
iris.FUTURE.netcdf_promote = True
import matplotlib.pyplot as plt
import iris.plot as iplt
import iris.coord_categorisation
import cmocean
import numpy
import pdb


def read_data(fname, month):
    """Read an input data file"""
    
    cube = iris.load_cube(fname, 'precipitation_flux')
    
    iris.coord_categorisation.add_month(cube, 'time')
    cube = cube.extract(iris.Constraint(month=month))
    
    return cube


def convert_pr_units(cube):
    """Convert kg m-2 s-1 to mm day-1"""
    
    cube.data = cube.data * 86400
    cube.units = 'mm/day'
    
    return cube


def plot_data(cube, month, tick_levels, gridlines=False):
    """Plot the data."""
        
    fig = plt.figure(figsize=[12,5])    
    iplt.contourf(cube, cmap=cmocean.cm.haline_r, 
                  levels=numpy.arange(0, 10),
                  extend='max')

    plt.gca().coastlines()
    if gridlines:
        plt.gca().gridlines()
    cbar = plt.colorbar()
    cbar.set_label(str(cube.units))
    
    title = '%s precipitation climatology (%s)' %(cube.attributes['model_id'], month)
    plt.title(title)


def main(inargs):
    """Run the program."""

    cube = read_data(inargs.infile, inargs.month)   
    #pdb.set_trace()
    cube = convert_pr_units(cube)
    clim = cube.collapsed('time', iris.analysis.MEAN)
    plot_data(clim, inargs.month,inargs.tick_levels,inargs.gridlines)
    plt.savefig(inargs.outfile)


if __name__ == '__main__':
    description='Plot the precipitation climatology.'
    parser = argparse.ArgumentParser(description=description)
    
    parser.add_argument("infile", type=str, help="Input file name")
    parser.add_argument("month",type=str, choices=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],  help="Month to plot")
    parser.add_argument("outfile", type=str, help="Output file name")
    parser.add_argument("gridlines", default=False , help="If we want gridlines")
    parser.add_argument("tick_levels", type=float, help="If we want to change the ticks")

    args = parser.parse_args()
    
    main(args)
