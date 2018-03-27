#############################################################
# Segregation Model based on Thomas C. Schelling 1971       #
# Dynamic models of segregation                             #
# Code written by Morgen Burke in March, 2018               #
#############################################################

# Copyright (C) 2018  Morgen Burke

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# The imports
import numpy
import random
from sys import argv
# use of the -p tag requires matplotlib


def make_the_board(lenx, leny):
    # Create the Board, and a randomly distributed set of 0,1,2
    if (lenx * leny) % 3 != 0:
        print('\n Product of length and width is not divisible by 3\n')
        quit()
    ModelBoard = numpy.zeros((lenx, leny), dtype=numpy.int8)
    # print(ModelBoard)
    x_arr, y_arr = numpy.where(ModelBoard == 0)
    zip_arr = zip(x_arr, y_arr)
    numpy.random.shuffle(zip_arr)
    # print(zip_arr)
    count = 0
    for x, y in zip_arr:
        ModelBoard[x, y] = count
        if count == 2:
            count = 0
        else:
            count += 1
    del zip_arr
    zip_array = zip(x_arr, y_arr)
    return ModelBoard, zip_array


def getopts(argv):  # Look for agruments sent into the scrip
    opts = {}  # Empty dictionary to store key-value pairs.
    nextisi = False
    nextisslength = False
    nextisswidth = False
    for args in argv:  # While there are arguments left to parse...
        # print(args)
        if args == 'SegregationModel.py':
            print('\n')
        elif args == '-i':  # Found a "-name value" pair.
            nextisi = True
            opts[args] = 10
        elif nextisi is True:
            opts['-i'] = args  # Add key and value to the dictionary.
            nextisi = False
        elif args == '-s':  # Found a "-name value" pair.
            nextisslength = True
            opts['-sa'] = 10
            opts['-sb'] = 12
        elif nextisslength is True:
            opts['-sa'] = args  # Add key and value to the dictionary.
            nextisslength = False
            nextisswidth = True
        elif nextisswidth is True:
            opts['-sb'] = args  # Add key and value to the dictionary.
            nextisswidth = False
        elif args == '-h':
            opts[args] = 0
        elif args == '-p':
            opts[args] = 0
        argv = args[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


def get_list_of_neighbours(cx, cy):  # Get the coordinates of the neighboring cells
    neighborlist = list()
    x, y = cx-1, cy+1
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx, cy+1
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx+1, cy+1
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx+1, cy
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx+1, cy-1
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx, cy-1
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx-1, cy-1
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    x, y = cx-1, cy
    if lenx > x >= 0:
        if leny > y >= 0:
            neighborlist.append((x, y))
    return(neighborlist)


def get_the_unhappy_list(zip_arr):  # get coordinates for cells that do not hold a local majority
    UnhappyCellList = list()
    for ccx, ccy in zip_arr:
        NeighborList = get_list_of_neighbours(ccx, ccy)

        tokenvalue = ModelBoard[ccx, ccy]
        unlikecount = 0
        likecount = 1
        if tokenvalue > 0:
            for x, y in NeighborList:
                if ModelBoard[x, y] == tokenvalue:
                    likecount += 1
                elif ModelBoard[x, y] != tokenvalue:
                    if ModelBoard[x, y] > 0:
                        unlikecount += 1
            if likecount <= unlikecount:
                UnhappyCellList.append((ccx, ccy))
    return UnhappyCellList


def move_the_unhappy_cells(UnhappyCells):  # move the unhappy cells to a randomly open spot (open spots are a zero)
    for uhx, uhy in UnhappyCells:
        zerocount = 0
        unhappyneighbors = get_list_of_neighbours(uhx, uhy)
        for uhnx, uhny in unhappyneighbors:
            if ModelBoard[uhnx, uhny] == 0:
                zerocount += 1
        if zerocount == 1:
            # print("one move")
            for uhnx, uhny in unhappyneighbors:
                if ModelBoard[uhnx, uhny] == 0:
                    ModelBoard[uhnx, uhny] = ModelBoard[uhx, uhy]
                    ModelBoard[uhx, uhy] = 0
        elif zerocount > 1:
            # print("lots of moves")
            randnum = random.randint(0, zerocount)
            zeroplacecount = 0
            for uhnx, uhny in unhappyneighbors:
                if ModelBoard[uhnx, uhny] == 0:
                    if zeroplacecount == randnum:
                        ModelBoard[uhnx, uhny] = ModelBoard[uhx, uhy]
                        ModelBoard[uhx, uhy] = 0
                    else:
                        zeroplacecount += 1


def show_field(field1, field2):
    import matplotlib.pyplot as plt
    from matplotlib import colors
    cmap = colors.ListedColormap(['white', 'blue', 'red'])
    fig = plt.figure()
    ax = fig.add_subplot(2, 1, 1)
    ax.imshow(field1, cmap=cmap)
    ax.set_adjustable('box-forced')
    ax.autoscale(False)
    ax2 = fig.add_subplot(2, 1, 2)
    ax2.set_adjustable('box-forced')
    ax2.imshow(field2, cmap=cmap)
    ax2.autoscale(False)
    plt.show()


if __name__ == '__main__':  # Start the main body of the script
    print('\n #############################################################')
    print(' # Segregation Model based on Thomas C. Schelling 1971       #')
    print(' # Dynamic models of segregation                             #')
    print(' # Code written by Morgen Burke in March, 2018               #')
    print(' #############################################################')

    myargs = getopts(argv)  # Pull in the user arguments
    if '-h' in myargs:  # if help requested
        print("\n HELP:\n      Use -h tag to display this help prompt\n"
              "\n      Use -i tag to set number of iterations \n      "
              "Example argument: python SegregationModel.py -i 15 \n"
              "      This will run the model for 15 iterations before displaying the results\n"
              "\n      Use -s tag with two numbers to set the width/height of the array\n"
              "      Example argument: python SegregationModel.py -s 10 18 \n"
              "      This will run the model using an array size 18 wide by 10 high\n"
              "      The product of the two values must be divisible by three or it will result in error\n"
              "\n      Use -p tag to display a colored chart of the original and final model\n")
        quit()
    if '-i' in myargs:  # user set an iteration value
        NumberOfIterations = int(myargs['-i'])
    else:
        NumberOfIterations = int(10)
    if '-sa' in myargs:  # user set array size for vertical distance
        lenx = int(myargs['-sa'])
    else:
        lenx = 10
    if '-sb' in myargs:  # user set array size horizontal distance
        leny = int(myargs['-sb'])
    else:
        leny = 12
    if '-p' in myargs:  # user set array size horizontal distance
        showplot = True
    else:
        showplot = False

    # Make the array, and return a list of positions in the array
    ModelBoard, zip_array = make_the_board(lenx, leny)
    # Let the user know what the different numbers mean
    print(' Legend:')
    print(' A 0 is a blank/unoccupied space')
    print(' A 1 is a space occupied by the first cultural group')
    print(' A 2 is a space occupied by the second cultural group')
    print('\n Starting randomly distributed model\n')
    print(ModelBoard)
    OG_ModelBoard = numpy.array(ModelBoard)

    UnhappyCell_ListOfLength = list()  # list to hold the number of unhappy cells at each iteration
    while NumberOfIterations > 0:  # Loops for each iteration set by default to 10, or set by user argument
        TheUnhappyCells = get_the_unhappy_list(zip_array)
        UnhappyCell_ListOfLength.append(len(TheUnhappyCells))
        move_the_unhappy_cells(TheUnhappyCells)
        NumberOfIterations -= 1

    print('\n Number of unhappy cells for each iteration:')
    print(' '+str(UnhappyCell_ListOfLength))
    TheUnhappyCells = get_the_unhappy_list(zip_array)
    print('\n The final segregation model\n Unhappy cells remaining: '+str(len(TheUnhappyCells))
          +'\n Location starting at 0,0 (vertical,horizontal): '+str(TheUnhappyCells)+'\n')
    print(ModelBoard)
    print('\n')

    if showplot is True:
        show_field(OG_ModelBoard, ModelBoard)





