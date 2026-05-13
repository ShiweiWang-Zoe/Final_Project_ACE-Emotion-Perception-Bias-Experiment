import os
import pandas as pd
from psychopy import visual, core, event, gui, data

print("STEP 0: imports successful")

def run():
    print("STEP 1: entered run()")
    
    # set working directory
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)
    
    print("STEP 2: changed working directory")
    print("Current folder:", os.getcwd())
    
    # participant dialog
    expInfo = {"participant": ""}
    dlg = gui.DlgFromDict(dictionary=expInfo)
    
    print("STEP 3: dialog opened")
    
    if not dlg.OK:
        core.quit()
    
    print("STEP 4: dialog completed")
    
    # read csv
    trials = pd.read_csv("trials_test.csv")
    print("STEP 5: csv loaded")
    
    # create test window
    win = visual.Window(
        [900, 600],
        fullscr=False,
        units="height",
        color="black"
    )

    print("STEP 6: window created")

    # text stimuli
    fixation = visual.TextStim(win, text="+", color="white", height=0.08)
    instruction = visual.TextStim(
        win,
        text="1 = negative\n2 = neutral\n3 = positive\n\nPress any key to start",
        color="white",
        height=0.04
    )

    img = visual.ImageStim(win, size=(0.7, 0.7))

    # show instruction
    instruction.draw()
    win.flip()
    event.waitKeys()

    results = []

    # response mapping
    key_map = {
        "1": "negative",
        "2": "neutral",
        "3": "positive"
    }

    print("STEP 7: starting trials")

    for i, trial in trials.iterrows():
        print("Trial", i + 1, trial["image"])

        # fixation
        fixation.draw()
        win.flip()
        core.wait(0.5)

        # show image
        image_path = os.path.join("stimuli_test", trial["image"])
        img.image = image_path
        img.draw()
        win.flip()

        # wait for response
        clock = core.Clock()
        keys = event.waitKeys(
            keyList=["1", "2", "3", "escape"],
            timeStamped=clock
        )

        key, rt = keys[0]

        if key == "escape":
            win.close()
            core.quit()

        response = key_map[key]
        correct = response == trial["correct_valence"]

        results.append({
            "participant": expInfo["participant"],
            "trial_num": i + 1,
            "image": trial["image"],
            "identity": trial["identity"],
            "expression": trial["expression"],
            "correct_valence": trial["correct_valence"],
            "response": response,
            "correct": correct,
            "rt": rt
        })

    print("STEP 8: trials completed")

    # save data
    os.makedirs("data_test", exist_ok=True)

    output_file = os.path.join(
        "data_test",
        expInfo["participant"] + "_test_data.csv"
    )

    pd.DataFrame(results).to_csv(output_file, index=False)

    print("STEP 9: data saved:", output_file)

    # end screen
    end_text = visual.TextStim(
        win,
        text="Done! Thank you.",
        color="white",
        height=0.05
    )
    end_text.draw()
    win.flip()
    event.waitKeys()

    win.close()
    core.quit()

run()