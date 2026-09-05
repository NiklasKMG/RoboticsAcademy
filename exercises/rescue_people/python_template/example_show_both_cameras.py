"""Example: show both drone cameras in the WebGUI panel.

HAL.get_frontal_image() / HAL.get_ventral_image() give you the raw frames.
WebGUI.py already knows how to display them: it subscribes to two ROS2
debug-image topics and forwards whatever arrives on them to the browser
panel:

    /webgui/image_debug_left   -> left panel in the browser
    /webgui/image_debug_right  -> right panel in the browser

WebGUI.py is now auto-started alongside this script (see the exercise's
"entrypoints" DB entry), so all this script needs to do is publish both
cameras to those two topics -- no need to launch WebGUI.py yourself.

Paste this into the code editor as your academy.py and run it; you should
see both cameras appear live in the WebGUI panel. Stop it again once you
have seen them, it is only meant as a quick check, not a real solution.
"""

import time

import HAL

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge


DURATION_SECONDS = 30  # how long to stream before stopping on its own
RATE_HZ = 10  # publish rate; the debug view does not need full frame rate


class DebugImagePublisher(Node):
    """Publishes both drone cameras to the topics WebGUI.py listens on."""

    def __init__(self):
        super().__init__("rescue_people_camera_preview")
        self.bridge = CvBridge()
        self.pub_left = self.create_publisher(Image, "/webgui/image_debug_left", 10)
        self.pub_right = self.create_publisher(Image, "/webgui/image_debug_right", 10)

    def publish(self, frontal_bgr, ventral_bgr):
        # HAL images are already BGR8 numpy arrays (see hal_interfaces camera.py),
        # so no color conversion is needed before handing them to cv_bridge.
        self.pub_left.publish(self.bridge.cv2_to_imgmsg(frontal_bgr, encoding="bgr8"))
        self.pub_right.publish(self.bridge.cv2_to_imgmsg(ventral_bgr, encoding="bgr8"))


if not rclpy.ok():
    rclpy.init()

gui_node = DebugImagePublisher()

print(
    f"Streaming both cameras to the WebGUI for {DURATION_SECONDS}s "
    "(left = frontal cam, right = ventral cam)...",
    flush=True,
)

start = time.time()
period = 1.0 / RATE_HZ
while time.time() - start < DURATION_SECONDS:
    frontal = HAL.get_frontal_image()
    ventral = HAL.get_ventral_image()
    gui_node.publish(frontal, ventral)
    time.sleep(period)

print("Done. Both cameras should have appeared in the WebGUI panel.", flush=True)
