import pygame

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.ui.analysis_scene import AnalysisScene

_STATS = {
    "avg_rt": 250.0,
    "median_rt": 240.0,
    "min_rt": 180.0,
    "max_rt": 340.0,
    "accuracy": 0.92,
    "n_trials": 24,
    "n_correct": 22,
}


class _BackScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def is_done(self) -> bool:
        return False


def _make_scene() -> AnalysisScene:
    pygame.init()
    chart = pygame.Surface((680, 550))
    chart.fill((10, 10, 20))
    return AnalysisScene(
        chart_surface=chart,
        stats=_STATS,
        strings=EN,
        back_scene=_BackScene(),
    )


def test_analysis_scene_draws_without_crash() -> None:
    scene = _make_scene()
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_esc_sets_done() -> None:
    scene = _make_scene()
    assert not scene.is_done()
    esc = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    scene.handle_event(esc)
    assert scene.is_done()
    assert isinstance(scene.next_scene(), _BackScene)


def test_mouse_click_sets_done() -> None:
    scene = _make_scene()
    click = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 300))
    scene.handle_event(click)
    assert scene.is_done()
    assert isinstance(scene.next_scene(), _BackScene)
