import os
import pandas as pd
from psychopy import visual, core, event, gui
from datetime import datetime

print("STEP 0: imports successful")


def wait_for_enter_or_escape(win):
    keys = event.waitKeys(keyList=["return", "escape"])
    if "escape" in keys:
        win.close()
        core.quit()


def run():
    print("STEP 1: entered run()")

    # set working directory to this script's folder
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    print("STEP 2: changed working directory")
    print("Current folder:", os.getcwd())

    # participant dialog
    expInfo = {
        "Participant ID": "",
        "Age": "",
        "Gender": "",
        "Ethnicity": ""
    }

    dlg = gui.DlgFromDict(dictionary=expInfo)

    if not dlg.OK:
        core.quit()

    print("STEP 3: participant dialog completed")

    # read csv files
    practice_trials = pd.read_csv("practice/practice_trials.csv")
    main_trials = pd.read_csv("trials_main.csv")

    practice_trials = practice_trials.sample(frac=1).reset_index(drop=True)
    main_trials = main_trials.sample(frac=1).reset_index(drop=True)

    print("STEP 4: csv files loaded")

    # create window
    win = visual.Window(
        #[900, 600],
        fullscr=True,
        units="height",
        color="black"
    )

    print("STEP 5: window created")

    # ---------------- TEXT STIMULI ----------------
    welcome = visual.TextStim(
        win,
        text="Welcome to this experiment.\n\nPress Enter to continue.",
        color="white",
        height=0.05,
        wrapWidth=1.2
    )

    instruction = visual.TextStim(
        win,
        text=(
            "Instructions:\n\n"
            "In this experiment, you will see a series of human faces.\n\n"
            "Your task is to identify the emotional expression shown on each face.\n\n"
            "Press F for angry\n"
            "Press G for neutral\n"
            "Press H for happy\n\n"
            "Please respond as quickly and accurately as possible.\n\n"
            "Press Enter to continue."
        ),
        color="white",
        height=0.04,
        wrapWidth=1.2
    )

    practice_instruction = visual.TextStim(
        win,
        text=(
            "Practice Trials\n\n"
            "You will now complete 3 practice trials.\n\n"
            "During practice, you will receive feedback after each response.\n\n"
            "Press F for angry\n"
            "Press G for neutral\n"
            "Press H for happy\n\n"
            "Press Enter to begin practice."
        ),
        color="white",
        height=0.04,
        wrapWidth=1.2
    )

    formal_instruction = visual.TextStim(
        win,
        text=(
            "Practice complete.\n\n"
            "You will now begin the main experiment.\n\n"
            "This time, you will NOT receive feedback.\n\n"
            "Please respond as quickly and accurately as possible.\n\n"
            "Press Enter to begin."
        ),
        color="white",
        height=0.04,
        wrapWidth=1.2
    )

    fixation = visual.TextStim(
        win,
        text="+",
        color="white",
        height=0.08
    )

    feedback_text = visual.TextStim(
        win,
        text="",
        color="white",
        height=0.05,
        wrapWidth=1.2
    )

    end_text = visual.TextStim(
        win,
        text=(
            "You have completed the experiment.\n\n"
            "Thank you for your participation.\n\n"
            "Press any key to exit."
        ),
        color="white",
        height=0.05,
        wrapWidth=1.2
    )

    img = visual.ImageStim(
        win,
        size=(0.7, 0.7)
    )

    # response mapping
    key_map = {
        "f": "angry",
        "g": "neutral",
        "h": "happy"
    }

    correct_label_map = {
        "f": "angry",
        "g": "neutral",
        "h": "happy"
    }

    results = []

    def run_trials(trial_df, phase, image_folder, give_feedback=False):
        print(f"Starting {phase} trials")

        for i, trial in trial_df.iterrows():
            event.clearEvents()

            print(phase, "trial", i + 1, trial["image"])

            # fixation
            fixation.draw()
            win.flip()
            core.wait(0.8)

            # image
            image_path = os.path.join(image_folder, trial["image"])
            img.image = image_path
            img.draw()

            event.clearEvents()
            win.flip()

            clock = core.Clock()

            keys = event.waitKeys(
                maxWait=3.0,   
                keyList=["f", "g", "h", "escape"],
                timeStamped=clock
            )

            if keys is None:
                key = None
                rt = None
            else:
                key, rt = keys[0]

            if key == "escape":
                win.close()
                core.quit()

            correct_key = trial["correct_key"]
            correct_answer = correct_label_map[correct_key]

            if key is None:
                response = "no_response"
                correct = False
            else:
                response = key_map[key]
                correct = key == correct_key

            results.append({
                "Participant_ID": expInfo["Participant ID"],
                "Age": expInfo["Age"],
                "Gender": expInfo["Gender"],
                "Ethnicity": expInfo["Ethnicity"],
                "phase": phase,
                "trial_num": i + 1,
                "image": trial["image"],
                "identity": trial["identity"],
                "expression": trial["expression"],
                "correct_valence": trial["correct_valence"],
                "correct_key": correct_key,
                "correct_answer": correct_answer,
                "response_key": key,
                "response": response,
                "correct": correct,
                "rt": rt
            })

            if give_feedback:
                if correct:
                    feedback_text.text = "Correct"
                else:
                    feedback_text.text = (
                        "Incorrect\n\n"
                        "Remember:\n"
                        "F = Angry\n"
                        "G = Neutral\n"
                        "H = Happy"
                    )

                feedback_text.draw()
                win.flip()
                core.wait(1.0)

    # ---------------- FLOW ----------------

    welcome.draw()
    win.flip()
    wait_for_enter_or_escape(win)

    instruction.draw()
    win.flip()
    wait_for_enter_or_escape(win)

    practice_instruction.draw()
    win.flip()
    wait_for_enter_or_escape(win)

    run_trials(
        trial_df=practice_trials,
        phase="practice",
        image_folder=os.path.join("practice", "practice_stimuli"),
        give_feedback=True
    )

    formal_instruction.draw()
    win.flip()
    wait_for_enter_or_escape(win)

    run_trials(
        trial_df=main_trials,
        phase="main",
        image_folder="stimuli",
        give_feedback=False
    )

    print("STEP 6: trials completed")

    # ---------------- SAVE DATA ----------------
    os.makedirs("data", exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    output_file = os.path.join(
        "data",
        f"{expInfo['Participant ID']}_{timestamp}_experiment_data.csv"
    )

    pd.DataFrame(results).to_csv(output_file, index=False)

    print("STEP 7: data saved:", output_file)

    # ---------------- END PAGE ----------------
    end_text.draw()
    win.flip()
    event.waitKeys()

    win.close()
    core.quit()


run()