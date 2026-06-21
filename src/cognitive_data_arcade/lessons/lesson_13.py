# src/cognitive_data_arcade/lessons/lesson_13.py
"""Lesson 13 - Distributions and Variability."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Rozkład statystyczny opisuje, jak często występują różne wartości w zbiorze danych. W badaniach RT najczęściej spotykamy rozkłady zbliżone do normalnego, ale z charakterystycznym prawym ogonem - bo bardzo wolne reakcje są możliwe, a bardzo szybkie (poniżej 150 ms) nie.",
            "Rozkład normalny (Gaussa) jest symetryczny: tyle samo obserwacji po lewej co po prawej stronie średniej. Opisuje go średnia (mu, centrum) i odchylenie standardowe (sigma, szerokość). Większość RT-ów z prostego zadania mieści się w przedziale mu +/- 2*sigma.",
            "Rozkład jednostajny oznacza równe prawdopodobieństwo dla każdej wartości w przedziale [min, max]. W RT nie występuje naturalnie, ale używamy go jako model bazowy do porównania z rozkładami skośnymi.",
            "Rozkład Ex-Gaussian (normalny + wykładniczy) jest ulubieńcem psychologów poznawczych. Parametr tau opisuje długość prawego ogona - czas potrzebny na dodatkowe procesy (np. przeszukiwanie pamięci, hamowanie odpowiedzi). Większa tau = dłuższy ogon = więcej wolnych prób.",
            "Rozkład opisują: średnia (czuła na wartości odstające), mediana (odporna), odchylenie std (rozrzut), IQR (odporny rozrzut) i skośność (asymetria). Dla danych RT skośność jest zwykle dodatnia - mamy ogon w prawo.",
        ],
        "notes": [
            "Skośność RT-ów jest cechą, nie błędem. Prawdziwe dane z eksperymentów RT zawsze mają prawy ogon - to efekt biologiczny. Używanie średniej bez sprawdzenia skośności może dać mylący obraz.",
            "Wielkość próbki (N) wpływa na stabilność histogramu. Przy N=20 histogram jest hałaśliwy; przy N=200 wygląda gładziej. Większe N nie zmienia kształtu rozkładu - tylko nasz szacunek staje się dokładniejszy.",
            "Cohen's d i p-value mierzą różne rzeczy. p-value zależy od N: duża próba da p<0.05 nawet dla trywialnej różnicy. Cohen's d pokazuje wielkość efektu niezależnie od N. Zawsze raportuj oba.",
        ],
        "tasks": [
            "W Fazie A: porównaj histogramy normalnego i Ex-Gaussian z tymi samymi mu i sigma. Jak zmienia się kształt gdy zwiększasz tau? W jakim zakresie tau skośność staje się wyraźnie widoczna?",
            "W Fazie B: zgadnij rozkład bez wskazówek. Ile prób potrzebujesz? Które parametry są najtrudniejsze do odgadnięcia - mu, sigma czy tau? Dlaczego?",
            "W Fazie C: ustaw rozkład A jako normalny (mu=400, sigma=60, N=50) i rozkład B jako Ex-Gaussian (mu=400, sigma=60, tau=100, N=50). Obserwuj Cohen's d i p-value. Teraz zwiększaj N w obu do 200. Jak zmienia się p-value? Jak zmienia się Cohen's d?",
        ],
    },
    "en": {
        "theory": [
            "A statistical distribution describes how often different values appear in a dataset. RT data most often follows a distribution close to normal but with a characteristic right tail - very slow reactions are possible, but very fast ones (below 150 ms) are not.",
            "The Normal (Gaussian) distribution is symmetric: equal observations on either side of the mean. It is described by the mean (mu, centre) and standard deviation (sigma, width). Most RT data from a simple task falls within mu +/- 2*sigma.",
            "The Uniform distribution assigns equal probability to every value in [min, max]. It does not occur naturally in RT data but serves as a baseline model for comparison with skewed distributions.",
            "The Ex-Gaussian (normal + exponential) distribution is a favourite of cognitive psychologists. The tau parameter describes the length of the right tail - time needed for additional processes (e.g. memory search, response inhibition). Larger tau = longer tail = more slow trials.",
            "Descriptive statistics of a distribution: mean (sensitive to outliers), median (robust), standard deviation (spread), IQR (robust spread), and skewness (asymmetry). For RT data, skewness is usually positive, meaning there is a right tail.",
        ],
        "notes": [
            "RT skewness is a feature, not an error. Real RT experiment data always has a right tail - a biological effect. Using the mean without checking skewness can give a misleading picture.",
            "Sample size (N) affects histogram stability. At N=20 the histogram is noisy; at N=200 it looks smoother. But larger N does not change the distribution shape - only our estimate becomes more precise.",
            "Cohen's d and p-value measure different things. p-value depends on N: a large sample gives p<0.05 even for a trivial difference. Cohen's d shows effect size independent of N. Always report both.",
        ],
        "tasks": [
            "In Phase A: compare Normal and Ex-Gaussian histograms with the same mu and sigma. How does the shape change as you increase tau? At what tau range does skewness become clearly visible?",
            "In Phase B: guess the distribution without hints. How many attempts do you need? Which parameters are hardest to guess - mu, sigma, or tau? Why?",
            "In Phase C: set distribution A to Normal (mu=400, sigma=60, N=50) and distribution B to Ex-Gaussian (mu=400, sigma=60, tau=100, N=50). Observe Cohen's d and p-value. Now increase N in both to 200. How does p-value change? How does Cohen's d change?",
        ],
    },
}
