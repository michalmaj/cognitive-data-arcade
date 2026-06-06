# src/cognitive_data_arcade/games/data_cleaning/ui_report.py
from __future__ import annotations

import pygame

from cognitive_data_arcade.engine.fonts import get_font
from cognitive_data_arcade.engine.i18n import Strings
from cognitive_data_arcade.games.data_cleaning.generator import (
    CleaningSession,
    apply_fixes,
    compute_score,
    compute_stats,
)

_WHITE = (240, 240, 240)
_DIM = (120, 120, 160)
_ORANGE = (243, 156, 18)


def draw_report(
    surface: pygame.Surface,
    session: CleaningSession,
    flagged: set[int],
    fixes: dict[int, str],
    strings: Strings,
    font_title: pygame.font.Font,
    font_body: pygame.font.Font,
    font_hint: pygame.font.Font,
) -> None:
    w, h = surface.get_size()
    lang = strings.language

    # Title
    title_surf = font_title.render(strings.data_cleaning_report_title, True, _ORANGE)
    surface.blit(title_surf, (w // 2 - title_surf.get_width() // 2, 20))

    # Score
    d, f, total = compute_score(session, flagged, fixes)
    score_text = f"Score: {total}/100   (Detection: {d}/60   Fix quality: {f}/40)"
    score_surf = font_body.render(score_text, True, _WHITE)
    surface.blit(score_surf, (w // 2 - score_surf.get_width() // 2, 80))

    # Stats before / after
    stats_before = compute_stats(session.rows)
    cleaned = apply_fixes(session, flagged, fixes)
    stats_after = compute_stats(cleaned)

    pygame.draw.line(surface, _DIM, (40, 120), (w - 40, 120), 1)

    col_x = [40, w // 2 + 20]
    col_labels = ["Before cleaning", "After cleaning"]
    if lang == "pl":
        col_labels = ["Przed czyszczeniem", "Po czyszczeniu"]

    for ci, (cx, label) in enumerate(zip(col_x, col_labels)):
        stats = stats_before if ci == 0 else stats_after
        lbl_surf = font_body.render(label, True, _ORANGE)
        surface.blit(lbl_surf, (cx, 132))
        lines = [
            f"Rows:          {int(stats['n_rows'])}",
            f"Mean RT:       {stats['mean_rt']:.1f} ms",
            f"Std RT:        {stats['std_rt']:.1f} ms",
            f"Mean accuracy: {stats['mean_accuracy']:.3f}",
        ]
        y = 170
        for line in lines:
            s = font_hint.render(line, True, _WHITE)
            surface.blit(s, (cx, y))
            y += 26

    # Detection summary
    pygame.draw.line(surface, _DIM, (40, 310), (w - 40, 310), 1)
    total_errors = len(session.ground_truth)
    found = len(flagged & set(session.ground_truth.keys()))
    missed = total_errors - found
    false_pos = len(flagged - set(session.ground_truth.keys()))

    summary_lines = [
        f"Errors in dataset: {total_errors}",
        f"Errors found:      {found}   Missed: {missed}   False flags: {false_pos}",
    ]
    y = 322
    for line in summary_lines:
        s = font_hint.render(line, True, _DIM)
        surface.blit(s, (40, y))
        y += 24

    # Bottom hint: player uses ESC to open pause menu and Restart from there
    esc_hint = "Press ESC for menu" if strings.language != "pl" else "Nacisnij ESC, aby otworzyc menu"
    esc_surf = font_hint.render(esc_hint, True, _DIM)
    surface.blit(esc_surf, (w // 2 - esc_surf.get_width() // 2, h - 36))
