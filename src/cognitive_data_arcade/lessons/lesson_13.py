# src/cognitive_data_arcade/lessons/lesson_13.py
"""Lesson 13 -- Distributions and Variability."""
from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Rozklad statystyczny opisuje, jak czesto wystepuja rozne wartosci w zbiorze danych. W badaniach RT najczesciej spotykamy rozklady zblizone do normalnego, ale z charakterystycznym prawym ogonem -- bo bardzo wolne reakcje sa mozliwe, a bardzo szybkie (ponizej 150 ms) nie.",
            "Rozklad normalny (Gaussa) jest symetryczny: tyle samo obserwacji po lewej co po prawej stronie sredniej. Opisuje go srednia (mu, centrum) i odchylenie standardowe (sigma, szerokosc). Wiekszosc RT-ow z prostego zadania miesci sie w przedziale mu +/- 2*sigma.",
            "Rozklad jednostajny oznacza rowne prawdopodobienstwo dla kazdej wartosci w przedziale [min, max]. W RT nie wystepuje naturalnie, ale uzywamy go jako model bazowy do porownania z rozkladami skosymi.",
            "Rozklad Ex-Gaussian (normalny + wykladniczy) jest ulubiencem psychologow poznawczych. Parametr tau opisuje dlugosc prawego ogona -- czas potrzebny na dodatkowe procesy (np. przeszukiwanie pamieci, hamowanie odpowiedzi). Wieksza tau = dluzszy ogon = wiecej wolnych prob.",
            "Statystyki opisowe rozkladu: srednia (czula na outliery), mediana (odporna), odchylenie std (rozrzut), IQR (odporny rozrzut) i skosnosc (asymetria). Dla danych RT skosnosc jest zwykle dodatnia, czyli mamy ogon w prawo.",
        ],
        "notes": [
            "Skosnosc RT-ow jest cecha, nie bledem. Prawdziwe dane z eksperymentow RT zawsze maja prawy ogon -- to efekt biologiczny. Uzywanie sredniej bez sprawdzenia skosnosci moze dac mylacy obraz.",
            "Wielkosc probki (N) wplywa na stabilnosc histogramu. Przy N=20 histogram jest haslasty; przy N=200 wyglada gladziej. Ale wieksze N nie zmienia ksztaltu rozkladu -- tylko nasz szacunek staje sie dokladniejszy.",
            "Cohen's d i p-value mierza rozne rzeczy. p-value zalezy od N: duza proba da p<0.05 nawet dla trywialnej roznicy. Cohen's d pokazuje wielkosc efektu niezaleznie od N. Zawsze raportuj oba.",
        ],
        "tasks": [
            "W Fazie A: porownaj histogramy normalnego i Ex-Gaussian z tymi samymi mu i sigma. Jak zmienia sie ksztalt gdy zwiekszasz tau? W jakim zakresie tau skosnosc staje sie wyraznie widoczna?",
            "W Fazie B: zgadnij rozklad bez wskazowek. Ile prob potrzebujesz? Ktore parametry sa najtrudniejsze do odgadniecia -- mu, sigma czy tau? Dlaczego?",
            "W Fazie C: ustaw rozklad A jako normalny (mu=400, sigma=60, N=50) i rozklad B jako Ex-Gaussian (mu=400, sigma=60, tau=100, N=50). Obserwuj Cohen's d i p-value. Teraz zwiekszaj N w obu do 200. Jak zmienia sie p-value? Jak zmienia sie Cohen's d?",
        ],
    },
    "en": {
        "theory": [
            "A statistical distribution describes how often different values appear in a dataset. RT data most often follows a distribution close to normal but with a characteristic right tail -- very slow reactions are possible, but very fast ones (below 150 ms) are not.",
            "The Normal (Gaussian) distribution is symmetric: equal observations on either side of the mean. It is described by the mean (mu, centre) and standard deviation (sigma, width). Most RT data from a simple task falls within mu +/- 2*sigma.",
            "The Uniform distribution assigns equal probability to every value in [min, max]. It does not occur naturally in RT data but serves as a baseline model for comparison with skewed distributions.",
            "The Ex-Gaussian (normal + exponential) distribution is a favourite of cognitive psychologists. The tau parameter describes the length of the right tail -- time needed for additional processes (e.g. memory search, response inhibition). Larger tau = longer tail = more slow trials.",
            "Descriptive statistics of a distribution: mean (sensitive to outliers), median (robust), standard deviation (spread), IQR (robust spread), and skewness (asymmetry). For RT data, skewness is usually positive, meaning there is a right tail.",
        ],
        "notes": [
            "RT skewness is a feature, not an error. Real RT experiment data always has a right tail -- a biological effect. Using the mean without checking skewness can give a misleading picture.",
            "Sample size (N) affects histogram stability. At N=20 the histogram is noisy; at N=200 it looks smoother. But larger N does not change the distribution shape -- only our estimate becomes more precise.",
            "Cohen's d and p-value measure different things. p-value depends on N: a large sample gives p<0.05 even for a trivial difference. Cohen's d shows effect size independent of N. Always report both.",
        ],
        "tasks": [
            "In Phase A: compare Normal and Ex-Gaussian histograms with the same mu and sigma. How does the shape change as you increase tau? At what tau range does skewness become clearly visible?",
            "In Phase B: guess the distribution without hints. How many attempts do you need? Which parameters are hardest to guess -- mu, sigma, or tau? Why?",
            "In Phase C: set distribution A to Normal (mu=400, sigma=60, N=50) and distribution B to Ex-Gaussian (mu=400, sigma=60, tau=100, N=50). Observe Cohen's d and p-value. Now increase N in both to 200. How does p-value change? How does Cohen's d change?",
        ],
    },
}
