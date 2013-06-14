""" TANKODROME

Created on Jun 13, 2013
@author: Luis Navarro Verduzco

"""
### -- Import modules -- ###
import sys, pygame
from pygame.locals import *
import objects, resources


def main():
    """ Main Function """
    game = resources.GameApp(screen_size=(300, 200),
                             screen_title='Tankodrome')


if __name__ == '__main__':
    """ Execution """
    status = main()
    sys.exit(status)