import os
import random
import shutil
import pandas as pd

# ---------------- PATHS ----------------
cfd_path = r"F:\cfd\cfd\CFD Version 3.0\Images\CFD"
final_path = r"D:\AAA programming for psychology\final"

main_stimuli = rf"{final_path}\main\stimuli"
prep_path = rf"{final_path}\prep"

os.makedirs(main_stimuli, exist_ok=True)

# ---------------- SCAN CFD ----------------
records = []

for identity_folder in os.listdir(cfd_path):
    folder_path = os.path.join(cfd_path, identity_folder)

    if os.path.isdir(folder_path):
        emotions = []

        for file in os.listdir(folder_path):
            if file.lower().endswith(".jpg"):
                emotion = file.replace(".jpg", "").split("-")[-1]
                emotions.append(emotion)

        records.append({
            "identity": identity_folder,
            "num_images": len(emotions),
            "emotions": sorted(list(set(emotions)))
        })

df = pd.DataFrame(records)

usable_df = df[df["emotions"].apply(
    lambda x: ("A" in x) and ("N" in x) and (("HC" in x) or ("HO" in x))
)]

usable_df.to_csv(
    rf"{prep_path}\usable_faces.csv",
    index=False
)

df.to_csv(
    rf"{prep_path}\all_candidate_faces.csv",
    index=False
)

print("usable faces saved")

# ---------------- SELECT IDENTITIES ----------------
groups = ["BF", "BM", "WF", "WM"]

selected = []

for group in groups:
    subset = usable_df[usable_df["identity"].str.startswith(group)]
    chosen = subset.sample(3, random_state=42)
    selected.append(chosen)

selected_df = pd.concat(selected)

selected_df.to_csv(
    rf"{prep_path}\selected_identities.csv",
    index=False
)

print("selected identities saved")
print(selected_df)

# ---------------- BUILD TRIALS ----------------
random.seed(42)

trials = []

for identity in selected_df["identity"]:
    folder = os.path.join(cfd_path, identity)
    files = os.listdir(folder)

    angry = [f for f in files if f.endswith("-A.jpg")][0]
    neutral = [f for f in files if f.endswith("-N.jpg")][0]
    happy_options = [f for f in files if f.endswith("-HC.jpg") or f.endswith("-HO.jpg")]
    happy = random.choice(happy_options)

    selected_images = [
        (angry, "negative", "f", "A"),
        (neutral, "neutral", "g", "N"),
        (happy, "positive", "h", happy.split("-")[-1].replace(".jpg", ""))
    ]

    for filename, valence, correct_key, expression in selected_images:
        src = os.path.join(folder, filename)
        dst = os.path.join(main_stimuli, filename)

        shutil.copy2(src, dst)

        trials.append({
            "image": filename,
            "correct_valence": valence,
            "correct_key": correct_key,
            "identity": identity,
            "expression": expression
        })

trial_df = pd.DataFrame(trials)
trial_df = trial_df.sample(frac=1, random_state=42).reset_index(drop=True)

trial_df.to_csv(
    rf"{final_path}\main\trials_main.csv",
    index=False
)

print("DONE")
print("Number of trials:", len(trial_df))

# ---------------- BUILD PRACTICE VERSION ----------------
print("building practice version...")

practice_path = rf"{final_path}\main\practice"
practice_stimuli = rf"{practice_path}\practice_stimuli"

os.makedirs(practice_stimuli, exist_ok=True)

formal_identities = set(selected_df["identity"])

practice_pool = usable_df[
    ~usable_df["identity"].isin(formal_identities)
]

assert len(practice_pool) >= 3

practice_selected = practice_pool.sample(
    3,
    random_state=99
).reset_index(drop=True)

practice_specs = [
    ("negative", "A"),
    ("neutral", "N"),
    ("positive", "H")
]

practice_trials = []

for i, (valence, expression_type) in enumerate(practice_specs):
    identity = practice_selected.loc[i, "identity"]
    folder = os.path.join(cfd_path, identity)
    files = os.listdir(folder)

    if expression_type == "A":
        filename = [f for f in files if f.endswith("-A.jpg")][0]
        expression = "A"

    elif expression_type == "N":
        filename = [f for f in files if f.endswith("-N.jpg")][0]
        expression = "N"

    else:
        happy_options = [
            f for f in files
            if f.endswith("-HC.jpg") or f.endswith("-HO.jpg")
        ]
        filename = random.choice(happy_options)
        expression = filename.split("-")[-1].replace(".jpg", "")

    shutil.copy2(
        os.path.join(folder, filename),
        os.path.join(practice_stimuli, filename)
    )

    practice_trials.append({
        "image": filename,
        "correct_valence": valence,
        "correct_key": (
            "f" if valence == "negative"
            else "g" if valence == "neutral"
            else "h"
        ),
        "identity": identity,
        "expression": expression
    })

practice_df = pd.DataFrame(practice_trials)
practice_df = practice_df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

practice_df.to_csv(
    rf"{practice_path}\practice_trials.csv",
    index=False
)

print(practice_df)
print("practice version saved")

# ---------------- BUILD TEST VERSION ----------------
print("building test version...")

test_path = rf"{final_path}\test"
test_stimuli = rf"{test_path}\stimuli_test"

os.makedirs(test_stimuli, exist_ok=True)

test_df = pd.concat([
    trial_df[trial_df["correct_valence"] == "negative"].sample(1, random_state=42),
    trial_df[trial_df["correct_valence"] == "neutral"].sample(1, random_state=42),
    trial_df[trial_df["correct_valence"] == "positive"].sample(1, random_state=42),
])

test_df = test_df.sample(frac=1, random_state=42).reset_index(drop=True)

test_df.to_csv(
    rf"{test_path}\trials_test.csv",
    index=False
)

for img in test_df["image"]:
    shutil.copy2(
        os.path.join(main_stimuli, img),
        os.path.join(test_stimuli, img)
    )

print(test_df)
print("test version saved")