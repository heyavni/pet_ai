import sys
import threading
from objc import python_method
from AppKit import (
    NSApplication, NSWindow, NSImage, NSRect, NSImageView,
    NSBackingStoreBuffered, NSImageScaleProportionallyUpOrDown, NSScreen, NSThread,
    NSWindowStyleMaskBorderless, NSWindowStyleMaskNonactivatingPanel,
    NSApplicationActivationPolicyAccessory, NSColor, NSNotificationCenter, NSApplicationDidChangeScreenParametersNotification
)
from PyObjCTools import AppHelper
import Quartz
from Foundation import NSObject
import objc
import time
import os

# Define actions with sprint images
dog_sprints = {
    "happy": ["sprint1.png"],
    "walk": ["sprint3.png", "sprint2.png"],
    "walk_back": ["sprint3_rev.png", "sprint2_rev.png"],
    "sit": ["sprint5.png"],
    "stand": ["sprint4.png"],
    "sleep": ["sprint6.png"],
    "run": ["sprint3.png", "sprint2.png"]
}

def validate_image_path(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return False
    print(f"Image found at {image_path}")
    return True

class DraggableWindow(NSWindow):
    def __new__(cls, *args, **kwargs):
        return objc.super(DraggableWindow, cls).new()

    def initWithContentRect_styleMask_backing_defer_(self, contentRect, styleMask, backing, defer):
        styleMask = NSWindowStyleMaskBorderless
        self = objc.super(DraggableWindow, self).initWithContentRect_styleMask_backing_defer_(
            contentRect, styleMask, backing, defer
        )
        if self is not None:
            # Essential settings for global visibility
            self.setMovableByWindowBackground_(True)
            self.setLevel_(Quartz.kCGFloatingWindowLevel + 2)
            
            # Window behavior settings
            collection_behavior = (
                1 << 0 |  # NSWindowCollectionBehaviorCanJoinAllSpaces
                1 << 8 |  # NSWindowCollectionBehaviorFullScreenAuxiliary
                1 << 3    # NSWindowCollectionBehaviorStationary
            )
            self.setCollectionBehavior_(collection_behavior)
            
            # Window appearance settings
            self.setOpaque_(False)
            self.setHasShadow_(True)
            self.setBackgroundColor_(NSColor.clearColor())
            self.setAlphaValue_(1.0)
            
            # Interaction settings
            self.setIgnoresMouseEvents_(False)
            self.setAcceptsMouseMovedEvents_(True)
            self.setHidesOnDeactivate_(False)
            
        return self

    def mouseDown_(self, event):
        self.dragging = True
        self.start_location = event.locationInWindow()

    def mouseDragged_(self, event):
        if self.dragging:
            new_location = self.frame().origin
            delta = (event.locationInWindow().x - self.start_location.x,
                     event.locationInWindow().y - self.start_location.y)
            new_location.x += delta[0]
            new_location.y += delta[1]
            self.setFrameOrigin_(new_location)

    def mouseUp_(self, event):
        self.dragging = False

class FloatingDogWindow(NSObject):
    def init(self):
        self = objc.super(FloatingDogWindow, self).init()
        if self is None:
            return None
        self.window = None
        self.image_view = None
        self.image_path = None
        self.app = None
        self.initialized = threading.Event()
        return self

    def initWithImagePath_(self, image_path):
        self = self.init()
        if self is None:
            return None
        self.image_path = image_path
        return self

    @objc.python_method
    def run(self):
        try:
            self.app = NSApplication.sharedApplication()
            self.app.setActivationPolicy_(NSApplicationActivationPolicyAccessory)
            
            # Register for notifications about screen changes
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                self,
                'screenParametersDidChange:',
                NSApplicationDidChangeScreenParametersNotification,
                None
            )
            
            self.app.finishLaunching()
            self.createAndShowWindow_(None)
            AppHelper.runEventLoop()
            
        except Exception as e:
            print(f"DEBUG: Exception in run sequence: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")

    def screenParametersDidChange_(self, notification):
        """Handle screen parameter changes"""
        if self.window and self.window.screen():
            # Ensure window stays visible after screen changes
            self.window.orderFrontRegardless()

    def createAndShowWindow_(self, sender):
        if not NSThread.isMainThread():
            self.performSelectorOnMainThread_withObject_waitUntilDone_(
                "createAndShowWindow:", None, True)
            return

        if not validate_image_path(self.image_path):
            return

        image = NSImage.alloc().initWithContentsOfFile_(self.image_path)
        if not image:
            return

        screen = NSScreen.mainScreen()
        if not screen:
            return
        
        screen_frame = screen.frame()
        window_width, window_height = 150, 150
        padding = 20
        x = screen_frame.size.width - window_width - padding
        y = screen_frame.size.height - window_height - padding
        
        window_frame = NSRect((x, y), (window_width, window_height))
        
        try:
            self.window = DraggableWindow.alloc().initWithContentRect_styleMask_backing_defer_(
                window_frame,
                NSWindowStyleMaskBorderless,
                NSBackingStoreBuffered,
                False
            )

            if self.window is None:
                return

            # Create and configure image view
            self.image_view = NSImageView.alloc().initWithFrame_(
                NSRect((0, 0), (window_width, window_height))
            )
            self.image_view.setImage_(image)
            self.image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
            self.image_view.setWantsLayer_(True)
            self.image_view.layer().setOpacity_(1.0)

            self.window.setContentView_(self.image_view)
            
            # Show window and bring to front
            self.window.makeKeyAndOrderFront_(None)
            self.window.orderFrontRegardless()
            
            self.initialized.set()
            
        except Exception as e:
            print(f"DEBUG: Exception during window creation: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")

    def dealloc(self):
        """Clean up notifications when the window is destroyed"""
        NSNotificationCenter.defaultCenter().removeObserver_(self)
        super().dealloc()



def perform_action(window, action, stop_event):
    if action in ["walk", "run"]:
        direction = 1  # 1 for moving right, -1 for moving left
        step_size = 20 if action == "walk" else 35
        delay = 0.2 if action == "walk" else 0.1

        while not stop_event.is_set():
            frames = dog_sprints["walk"] if direction == 1 else dog_sprints["walk_back"]
            for frame in frames:
                if stop_event.is_set():
                    break
                image_path = f"/Users/avnisoni/pup_ai/resources/sprints/{frame}"
                if validate_image_path(image_path):
                    window.performSelectorOnMainThread_withObject_waitUntilDone_(
                        "updateImage:", image_path, True
                    )

                current_frame = window.window.frame()
                current_x = current_frame.origin.x
                screen_frame = NSScreen.mainScreen().frame()
                max_x = screen_frame.size.width - current_frame.size.width
                new_x = current_x + (step_size * direction)

                if new_x < 0:
                    new_x = 0
                    direction = 1
                elif new_x > max_x:
                    new_x = max_x
                    direction = -1

                window.performSelectorOnMainThread_withObject_waitUntilDone_(
                    "moveWindow:", (new_x - current_x, 0), True
                )
                time.sleep(delay)
    else:
        frames = dog_sprints.get(action, [])
        while not stop_event.is_set():
            for frame in frames:
                if stop_event.is_set():
                    break
                image_path = f"/Users/avnisoni/pup_ai/resources/sprints/{frame}"
                if validate_image_path(image_path):
                    window.performSelectorOnMainThread_withObject_waitUntilDone_(
                        "updateImage:", image_path, True
                    )
                time.sleep(0.5)
