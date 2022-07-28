from typing import Tuple, Type

import pygame

from client.state.gamestate import GameState


def __fade(out: bool, duration_frames: int, from_color: Tuple[int, int, int] = (0, 0, 0)):
    # alpha levels increase when fading out, decrease when fading in
    if out:
        # TODO: think of fade out implementation
        pass
        # def get_current_alpha(framectr, maxframes) -> float:
        #     return round(255 * (framectr / maxframes))
    else:

        def get_current_alpha(framectr, maxframes) -> float:
            return round(255 - 255 * (framectr / maxframes))

    def decorator(cls: Type[GameState]):
        class FadeInWrapper(cls):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)

                w, h = self.window.get_width(), self.window.get_height()
                self.__solid_surface = pygame.Surface((w, h))
                # this converts the surface format from RGB to RGBA
                self.__solid_surface.convert()
                self.__solid_surface.fill(from_color)

                self.__frame_ctr = 0

                self.__stop = False

            # Call superclass redraw function, then fill the screen with semitransparent surface.
            def redraw(self, *args, **kwargs):
                super().redraw(*args, **kwargs)

                if self.__stop:
                    return

                # fill amount ranges from 0-1
                alpha: float = get_current_alpha(self.__frame_ctr, duration_frames)
                # print(f"α: {alpha}")

                if alpha > 0:
                    self.__solid_surface.set_alpha(alpha)
                    self.window.blit(self.__solid_surface, (0, 0))

                    self.__frame_ctr += 1
                else:
                    # no reason for this function to exist / run after alpha reaches 0
                    self.__stop = True

        return FadeInWrapper

    return decorator


def fade_in(duration_frames: int, from_color: Tuple[int, int, int] = (0, 0, 0)):
    """Decorator to make screen fade into game state from a colored screen.

    Decorates any subclass of `GameState`.
    """
    return __fade(False, duration_frames, from_color)


# TODO
# def fade_out(duration_frames: int, from_color: Tuple[int, int, int] = (0, 0, 0)):
#     return __fade(True, duration_frames, from_color)
