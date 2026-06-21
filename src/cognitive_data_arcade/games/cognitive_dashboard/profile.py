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
    lines: list[str] = []

    rt_avg = _rt_baseline(session)
    if rt_avg is not None:
        if rt_avg < 220:
            lines.append(f"Czas reakcji bazowy: bardzo szybki ({rt_avg:.0f} ms).")
        elif rt_avg <= 320:
            lines.append(f"Czas reakcji bazowy: przeciętny ({rt_avg:.0f} ms).")
        else:
            lines.append(f"Czas reakcji bazowy: wolniejszy niż norma ({rt_avg:.0f} ms).")

    stroop_eff = _stroop_effect(session)
    if stroop_eff < 40:
        lines.append("Odporność na interferencję: silna (efekt Stroopa poniżej 40 ms).")
    elif stroop_eff <= 80:
        lines.append(f"Odporność na interferencję: przeciętna (efekt Stroopa {stroop_eff:.0f} ms).")
    else:
        lines.append(f"Efekt Stroopa wyraźnie widoczny - duża interferencja ({stroop_eff:.0f} ms).")

    flanker_eff = _flanker_effect(session)
    if flanker_eff < 25:
        lines.append("Selektywna uwaga: bardzo dobra (efekt Flankera poniżej 25 ms).")
    elif flanker_eff <= 60:
        lines.append(f"Selektywna uwaga: przeciętna (efekt Flankera {flanker_eff:.0f} ms).")
    else:
        lines.append(
            f"Dystraktorzy wyraźnie spowalniają reakcję (efekt Flankera {flanker_eff:.0f} ms)."
        )

    fa = _gonogo_fa_count(session)
    if fa == 0:
        lines.append("Hamowanie impulsów: bezbłędne (zero fałszywych alarmów).")
    elif fa == 1:
        lines.append("Hamowanie impulsów: dobre (drobne błędy na próbach no-go).")
    else:
        lines.append(f"Tendencja do impulsywności - trudność z hamowaniem ({fa} fałszywe alarmy).")

    lines.append("Pamiętaj - to tylko 8 prób. Więcej danych = pewniejszy wynik.")
    return lines
