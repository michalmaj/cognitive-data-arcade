# Theory — Big Data in Cognitive Science

## 1. What Is Big Data?

Big Data refers to datasets so large and complex that traditional data-processing tools cannot handle them. Three characteristics — often called the **three Vs** — define Big Data:

- **Volume:** The sheer quantity of data. A single fMRI session produces gigabytes of raw signal; the Human Connectome Project stores data from over 1 200 participants, totalling several terabytes.
- **Velocity:** The speed at which data is generated. Eye-tracking devices record gaze position at 250–1 000 samples per second. EEG amplifiers stream hundreds of channels at up to 10 000 Hz.
- **Variety:** The diversity of data types. Cognitive science combines brain images, behavioural logs, speech recordings, physiological signals, and electronic health records — often within a single study.

## 2. A Brief History

The measurement of cognitive processes through data begins with **Franciscus Donders** in 1868, who subtracted simple reaction times from choice reaction times to estimate the duration of a mental decision — the first recorded application of subtraction logic to behavioural data.

The late twentieth century saw the emergence of large-scale neuroimaging. Projects such as the **Human Connectome Project** (launched 2010) and **OpenNeuro** (launched 2017) made multi-gigabyte brain datasets publicly available for the first time, enabling researchers worldwide to ask questions that no single laboratory could answer alone.

The current decade extends data collection beyond the laboratory. **Digital phenotyping** — the continuous passive measurement of behaviour through smartphones — generates streams of GPS coordinates, accelerometer readings, and interaction logs that correlate with mental health states at population scale.

## 3. Key Open Datasets in Cognitive Science

**Human Connectome Project (HCP)**
Structural and functional MRI data from 1 200 healthy adults, collected at multiple sites. One of the largest and most carefully curated neuroimaging datasets, used to map the network architecture of the human brain.

**OpenNeuro**
A public repository hosting thousands of brain imaging datasets (fMRI, EEG, MEG) contributed by researchers worldwide. Data are freely downloadable under open licences, allowing secondary analysis without new data collection.

**CHILDES Corpus**
A multinational collection of transcribed child-speech recordings spanning dozens of languages and developmental stages. The foundational resource for computational and empirical research on language acquisition.

**UK Biobank**
Medical and genetic data from 500 000 UK adults, collected since 2006. Includes neuroimaging, cognitive assessments, physical measurements, and genomic sequences — enabling large-scale studies of brain ageing and psychiatric risk.

## 4. Why Scale Matters

Small samples constrain the questions researchers can ask. A study with 30 participants can detect only large effects; subtle phenomena — such as the interaction between sleep quality and memory consolidation — require hundreds or thousands of observations to reach statistical reliability.

Large datasets shift the frontier of what is discoverable. The ABCD Study (11 800 children followed longitudinally) revealed developmental trajectories invisible to earlier, smaller cohorts. UK Biobank analyses have identified genetic variants associated with cognitive ability that no previous study was sufficiently powered to detect.

Scale also introduces new methodological responsibilities: with enough data, spurious correlations become statistically significant. Researchers working with Big Data must apply rigorous multiple-comparison correction and pre-registration to avoid false discoveries.
