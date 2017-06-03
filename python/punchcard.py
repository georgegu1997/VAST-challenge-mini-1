#!/usr/bin/env python
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import numpy as np

# Discussion http://stackoverflow.com/questions/14849815/matplotlib-how-to-remove-the-vertical-space-when-displaying-circles-on-a-grid
def draw_punchcard(infos,
                ax1=range(7),
                ax2=range(24),
                ax1_ticks=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                ax2_ticks=range(24),
                ax1_label='Day',
                ax2_label='Hour'):
    """Construct a punchcard.
    Quick'n dirty way.
    Parameters
    ==========
    - infos: Dictionary of quantities to display.
            They are indexed by key of type (val1,val2) with
            val1 included in ax1 and val2 included in ax2.
    - ax1: list
            Possible values for first axe (if different than days)
    - ax2: list
            Possible values for second axe (if different than hours)
    - ax1_ticks: list
            Value to display in ticks of first axe (if different than days)
    - ax2_ticks: list
            Value to display in ticks of second axe (if different than days)
    - ax1_label: String
            Value to give to first axis (if different than day)
    - ax2_label: String
            Value to give to second axis (if different than day)
    """

    # build the array which contains the values
    data = np.zeros((len(ax1),len(ax2)))
    for key in infos:
        data[key[0],key[1]] = infos[key]
    data_ax1 = np.sum(data, axis=1)
    data_ax2 = np.sum(data, axis=0)
    data_ax1.shape=(-1,1)
    data_ax2.shape=(1,-1)
    data = data/float(np.max(data))
    data_ax1 = data_ax1/float(np.max(data_ax1))
    data_ax2 = data_ax2/float(np.max(data_ax2))

    # shape ratio
    r = float(data.shape[1])/data.shape[0]
    # Draw the punchcard (create one circle per element)
    # Ugly normalisation allows to obtain perfect circles instead of ovals....
    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            circle = plt.Circle((x/float(data.shape[1])*data.shape[0],y/r),
                                data[y][x]/float(data.shape[1])*data.shape[0]/2,
                                color='gray')
            plt.gca().add_artist(circle)

    plt.ylim(0-0.5,  data.shape[0]-0.5)
    plt.xlim(0-0.5, data.shape[0])
    plt.yticks(np.arange(0,len(ax1)/r-.1,1/r), ax1_ticks)
    plt.xticks(np.linspace(0,len(ax1), len(ax2))+0.5/float(data.shape[1]), ax2_ticks)
    plt.xlabel(ax1_label)
    plt.ylabel(ax2_label)
    plt.gca().invert_yaxis()

    # make sure the axes are equal, and resize the canvas to fit the plot
    plt.axis('equal')
    plt.axis([0, 7.02, 7/r, -.5])
    scale = 0.5
    plt.gcf().set_size_inches(data.shape[1]*scale,data.shape[0]*scale, forward=True)



if __name__ == '__main__':
    infos = {(6, 9): 12196, (0, 20): 22490, (1, 17): 59636, (0, 7): 14915, (2, 22): 7193, (1, 6): 11694, (0, 10): 85793, (3, 7): 17507, (2, 5): 4078, (1, 11): 83424, (5, 8): 33625, (4, 0): 1915, (6, 7): 10528, (5, 5): 3525, (4, 19): 33253, (6, 10): 12186, (5, 18): 20856, (0, 17): 61370, (0, 4): 551, (1, 1): 389, (4, 10): 94684, (3, 2): 286, (2, 6): 11845, (5, 11): 46822, (4, 5): 5215, (3, 23): 1841, (6, 0): 3441, (4, 16): 94545, (6, 23): 1285, (5, 21): 11096, (2, 17): 59928, (0, 1): 279, (3, 12): 56193, (1, 12): 59846, (4, 15): 102986, (3, 1): 371, (2, 11): 78007, (5, 14): 27711, (3, 18): 41365, (6, 13): 11994, (4, 21): 14477, (6, 16): 11669, (1, 21): 13629, (2, 18): 42399, (0, 14): 66284, (3, 11): 76402, (2, 1): 358, (1, 15): 93381, (4, 12): 67279, (2, 12): 57427, (5, 1): 509, (3, 17): 58974, (6, 14): 11383, (0, 21): 12604, (1, 16): 86199, (2, 23): 1914, (1, 5): 4002, (0, 11): 79164, (3, 6): 11434, (2, 2): 304, (1, 10): 88874, (4, 1): 420, (6, 4): 750, (5, 4): 783, (6, 11): 12886, (5, 17): 21573, (0, 18): 41842, (1, 19): 33073, (0, 5): 2777, (1, 0): 1189, (0, 8): 46486, (4, 11): 89246, (3, 5): 4105, (2, 7): 18534, (5, 10): 54826, (4, 6): 14638, (3, 22): 5043, (6, 1): 894, (5, 7): 16052, (4, 17): 66899, (6, 20): 16085, (5, 20): 18041, (0, 2): 219, (3, 15): 81526, (1, 3): 251, (4, 8): 58008, (3, 0): 1581, (2, 8): 47233, (5, 13): 23896, (3, 21): 13998, (6, 2): 540, (4, 22): 5920, (6, 17): 13856, (5, 23): 2155, (1, 20): 24386, (2, 19): 33216, (0, 15): 86664, (3, 10): 81444, (1, 14): 74440, (4, 13): 62307, (2, 13): 51784, (5, 0): 1959, (3, 16): 76742, (6, 15): 11438, (0, 22): 4055, (6, 18): 17554, (1, 23): 1681, (2, 20): 26427, (1, 4): 710, (0, 12): 59008, (3, 9): 72555, (2, 3): 372, (1, 9): 79140, (4, 2): 322, (2, 14): 68869, (6, 5): 3091, (5, 3): 392, (6, 8): 11720, (5, 16): 28663, (0, 19): 30223, (1, 18): 41624, (0, 6): 8791, (1, 7): 18280, (0, 9): 75860, (3, 4): 765, (2, 4): 834, (5, 9): 52874, (4, 7): 21830, (6, 6): 7618, (5, 6): 9935, (4, 18): 43274, (6, 21): 9836, (5, 19): 20758, (0, 16): 81458, (0, 3): 245, (3, 14): 66845, (1, 2): 291, (4, 9): 86355, (3, 3): 346, (2, 9): 71401, (5, 12): 27939, (4, 4): 987, (3, 20): 24478, (6, 3): 450, (4, 23): 2236, (6, 22): 3779, (5, 22): 4950, (2, 16): 79009, (0, 0): 1655, (3, 13): 53589, (1, 13): 55308, (4, 14): 81394, (2, 10): 80932, (5, 15): 32751, (3, 19): 32193, (6, 12): 12770, (4, 20): 24379, (0, 23): 1240, (6, 19): 18908, (1, 22): 4887, (2, 21): 16508, (0, 13): 54858, (3, 8): 47367, (2, 0): 1778, (1, 8): 50393, (4, 3): 387, (2, 15): 86256, (5, 2): 385}
    draw_punchcard(infos)
    plt.show()
