"""Example: show both drone cameras -- no WebGUI panel required.

The intended path is the browser's WebGUI panel (WebGUI.py forwards
/webgui/image_debug_left and /webgui/image_debug_right to it), but that
relies on a chain of things that are not reliably wired up for this
exercise right now (WebGUI.py is never auto-started -- see the empty
"entrypoints" column in the exercise DB -- and the internal GUI bridge on
port 2303 has shown signs of not surviving repeated tool restarts within
one session).

This script sidesteps all of that: it opens two plain OpenCV windows
directly on the simulator's own X display (":2", the same one gzclient
renders into, visible through the "Simulator" view / noVNC). No WebGUI
process, no extra websocket hop -- just HAL images in a window.

Paste this into the code editor as your academy.py and run it; check the
Simulator view (not the WebGUI camera panel) for two windows titled
"Frontal camera" and "Ventral camera". Stop it again once you have seen
them, it is only meant as a quick check, not a real solution.
"""

import os
import time

import cv2

import HAL

os.environ["DISPLAY"] = ":2"

DURATION_SECONDS = 30

print(
    f"Showing both cameras for {DURATION_SECONDS}s as OpenCV windows on the "
    "simulator display -- look at the Simulator view, not the WebGUI panel.",
    flush=True,
)

start = time.time()
while time.time() - start < DURATION_SECONDS:
    frontal = HAL.get_frontal_image()
    ventral = HAL.get_ventral_image()
    cv2.imshow("Frontal camera", frontal)
    cv2.imshow("Ventral camera", ventral)
    cv2.waitKey(1)
    time.sleep(0.05)

cv2.destroyAllWindows()
print("Done.", flush=True)
