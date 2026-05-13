# Final_Project_ACE-Emotion-Perception-Bias-Experiment
This repository contains materials to run the ACE and Emotion Perception Bias Experiment that captures emotion perception to facial expressions. This experiment is the final project for a Teachers College course CCPX5199 Programming for Psychologists.

The following are available to download:
1.	The ACE and Emotion Perception Bias Experiment Manual (including instructions for running the task)
2.	Python scripts to run the task
3.	Task stimuli

## Project introduction
This project is a PsychoPy-based behavioral experiment prototype examining emotional face perception.

Participants view human facial expressions and classify each face as angry, neutral, or happy using keyboard responses.

The broader research motivation comes from literature suggesting that individuals with adverse childhood experiences (ACEs) may show altered emotional processing, particularly heightened sensitivity to threat-related social cues.

This implementation focuses on constructing the behavioral experimental paradigm for emotion classification.

---

## Background

Emotional facial expressions are essential social cues that help individuals interpret others’ intentions, emotional states, and possible threats.

Research in developmental and affective psychology suggests that adverse early life experiences may shape emotional processing. Individuals exposed to childhood adversity may become more vigilant to threat-related cues and may be more likely to interpret ambiguous social information negatively.

One proposed mechanism is a negativity bias, which means  that neutral or ambiguous stimuli are more likely to be perceived as threatening.

This experimental paradigm is inspired by this literature and models a task that could be used to investigate emotional perception biases.

Relevant literature:

- Pollak, S. D. (2008). Mechanisms linking early experience and the emergence of emotions.
- Pollak, S. D., & Sinha, P. (2002). Effects of early experience on children's recognition of facial displays of emotion.
- Gibb, B. E., Schofield, C. A., & Coles, M. E. (2009). Reported history of childhood abuse and young adults' information-processing biases.

---

## Research Question

Does exposure to adverse childhood experiences influence emotional face perception?

More specifically:

Are individuals with higher ACE exposure more likely to interpret neutral facial expressions as negative or threatening?

---

## Hypothesis

Individuals with greater exposure to adverse childhood experiences may demonstrate a negativity bias in emotional face perception.

Specifically, they may:

- classify neutral faces as angry more frequently
- show lower accuracy for emotionally ambiguous stimuli
- respond more quickly to threat-related expressions 

---

## Experimental Design

### Independent Variable

Conceptual independent variable:

- Adverse childhood experience (ACE) exposure

(Note: ACE measurement is part of the broader research concept but is not implemented in this programming prototype.)

### Dependent Variables

Behavioral outcomes collected in this task:

- participant emotion classification response
- response accuracy
- reaction time
- misclassification patterns

---

## Task Procedure

Participants complete the following sequence:

1. Welcome screen
2. Instruction screen
3. Practice trials (3 trials with accuracy feedback)
4. Transition screen
5. Main experimental trials (without feedback) 
6. End screen


During practice trials:
Three separate practice images are included to familiarize participants with the response mapping before the formal experiment begins.

Practice trials provide immediate feedback on response accuracy.

Practice trial data are not saved in the main experimental dataset.


During each formal trial:

- a facial image appears
- participants classify the emotion using keyboard responses:
  - **F = Angry**
  - **G = Neutral**
  - **H = Happy**

Reaction time and response accuracy are recorded.

---

## Stimuli

Facial image stimuli were obtained from the Chicago Face Database (CFD).

The Chicago Face Database is a standardized, publicly available facial stimulus database developed for psychological research.

It contains high-quality photographs of diverse individuals across racial and gender groups, with validated emotional expression categories and norming data.

It is widely used in research on:

- emotion perception
- social cognition
- facial recognition
- implicit bias

Reference:

Ma, D. S., Correll, J., & Wittenbrink, B. (2015). The Chicago Face Database: A free stimulus set of faces and norming data*. Behavior Research Methods, 47(4), 1122–1135.

For this experiment, stimuli were selected from three emotional categories:

- Angry
- Neutral
- Happy

A subset of identities was selected to ensure emotional category consistency across stimuli.

---

## Software

Built using:

- Python
- PsychoPy
- pandas

---

## Folder Structure
```text
final/
│
├── main/
│   ├── data/
│   ├── stimuli/
│   ├── practice/
│   │   ├── practice_stimuli/
│   │   └── practice_trials.csv
│   ├── emotion_task_main.py
│   └── trials_main.csv
│
├── test/
│   ├── data_test/
│   ├── stimuli_test/
│   ├── emotion_task_test.py
│   └── trials_test.csv
│
├── prep/
│   ├── all_candidate_faces.csv
│   ├── select_identities.py
│   ├── select_identity.py
│   ├── selected_identities.csv
│   └── usable_faces.csv
│
└── README.md
```

---
## Repository Components

- **main/**  
  Contains the final experimental task used for the full implementation, including the main stimulus set, practice trials, and data output folder.

- **test/**  
  Contains a simplified prototype version of the experiment used for debugging and testing PsychoPy functionality before building the final implementation.

- **prep/**  
  Contains preprocessing scripts used to select eligible stimuli and generate trial files from the Chicago Face Database.
---

## How to Run

### Step 1: Generate stimuli and trial files

From the `prep/` folder, run:

python select_identities.py

This script selects eligible facial stimuli from the Chicago Face Database and generates the required trial CSV files for the experiment.

### Step 2: Start the experiment

Navigate to:

main/

Run:

python emotion_task.py

Participants will be prompted to enter:

- Participant ID
- Age
- Gender
- Ethnicity

### Data Storage

Experimental data are automatically saved in:

main/data/
---

## Output Variables

Saved data include:

- Participant_id
- Age
- Gender
- Ethnicity
- Trial number
- Stimulus filename
- Correct emotion
- Participant response
- Accuracy
- Reaction time

---

## Future Improvements

Potential future extensions:

- integrate ACE questionnaire directly into the task
- randomize response key mapping
- randomize trial order per participant
- increase stimulus sample size
- improve balancing across identities
- add statistical analysis scripts
