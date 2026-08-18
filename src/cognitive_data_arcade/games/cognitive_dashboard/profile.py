from __future__ import annotations

from cognitive_data_arcade.games.cognitive_dashboard.session import DashboardSession


def _stroop_effect(session: DashboardSession) -> float:
    s = session.stroop
    cong = [rt for rt, c in zip(s.rt_ms, s.condition) if c == "congruent" and rt > 0]
    incong = [rt for rt, c in zip(s.rt_ms, s.condition) if c == "incongruent" and rt > 0]
    if not cong or not incong:
        return 0.0
    return sum(incong) / len(incong) - sum(cong) / len(cong)


def _flanker_effect(session: DashboardSession) -> float:
    f = session.flanker
    cong = [rt for rt, c in zip(f.rt_ms, f.condition) if c == "congruent" and rt > 0]
    incong = [rt for rt, c in zip(f.rt_ms, f.condition) if c == "incongruent" and rt > 0]
    if not cong or not incong:
        return 0.0
    return sum(incong) / len(incong) - sum(cong) / len(cong)


def _gonogo_fa_count(session: DashboardSession) -> int:
    g = session.gonogo
    return sum(1 for cond, ok in zip(g.condition, g.correct) if cond == "nogo" and not ok)


def _rt_baseline(session: DashboardSession) -> float | None:
    rt = session.rt
    if rt is None:
        return None
    valid = [r for r in rt.rt_ms if r > 0]
    return sum(valid) / len(valid) if valid else None


def cognitive_profile(session: DashboardSession) -> list[str]:
    """Return session-scoped observations — no trait labels, no normative comparisons."""
    lines: list[str] = []

    rt_avg = _rt_baseline(session)
    if rt_avg is not None:
        n = sum(1 for r in session.rt.rt_ms if r > 0)
        lines.append(f"Czas reakcji: {rt_avg:.0f} ms (średnia z {n} prób).")

    if session.stroop is not None:
        stroop_eff = _stroop_effect(session)
        n_stroop = len(session.stroop.rt_ms)
        lines.append(f"Efekt Stroopa: {stroop_eff:+.0f} ms (niekongr. − kongr., n={n_stroop}).")

    if session.flanker is not None:
        flanker_eff = _flanker_effect(session)
        n_flanker = len(session.flanker.rt_ms)
        lines.append(f"Efekt Flankera: {flanker_eff:+.0f} ms (niekongr. − kongr., n={n_flanker}).")

    if session.gonogo is not None:
        fa = _gonogo_fa_count(session)
        n_nogo = sum(1 for c in session.gonogo.condition if c == "nogo")
        lines.append(f"Fałszywe alarmy: {fa} z {n_nogo} prób no-go.")

    results = [session.rt, session.stroop, session.flanker, session.gonogo]
    total = sum(len(x.rt_ms) for x in results if x is not None)
    lines.append(f"Łącznie {total} prób w tej sesji. To tylko jeden pomiar.")
    return lines
