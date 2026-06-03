# Tasks — Event Logs and Data Formats

Complete the following steps during the lesson. Record observations in a notebook or shared document as directed by the instructor.

## Step 1: Generate a session file

Launch the application and play any reaction-time game (e.g., Lesson 02 — Reaction Time Lab) for at least 20 trials. The game automatically saves a CSV to `data/generated/`. Confirm the file exists by checking that directory in your file manager or terminal.

## Step 2: Open the CSV

Open the CSV file in a spreadsheet application (Excel, LibreOffice Calc, or Google Sheets) or in a plain-text editor (Notepad, TextEdit, VS Code).

Observe the raw file in the text editor first. Notice that the first row is the **header** (column names) and each subsequent row is one trial.

## Step 3: Identify every column

For each of the eight standard columns listed below, write one sentence in your notebook describing what it contains and why it is there:

| Column | Description |
|---|---|
| `participant_id` | |
| `session_id` | |
| `trial_id` | |
| `condition` | |
| `stimulus_onset_ms` | |
| `response_time_ms` | |
| `response_key` | |
| `correct` | |

## Step 4: Locate the reaction time

Which column contains the reaction time in milliseconds? Write its name and record the minimum and maximum values you observe across all rows.

- Minimum RT: _______ ms
- Maximum RT: _______ ms

## Step 5: Verify participant identity

Check that `participant_id` is identical in every row of the file. If you find any row with a different value, note it.

Then calculate the number of unique values in `session_id`. For a single session this should be 1. If you played two separate sessions before opening the file, it may be 2.

## Step 6: Timestamp arithmetic

Look at the `stimulus_onset_ms` column. Subtract the value in row 1 from the value in row 2. This is the **inter-trial interval** (ITI) for the first two trials.

- ITI between trial 1 and trial 2: _______ ms

Subtract the first `stimulus_onset_ms` from the last one. This is the approximate session duration in milliseconds. Convert it to seconds.

- Approximate session duration: _______ seconds

## Discussion Questions

Discuss the following questions with your group or submit written answers as instructed:

1. **Why does the CSV not contain the participant's age or gender?** Where should that information be stored, and how would it be linked to this file?
2. **If this experiment were run with EEG simultaneously**, which column would you use to align the behavioural log to the EEG recording? What additional data would you need from the EEG system?
3. **Imagine two labs run the same experiment and store results in different CSV column names.** What practical problems arise when a third researcher wants to combine both datasets? How does BIDS address this?
