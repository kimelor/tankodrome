'''
Created on Jun 13, 2013

@author: morhir
'''
import sys, pygame
from pygame.locals import *
import CONSTANTS

# - Game app constants
SCREEN_SIZE = 800, 600
SCREEN_FLAGS = 0
SCREEN_TITLE = 'Tankor 0.1 dev'
FPS = 60


class GameApp(object):
    """ Main game controller """
    def __init__(self, **kwargs):
        pygame.init()
        ## Screen init
        self._screen = pygame.display.set_mode(kwargs.get('screen_size',
                                                          SCREEN_SIZE),
                                               kwargs.get('screen_flags',
                                                          SCREEN_FLAGS))
        pygame.display.set_caption(kwargs.get('screen_title',
                                              SCREEN_TITLE))
        self._mouse = {'pos': (0, 0),
                       'pressed': (False, False, False)}
        ## game data here
        self._control = (kwargs.get('control',
                                    ScreenManager()))
        ## loop control
        self._clock = pygame.time.Clock()
        self._fps = FPS
        self._exit = False
        ## go
        self.run()

    @property
    def mouse(self):
        """ mouse, read only """
        return self._mouse

    def set_control(self, control):
        self._control = control

    def run(self):
        """ Run the Main Game loop """
        while not self._exit:
            self.manage_events()
            self.update_game()
            self.update_screen()
            self._clock.tick(self._fps)
            pygame.display.flip()
        self.quit()

    def manage_events(self):
        # solve events
        for event in pygame.event.get():
            if event.type == QUIT:
                self._exit = True
            elif event.type == MOUSEMOTION:
                self._control.mouse_motion_update(self._mouse['pos'])
                pass
            elif event.type == MOUSEBUTTONDOWN:
                pass
            elif event.type == MOUSEBUTTONUP:
                pass
            elif event.type == KEYDOWN:  # A key was pressed
                if event.key in (K_LEFT, K_RIGHT, K_UP, K_DOWN):
                    pass
                elif event.key == K_SPACE:
                    pass
                elif event.key == K_h:
                    pass    # Otras opciones a agregar, son, al abandonar el mouse
                elif event.key == K_ESCAPE:
                    self._exit = True
            elif event.type == VIDEORESIZE:
                print event
                pass
        # update input
        self._mouse['pos'] = pygame.mouse.get_pos()
        self._mouse['pressed'] = pygame.mouse.get_pressed()
        self._keyboard = None

    def update_game(self):
        self._control.update()

    def update_screen(self):
        self._screen.fill(CONSTANTS.BLACK)
        self._control.draw(self._screen)

    def quit(self):
        pygame.quit()


class ScreenManager(pygame.sprite.LayeredDirty):
    """ Controls, updates and draws all objects in a screen """
    def __init__(self, *args,**kwargs):
        pygame.sprite.LayeredDirty.__init__(self, args)
        ## Gui Control
        self.gui_manager = None
        ## Screen surface
        self._board = pygame.surface.Surface(kwargs.get('surfasce_size',
                                                        SCREEN_SIZE),
                                             kwargs.get('surface_flags',
                                                        0))
    def update(self, *args):
        for sprite in self.sprites():
            sprite.update(*args)

    def mouse_motion_update(self, mouse_pos):
        """ return a list of Panels under the mouse  """
        under_cursor = []
        for panel in self.sprites():
            if panel.rect.collidepoint(mouse_pos) or panel.active:
                panel.mouse_motion_update(mouse_pos)


class Panel(pygame.sprite.DirtySprite):
    """ Controls, updates and draws all objects in a screen """
    def __init__(self):
        """ Constructor """
        pygame.sprite.DirtySprite.__init__(self)
        self.name = 'Generic Panel'
        self.active = False

    def set_surface(self, (width, height), flags=0, color=None):
        print (width, height), flags, color
        self._width, self._height = width, height
        self.image = pygame.surface.Surface((width, height), flags)
        self.rect = self.image.get_rect()
        self.color = color
        self.default_color = color
        if color is not None:
            self.color = color
            self.default_color = color
            self.refresh()

    def refresh(self):
        self.image.fill(self.color)

    def on_click(self, mouse_pos):
        relative_pos = (mouse_pos[0] - self.rect.left,
                        mouse_pos[1] - self.rect.top)
        print "Panel {0} clicked on {1}".format(self.name,
                                                relative_pos)

    def mouse_motion_update(self, mouse_pos):
        # if was active, but mouse leave
        if self.active and not self.rect.collidepoint(mouse_pos):
            self.active = False
            self.color = self.default_color
            self.refresh()
            #self.dirty = 1
        # if was inactive, and now is active
        elif not self.active and self.rect.collidepoint(mouse_pos):
            self.active = True
            self.color = CONSTANTS.BLUE
            self.refresh()
            #self.dirty = 2
        # if was active and is active
        else:
            pass


    def mouse_off(self):
        self.color = self.default_color
        self.refresh()
        #print "Panel {0} off".format(self.name)


def main():
    """ Main Function """
    gadget = Panel()
    gadget.name = 'Boton'
    gadget.dirty = 2
    gadget.set_surface((100, 50), 0, CONSTANTS.RED)
    gadget.rect.topleft = 200,200

    gadget1 = Panel()
    gadget1.name = 'sidepanel'
    gadget1.dirty = 2
    gadget1.set_surface((100, 300), 0, CONSTANTS.GRAY)
    gadget1.rect.topleft = 0, 0

    start_screen = ScreenManager(gadget, gadget1)
    game = GameApp(screen_size=(800, 600),
                   screen_title='Tankodrome',
                   screen_flags=RESIZABLE,
                   control=start_screen)
    return bool(game)

if __name__ == '__main__':
    """ Execution """
    status = main()
    sys.exit(status)