import os
import subprocess
import shutil
import signal
from time import sleep


def wait_click(image, timeout_seconds = 30):
    wait(image, timeout_seconds)
    sleep(1)
    # ...
    wait_target = wait(image, timeout_seconds)
    sleep(1)
    hover(wait_target)
    sleep(1)
    click(wait_target)
    sleep(1)


def wait_type(string):
    sleep(1)
    for c in string:
        sleep(0.1)
        type(c)
    sleep(1)


def install_addon():
    wait_click("1653006186042.png")
    wait_click("1653006219561.png")
    wait_click("1653006245537.png")
    wait_click("1653006260204.png")
    wait_click("1653006322280.png")
    wait("1653013496625.png")
    wait_click("1653013507589.png")
    wait_click(Pattern("1653006392352.png").targetOffset(-72,0))
    wait_click(Pattern("1653006463807.png").targetOffset(210,0))


def append_uv_sphere(bone_name):
    print("Append UV Sphere to " + bone_name)
    size = "0.2" if bone_name == "head" else "0.1"

    wait_click("1653007376739.png")
    wait_click(Pattern("1653007419304.png").targetOffset(-69,0))
    wait_click("1653007450670.png")
    wait("1653010404331.png")

    wait_click(Pattern("1653011456504.png"))
    wait_click(Pattern("1653007555060.png").targetOffset(-42,-12))

    wait_type(size)
    wait_type("\n")
    wait_click(Pattern("1653011456504.png"))
    wait_click(Pattern("1653007763700.png").targetOffset(-31,7))
    
    wait_type(size)
    wait_type("\n")
    wait_click(Pattern("1653011456504.png"))
    wait_click(Pattern("1653007801968.png").targetOffset(-34,29))
    
    wait_type(size)
    wait_type("\n")

    #click("1653008323373.png")
    wait_click("1653008343234.png")
    wait_type("Armature\n")
    wait_click("1653008471474.png")
    wait_type("b")
    wait_click("1653008569519.png")
    wait_type(bone_name)
    wait_type("\n")


Settings.MinSimilarity = 0.85

config_path = "/root/.config/blender"
if os.path.exists(config_path):
    shutil.rmtree("/root/.config/blender")
os.makedirs("/root/.config/blender/2.83/config")
os.makedirs("/root/.config/blender/2.83/scripts/addons")
os.symlink(
    "/root/io_scene_vrm",
    "/root/.config/blender/2.83/scripts/addons/VRM_Addon_for_Blender-repo",
)
os.symlink(
    "/root/tests/userpref.blend",
    "/root/.config/blender/2.83/config/userpref.blend",
)

record_my_desktop = subprocess.Popen(
    ["/usr/bin/recordmydesktop", "--no-sound", "--overwrite", "-o", "latest_capture.ogv"],
    cwd="/root",
    shell=False,
)

success = False
try:
    blender = subprocess.Popen(
        ["/root/blender/blender-softwaregl"],
        cwd="/root",
    )

    wait_click("1653006088062.png", 60)

    dragDrop("1653009624328.png", "1653009705365.png")

    # install_addon()

    wait_click("1653013745955.png")

    sleep(2)
    wait_type("n")
    sleep(2)

    wait_click("1653007264570.png")

    wait_click("1653007301490.png")
    wait("1653007349148.png")

    wait_click("1653007513161.png")
    wait_click("1653008285770.png")
    wait_click("1653008323373.png")
    wait_click("1653008343234.png")
    sleep(1)
    wait_type("Armature\n")
    sleep(1)
    wait_click("1653008471474.png")
    sleep(1)
    wait_type("b")
    sleep(1)
    wait_click("1653008569519.png")
    sleep(1)
    wait_type("spine\n")
    sleep(1)

    wait_click(Pattern("1653011456504.png"))
    wait_click(Pattern("1653007555060.png").targetOffset(-40,-13))

    sleep(0.5)
    wait_type("0.2")
    sleep(0.5)
    wait_type("\n")
    sleep(0.5)

    wait_click(Pattern("1653011456504.png"))
    wait_click(Pattern("1653007763700.png").targetOffset(-25,6))

    sleep(0.5)
    wait_type("0.2")
    sleep(0.5)
    wait_type("\n")
    sleep(0.5)

    wait_click(Pattern("1653011456504.png"))
    wait_click(Pattern("1653007801968.png").targetOffset(-28,27))

    sleep(0.5)
    wait_type("0.2")
    sleep(0.5)
    wait_type("\n")
    sleep(0.5)

    for bone_name in [
        "head",
        "upper_leg.L",
        "lower_leg.L",
        "upper_leg.R",
        "lower_leg.R",
        "upper_arm.L",
        "hand.L",
        "upper_arm.R",
        "hand.R",
    ]:
        append_uv_sphere(bone_name)

    wait_click("1653012330136.png")
    wait_click("1653012350151.png")
    wait_click("1653012365257.png")
    wait_click("1653012399042.png")

    output_path = "/root/untitled.vrm"

    # wait for save
    for retry in range(10):
        sleep(3)
        if os.path.exists(output_path):
            break

    shutil.copy(output_path, "/root/tests/output.vrm")
    blender.kill()
    success = True
finally:
    if record_my_desktop.poll() is None:
        if success:
            print("EXIT VIDEO RECORDER...")
            record_my_desktop.send_signal(signal.SIGINT)
            sleep(1)
            if record_my_desktop.poll() is None:
                record_my_desktop.send_signal(signal.SIGINT)
            sleep(1)
            if record_my_desktop.poll() is None:
                record_my_desktop.send_signal(signal.SIGTERM)
        else:
            print("START VIDEO ENCODING...")
            record_my_desktop.send_signal(signal.SIGINT)
        for _ in range(60):
            v = record_my_desktop.poll()
            if v is not None:
                break
            print("... WAITING => " + str(v))
            sleep(5)
        if record_my_desktop.poll() is None:
            print("... GIVE UP!")
            record_my_desktop.kill()
        print("... DONE! => " + str(v))
