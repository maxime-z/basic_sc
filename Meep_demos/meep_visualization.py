"""Module to visualize meep problem configuration and results"""

import matplotlib.pyplot as plt


def visualize(field):
    fig, ax = plt.subplots()

    ax.imshow(field, cmap='RdBu')
    plt.show()