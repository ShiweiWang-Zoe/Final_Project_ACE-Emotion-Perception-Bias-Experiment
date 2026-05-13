import os
import pandas as pd

base_path = r"F:\cfd\cfd\CFD Version 3.0\Images\CFD"

print("Path exists:", os.path.exists(base_path))

records = []

for identity_folder in os.listdir(base_path):
    folder_path = os.path.join(base_path, identity_folder)

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

print(usable_df)

usable_df.to_csv(
    r"D:\AAA programming for psychology\final\prep\usable_faces.csv",
    index=False
)

df.to_csv(
    r"D:\AAA programming for psychology\final\prep\all_candidate_faces.csv",
    index=False
)

print("saved to final/prep!")


import pandas as pd

usable = pd.read_csv(r"D:\AAA programming for psychology\final\prep\usable_faces.csv")

groups = ["BF", "BM", "WF", "WM"]

selected = []

for group in groups:
    subset = usable[usable["identity"].str.startswith(group)]
    chosen = subset.sample(3, random_state=42)
    selected.append(chosen)

selected_df = pd.concat(selected)

print(selected_df)

selected_df.to_csv(
    r"D:\AAA programming for psychology\final\prep\selected_identities.csv",
    index=False
)

print("saved!")