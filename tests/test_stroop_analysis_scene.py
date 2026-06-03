import pygame

from cognitive_data_arcade.engine.i18n import EN
from cognitive_data_arcade.engine.scene import Scene
from cognitive_data_arcade.ui.stroop_analysis_scene import StroopAnalysisScene

_STATS = {
    "avg_rt_congruent": 265.0,
    "avg_rt_neutral": 315.0,
    "avg_rt_incongruent": 415.0,
    "facilitation_ms": 50.0,
    "interference_ms": 100.0,
    "stroop_effect_ms": 150.0,
    "accuracy": 1.0,
    "n_trials": 12,
    "n_correct": 12,
}


class _DummyScene(Scene):
    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt_ms: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass

    def is_done(self) -> bool:
        return False

    def next_scene(self) -> Scene | None:
        return None


def _make_scene() -> StroopAnalysisScene:
    pygame.init()
    chart = pygame.Surface((680, 520))
    return StroopAnalysisScene(chart, _STATS, EN, _DummyScene())


_NAN_STATS = {
    "avg_rt_congruent": float("nan"),
    "avg_rt_neutral": float("nan"),
    "avg_rt_incongruent": float("nan"),
    "facilitation_ms": float("nan"),
    "interference_ms": float("nan"),
    "stroop_effect_ms": float("nan"),
    "accuracy": 0.0,
    "n_trials": 12,
    "n_correct": 0,
}


def test_draws_without_crash() -> None:
    scene = _make_scene()
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_esc_sets_done() -> None:
    scene = _make_scene()
    assert not scene.is_done()
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.is_done()


def test_draws_without_crash_all_timeouts() -> None:
    pygame.init()
    chart = pygame.Surface((680, 520))
    scene = StroopAnalysisScene(chart, _NAN_STATS, EN, _DummyScene())
    surface = pygame.Surface((1024, 768))
    scene.draw(surface)


def test_next_scene_is_none_before_esc() -> None:
    scene = _make_scene()
    assert scene.next_scene() is None


def test_next_scene_returns_back() -> None:
    back = _DummyScene()
    pygame.init()
    chart = pygame.Surface((680, 520))
    scene = StroopAnalysisScene(chart, _STATS, EN, back)
    scene.handle_event(
        pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")
    )
    assert scene.next_scene() is back


def test_mouse_click_sets_done() -> None:
    scene = _make_scene()
    scene.handle_event(pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(400, 300)))
    assert scene.is_done()
