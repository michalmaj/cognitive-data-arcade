from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pygame

from cognitive_data_arcade.engine.chart import figure_to_surface
from cognitive_data_arcade.engine.colors import (
    BG as _BG,
)
from cognitive_data_arcade.engine.colors import (
    BLUE as _BLUE,
)
from cognitive_data_arcade.engine.colors import (
    DIM as _DIM,
)
from cognitive_data_arcade.engine.colors import (
    GREEN as _GREEN,
)
from cognitive_data_arcade.engine.colors import (
    ORANGE as _ORANGE,
)
from cognitive_data_arcade.engine.colors import (
    RED as _RED,
)
from cognitive_data_arcade.engine.colors import (
    WHITE as _WHITE,
)
from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.scene import Scene

_PANEL = (18, 18, 42)
_FIG_BG = "#0f0f23"
_AX_BG = "#1a1a3e"
_W, _H = 1024, 768


class PhaseSessionResultScene(Scene):
    def __init__(
        self,
        session_score: int,
        round_results: list[dict],
        pm=None,
        strings=None,
    ) -> None:
        self._session_score = session_score
        self._round_results = round_results
        self._pm = pm
        self._strings = strings
        self._done = False
        self._next: Scene | None = None
        self._chart_surf = self._render_chart()

    def _render_chart(self) -> pygame.Surface:
        labels = [f"R{r['round_idx'] + 1}" for r in self._round_results]
        player_accs = [r["player_acc"] * 100 for r in self._round_results]
        knn_accs = [r["clf_accs"].get("knn", 0) * 100 for r in self._round_results]
        mean_knn = sum(knn_accs) / len(knn_accs) if knn_accs else 0

        fig, ax = plt.subplots(figsize=(7, 2.5), dpi=96, facecolor=_FIG_BG)
        ax.set_facecolor(_AX_BG)
        ax.bar(labels, player_accs, color="#f39c12", width=0.5, label="Ty")
        ax.axhline(mean_knn, color="#9b59b6", linestyle="--", linewidth=1, label="KNN (avg)")
        ax.set_ylim(0, 105)
        ax.set_ylabel("Dokładność (%)", color="#787890", fontsize=8)
        ax.tick_params(colors="#787890", labelsize=8)
        ax.legend(fontsize=7, facecolor=_FIG_BG, labelcolor="white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#2a2a50")
        return figure_to_surface(fig, (672, 240))

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if not self._done:
                self._next = self._build_next_scene()
            self._done = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            btn = pygame.Rect(_W // 2 - 130, _H - 62, 260, 44)
            if btn.collidepoint(event.pos):
                from cognitive_data_arcade.games.classifier_battle.phase_intro import (
                    PhaseIntroScene,
                )

                self._next = PhaseIntroScene()
                self._done = True

    def _build_next_scene(self) -> "Scene":
        from cognitive_data_arcade.engine.badges import BadgeEngine, SessionResult
        from cognitive_data_arcade.ui.session_summary import SessionSummaryScene

        total = len(self._round_results)
        correct = sum(1 for r in self._round_results if r.get("player_acc", 0) >= 0.5)
        ap = min(100, self._session_score // 10)
        session = SessionResult(
            task_name="classifier_battle",
            participant_id=self._pm.load().device_uuid,
            session_id="classifier_battle_session",
            total_trials=total,
            correct_trials=min(total, correct),
            avg_reaction_time_ms=0.0,
            min_reaction_time_ms=0.0,
            max_reaction_time_ms=0.0,
            arcade_points_earned=ap,
            science_points_earned=0,
        )
        profile_before = self._pm.load()
        badge_engine = BadgeEngine()
        new_badge_ids = badge_engine.evaluate(session, profile_before)
        self._pm.add_ap(ap)
        for bid in new_badge_ids:
            self._pm.award_badge(bid)
        profile_after = self._pm.load()
        return SessionSummaryScene(
            session=session,
            new_badge_ids=new_badge_ids,
            profile_before=profile_before,
            profile_after=profile_after,
            strings=self._strings,
            profile_manager=self._pm,
        )

    def update(self, dt_ms: float = 0.0) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(_BG)
        pygame.draw.rect(surface, _PANEL, (0, 0, _W, 56))
        title = get_font(22).render("Wyniki sesji — Classifier Battle", True, _WHITE)
        surface.blit(title, (_W // 2 - title.get_width() // 2, 14))

        # Score
        score_col = (
            _GREEN
            if self._session_score >= 400
            else (_ORANGE if self._session_score >= 200 else _RED)
        )
        score_surf = get_font(36).render(str(self._session_score), True, score_col)
        surface.blit(score_surf, (_W // 2 - score_surf.get_width() // 2, 68))
        pts = get_font(14).render("punktów", True, _DIM)
        surface.blit(pts, (_W // 2 - pts.get_width() // 2, 112))

        # Chart
        if self._chart_surf:
            surface.blit(self._chart_surf, (_W // 2 - 336, 136))

        # Table
        y = 390
        header_font = get_font(13)
        hdr = header_font.render(
            "  Runda   Scenariusz              Twój wynik   Najlepszy alg.   Różnica",
            True,
            _DIM,
        )
        surface.blit(hdr, (40, y))
        y += 20

        row_font = get_font(13)
        for r in self._round_results:
            best_name = max(r["clf_accs"], key=r["clf_accs"].get)
            best_acc = r["clf_accs"][best_name]
            diff = r["player_acc"] - best_acc
            diff_str = f"{diff:+.0%}"
            diff_col = _GREEN if diff >= 0 else _RED
            row = row_font.render(
                f"    {r['round_idx'] + 1}       {r['scenario_name']:<20}   {r['player_acc']:.0%}            {best_name} {best_acc:.0%}",
                True,
                _WHITE,
            )
            surface.blit(row, (40, y))
            diff_surf = row_font.render(diff_str, True, diff_col)
            surface.blit(diff_surf, (940, y))
            y += 20

        # Replay button
        btn = pygame.Rect(_W // 2 - 130, _H - 62, 260, 44)
        pygame.draw.rect(surface, _PANEL, btn, border_radius=6)
        pygame.draw.rect(surface, _BLUE, btn, 2, border_radius=6)
        lbl = get_font(18).render("Zagraj ponownie", True, _BLUE)
        surface.blit(lbl, (btn.centerx - lbl.get_width() // 2, btn.centery - lbl.get_height() // 2))

    def is_done(self) -> bool:
        return self._done

    def next_scene(self) -> Scene | None:
        return self._next
