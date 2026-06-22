"""Lesson 13 - Distributions and Variability."""

from __future__ import annotations

CONTENT: dict[str, dict[str, list[str]]] = {
    "pl": {
        "theory": [
            "Rozkład statystyczny opisuje, jak często występują różne wartości w zbiorze danych. W badaniach RT najczęściej spotykamy rozkłady zbliżone do normalnego, ale z charakterystycznym prawym ogonem - bo bardzo wolne reakcje są możliwe, a bardzo szybkie (poniżej 150 ms) nie.",
            "Rozkład normalny (Gaussa) - Gauss opracował go w 1809 roku do modelowania błędów pomiarowych w astronomii. Twierdzenie graniczne Laplace'a (1812) wyjaśnia, dlaczego pojawia sie w przyrodzie: suma wielu niezależnych zmiennych losowych dąży do rozkładu normalnego niezależnie od rozkładu składowych.",
            "Rozkład Ex-Gaussian (normalny + wykładniczy) wprowadził do psychologii Ratcliff (1978). Parametr tau opisuje długość prawego ogona - czas potrzebny na dodatkowe procesy (np. przeszukiwanie pamięci, hamowanie odpowiedzi). Większa tau = dłuższy ogon = więcej wolnych prób.",
            "Szum różowy 1/f w RT - Gilden (2001) wykazał, że kolejne czasy reakcji w długich seriach nie są niezależne, lecz wykazują długodystansowe korelacje czasowe (tzw. szum różowy lub 1/f). Oznacza to, że chwilowy stan uwagi ma efekty trwające setki prób, co ma konsekwencje dla modeli procesu poznawczego.",
            "Rozkład jednostajny oznacza równe prawdopodobieństwo dla każdej wartości w przedziale [min, max]. W RT nie występuje naturalnie, ale używa sie go jako model bazowy do porównania z rozkładami skośnymi.",
            "Rozkład opisują: średnia (czuła na wartości odstające), mediana (odporna), odchylenie std (rozrzut), IQR (odporny rozrzut) i skośność (asymetria). Dla danych RT skośność jest zwykle dodatnia - ogon jest po prawej stronie.",
        ],
        "notes": [
            "Skośność RT jest cechą, nie błędem. Prawdziwe dane RT zawsze mają prawy ogon - to efekt biologiczny. Używanie średniej bez sprawdzenia skośności może dać mylący obraz.",
            "Wielkość próbki (N) wpływa na stabilność histogramu. Przy N=20 histogram jest hałaśliwy; przy N=200 wygląda gładziej. Większe N nie zmienia kształtu rozkładu - tylko precyzja szacunku rośnie.",
            "Cohen's d i p-value mierzą różne rzeczy. p-value zależy od N: duża próba da p<0.05 nawet dla trywialnej różnicy. Cohen's d pokazuje wielkość efektu niezależnie od N. Warto raportować oba.",
        ],
        "tasks": [
            "W Fazie A: porównaj histogramy normalnego i Ex-Gaussian z tymi samymi mu i sigma. Jak zmienia sie kształt gdy zwiększasz tau? W jakim zakresie tau skośność staje sie wyraźnie widoczna?",
            "W Fazie B: zgadnij rozkład bez wskazówek. Ile prób potrzeba? Które parametry są najtrudniejsze do odgadnięcia - mu, sigma czy tau? Dlaczego?",
            "W Fazie C: ustaw rozkład A jako normalny (mu=400, sigma=60, N=50) i rozkład B jako Ex-Gaussian (mu=400, sigma=60, tau=100, N=50). Obserwuj Cohen's d i p-value. Teraz zwiększaj N w obu do 200. Jak zmienia sie p-value? Jak zmienia sie Cohen's d?",
        ],
    },
    "en": {
        "theory": [
            "A statistical distribution describes how often different values appear in a dataset. RT data most often follows a distribution close to normal but with a characteristic right tail - very slow reactions are possible, but very fast ones (below 150 ms) are not.",
            "The Normal (Gaussian) distribution - Gauss developed it in 1809 to model measurement errors in astronomy. Laplace's central limit theorem (1812) explains why it appears in nature: the sum of many independent random variables converges to a normal distribution regardless of the distribution of the components.",
            "The Ex-Gaussian (normal + exponential) distribution was introduced into psychology by Ratcliff (1978). The tau parameter describes the length of the right tail - time needed for additional processes (e.g. memory search, response inhibition). Larger tau = longer tail = more slow trials.",
            "Pink noise 1/f in RT - Gilden (2001) demonstrated that successive reaction times in long series are not independent but display long-range temporal correlations (so-called pink or 1/f noise). This means a momentary attentional state has effects lasting hundreds of trials, with implications for cognitive process models.",
            "The Uniform distribution assigns equal probability to every value in [min, max]. It does not occur naturally in RT data but serves as a baseline model for comparison with skewed distributions.",
            "Descriptive statistics of a distribution: mean (sensitive to outliers), median (robust), standard deviation (spread), IQR (robust spread), and skewness (asymmetry). For RT data, skewness is usually positive, meaning the tail is on the right.",
        ],
        "notes": [
            "RT skewness is a feature, not an error. Real RT experiment data always has a right tail - a biological effect. Using the mean without checking skewness can give a misleading picture.",
            "Sample size (N) affects histogram stability. At N=20 the histogram is noisy; at N=200 it looks smoother. But larger N does not change the distribution shape - only the precision of the estimate increases.",
            "Cohen's d and p-value measure different things. p-value depends on N: a large sample gives p<0.05 even for a trivial difference. Cohen's d shows effect size independent of N. Reporting both is good practice.",
        ],
        "tasks": [
            "In Phase A: compare Normal and Ex-Gaussian histograms with the same mu and sigma. How does the shape change as tau increases? At what tau range does skewness become clearly visible?",
            "In Phase B: guess the distribution without hints. How many attempts are needed? Which parameters are hardest to guess - mu, sigma, or tau? Why?",
            "In Phase C: set distribution A to Normal (mu=400, sigma=60, N=50) and distribution B to Ex-Gaussian (mu=400, sigma=60, tau=100, N=50). Observe Cohen's d and p-value. Now increase N in both to 200. How does p-value change? How does Cohen's d change?",
        ],
    },
}
