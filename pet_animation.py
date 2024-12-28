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
    # print(f"Image found at {image_path}")
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
            
            NSNotificationCenter.defaultCenter().addObserver_selector_name_object_(
                self,
                'screenParametersDidChange:',
                NSApplicationDidChangeScreenParametersNotification,
                None
            )
            
            self.app.finishLaunching()
            # Pass the initial image path here
            self.createAndShowWindow_(self.image_path)
            AppHelper.runEventLoop()
            
        except Exception as e:
            print(f"DEBUG: Exception in run sequence: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")

    def updateImage_(self, image_path):
        """Update the image in the existing window"""
        if not NSThread.isMainThread():
            self.performSelectorOnMainThread_withObject_waitUntilDone_(
                "updateImage:", image_path, True
            )
            return

        if not validate_image_path(image_path):
            return

        image = NSImage.alloc().initWithContentsOfFile_(image_path)
        if not image:
            return

        if self.image_view:
            self.image_view.setImage_(image)

    def screenParametersDidChange_(self, notification):
        """Handle screen parameter changes"""
        if self.window and self.window.screen():
            # Ensure window stays visible after screen changes
            self.window.orderFrontRegardless()

    def createAndShowWindow_(self, image_path):
        if not NSThread.isMainThread():
            self.performSelectorOnMainThread_withObject_waitUntilDone_(
                "createAndShowWindow:", image_path, True
            )
            return

        if not image_path or not validate_image_path(image_path):
            return

        image = NSImage.alloc().initWithContentsOfFile_(image_path)
        if not image:
            return

        # If window already exists, just update the image
        if self.window and self.image_view:
            self.image_view.setImage_(image)
            return

        screen = NSScreen.mainScreen()
        if not screen:
            return
        
        screen_frame = screen.frame()
        window_width, window_height = 150, 150
        padding = 20
        
        x = padding
        y = padding
        
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

            self.image_view = NSImageView.alloc().initWithFrame_(
                NSRect((0, 0), (window_width, window_height))
            )
            self.image_view.setImage_(image)
            self.image_view.setImageScaling_(NSImageScaleProportionallyUpOrDown)
            self.image_view.setWantsLayer_(True)
            self.image_view.layer().setOpacity_(1.0)

            self.window.setContentView_(self.image_view)
            self.window.makeKeyAndOrderFront_(None)
            self.window.orderFrontRegardless()
            
            self.initialized.set()
            
        except Exception as e:
            print(f"DEBUG: Exception during window creation: {str(e)}")
            import traceback
            print(f"DEBUG: Traceback: {traceback.format_exc()}")

    def moveWindow_(self, offset):
        dx, dy = offset  # Unpack the tuple
        current_frame = self.window.frame()
        new_x = current_frame.origin.x + dx
        new_y = current_frame.origin.y + dy

        # Get screen bounds
        screen_frame = NSScreen.mainScreen().frame()
        max_x = screen_frame.size.width - current_frame.size.width
        max_y = screen_frame.size.height - current_frame.size.height

        # Ensure the window stays within the screen
        new_x = max(0, min(new_x, max_x))
        new_y = max(0, min(new_y, max_y))

        # Move the window
        self.window.setFrameOrigin_((new_x, new_y))

    def dealloc(self):
        """Clean up notifications when the window is destroyed"""
        NSNotificationCenter.defaultCenter().removeObserver_(self)
        super().dealloc()



def perform_action(window, action, stop_event):
    if action in ["walk", "run"]:
        direction = 1  # 1 for moving right, -1 for moving left
        step_size = 20 if action == "walk" else 35  # Faster step size for run
        delay = 0.2 if action == "walk" else 0.1  # Faster animation for run
        
        while not stop_event.is_set():
            frames = dog_sprints["walk"] if direction == 1 else dog_sprints["walk_back"]
            for frame in frames:
                if stop_event.is_set():
                    break
                
                # Update the animation frame
                image_path = f"/Users/avnisoni/pup_ai/resources/sprints/{frame}"
                if validate_image_path(image_path):
                    window.performSelectorOnMainThread_withObject_waitUntilDone_(
                        "updateImage:", image_path, True
                    )
                
                # Get current window position and screen bounds
                current_frame = window.window.frame()
                current_x = current_frame.origin.x
                screen_frame = window.window.screen().frame()
                max_x = screen_frame.size.width - current_frame.size.width
                
                # Calculate new position
                new_x = current_x + (step_size * direction)
                
                # Check bounds and change direction if needed
                if new_x <= 0:
                    new_x = 0
                    direction = 1  # Change direction to right
                elif new_x >= max_x:
                    new_x = max_x
                    direction = -1  # Change direction to left
                
                # Move the window
                offset = (new_x - current_x, 0)  # Only move horizontally
                window.performSelectorOnMainThread_withObject_waitUntilDone_(
                    "moveWindow:", offset, True
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