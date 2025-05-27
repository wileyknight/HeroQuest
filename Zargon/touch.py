import threading
import queue
import time
import pygwidgets
import evdev
from evdev import InputDevice, categorize, ecodes

class Touch:
    def __init__(self, dashvars, screen):
        self.dashVars = dashvars
        self.screen = screen
        self.devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        self.last = {"xy": [0,0]}
        self.current = {"xy": [0,0]}
        self.touchXY = [16200, 9550]
        self.offSet = 50
        
        # Event queue for thread-safe communication
        self.event_queue = queue.Queue()
        
        # Message queue for display
        self.message_queue = queue.Queue()
        self.current_message = ""
        self.message_timestamp = 0
        self.message_duration = 3.0
        
        # Thread management
        self.running = False
        self.thread = None
        
        # Touch state tracking with thread-safe lock
        self.position_lock = threading.Lock()
        self.touch_state = False
        self.current_touch_x = 0
        self.current_touch_y = 0
        self.touch_pressure = 0
        
        # Touch smoothing and filtering
        self.position_history = []
        self.history_size = 3  # Average last N positions
        self.min_move_threshold = 2  # Minimum pixels to register as movement
        self.last_event_time = 0
        self.min_event_interval = 0.008  # Minimum 8ms between motion events
        
        # Tap detection
        self.touch_start_pos = None
        self.touch_start_time = 0
        self.max_tap_distance = 10  # pixels
        self.max_tap_duration = 0.3  # seconds
        
        # Debug mode
        self.debug = False  # Set to True for detailed logging
        
        # Create text displays (commented out as in original)
        #self.txt = pygwidgets.DisplayText(screen, (10, 10), 'Initializing...', fontSize=24, textColor=(255,255,255))
        #self.status_txt = pygwidgets.DisplayText(screen, (10, 40), '', fontSize=18, textColor=(200,200,200))
        #self.pos_txt = pygwidgets.DisplayText(screen, (10, 70), 'Position: (0, 0)', fontSize=18, textColor=(200,200,200))
        
        # Find touchscreen device
        self.touchscreen = None
        for device in self.devices:
            if 'HID' in device.name and 'Mouse' not in device.name:
                self.add_message(f"Found: {device.name}")
                self.touchscreen = InputDevice(device.path)
                break
        
        if not self.touchscreen:
            self.add_message("ERROR: No touchscreen found!")
            raise RuntimeError("No touchscreen device found")
        
        self._show_device_capabilities()
    
    def add_message(self, message, priority=False):
        """Add a message to be displayed"""
        self.message_queue.put((time.time(), message, priority))
        if priority:
            self.current_message = message
            self.message_timestamp = time.time()
            if self.debug:
                print(f"[Touch] {message}")
    
    def _show_device_capabilities(self):
        """Show device capabilities in the display"""
        caps_msg = "Touch device ready"
        caps = self.touchscreen.capabilities()
        
        if ecodes.EV_ABS in caps:
            supported = []
            for code in caps[ecodes.EV_ABS]:
                if isinstance(code, tuple):
                    code_val = code[0]
                else:
                    code_val = code
                    
                if code_val == ecodes.ABS_PRESSURE:
                    supported.append("Pressure")
                elif code_val == ecodes.ABS_MT_TRACKING_ID:
                    supported.append("MultiTouch")
                elif code_val == ecodes.ABS_X:
                    supported.append("X-axis")
                elif code_val == ecodes.ABS_Y:
                    supported.append("Y-axis")
            
            if supported:
                caps_msg = f"Supports: {', '.join(supported)}"
                if self.debug:
                    print(f"[Touch] Device capabilities: {caps_msg}")
        
        '''self.status_txt.setValue(caps_msg)'''
    
    def getMousePos(self, touchPos, screenW, capW):
        """Convert touch coordinates to screen coordinates"""
        if capW <= self.offSet:
            return 0
        xyPct = max(0, min(100, (touchPos - self.offSet) / (capW - self.offSet) * 100))
        return int(screenW / 100 * xyPct)
    
    def smooth_position(self, x, y):
        """Apply position smoothing to reduce jitter"""
        self.position_history.append((x, y))
        if len(self.position_history) > self.history_size:
            self.position_history.pop(0)
        
        # Average the positions
        if self.position_history:
            avg_x = sum(pos[0] for pos in self.position_history) // len(self.position_history)
            avg_y = sum(pos[1] for pos in self.position_history) // len(self.position_history)
            return avg_x, avg_y
        return x, y
    
    def getScreenInfo(self):
        """Thread function to read touch events"""
        try:
            # Buffer to collect events before processing
            event_buffer = []
            last_syn_time = time.time()
            
            for event in self.touchscreen.read_loop():
                if not self.running:
                    break
                
                # Collect events until we get a SYN_REPORT
                if event.type == ecodes.EV_SYN and event.code == ecodes.SYN_REPORT:
                    current_time = time.time()
                    
                    # Process all buffered events
                    x_updated = False
                    y_updated = False
                    touch_event = None
                    raw_x = None
                    raw_y = None
                    
                    for buffered_event in event_buffer:
                        if buffered_event.type == ecodes.EV_ABS:
                            absevent = categorize(buffered_event)
                            
                            # Update coordinates
                            with self.position_lock:
                                if absevent.event.code == ecodes.ABS_X:
                                    raw_x = self.getMousePos(
                                        absevent.event.value, 
                                        self.dashVars.screenSize[0], 
                                        self.touchXY[0]
                                    )
                                    x_updated = True
                                elif absevent.event.code == ecodes.ABS_Y:
                                    raw_y = self.getMousePos(
                                        absevent.event.value, 
                                        self.dashVars.screenSize[1], 
                                        self.touchXY[1]
                                    )
                                    y_updated = True
                                
                                # Check for touch events
                                elif absevent.event.code == ecodes.ABS_PRESSURE:
                                    pressure = absevent.event.value
                                    if pressure > 0 and not self.touch_state:
                                        self.touch_state = True
                                        touch_event = 'down'
                                    elif pressure == 0 and self.touch_state:
                                        self.touch_state = False
                                        touch_event = 'up'
                                    self.touch_pressure = pressure
                                
                                elif absevent.event.code == ecodes.ABS_MT_TRACKING_ID:
                                    if absevent.event.value >= 0 and not self.touch_state:
                                        self.touch_state = True
                                        touch_event = 'down'
                                    elif absevent.event.value == -1 and self.touch_state:
                                        self.touch_state = False
                                        touch_event = 'up'
                        
                        elif buffered_event.type == ecodes.EV_KEY:
                            if buffered_event.code == ecodes.BTN_TOUCH:
                                with self.position_lock:
                                    if buffered_event.value == 1 and not self.touch_state:
                                        self.touch_state = True
                                        touch_event = 'down'
                                    elif buffered_event.value == 0 and self.touch_state:
                                        self.touch_state = False
                                        touch_event = 'up'
                    
                    # Update position if we have new coordinates
                    if (x_updated or y_updated):
                        with self.position_lock:
                            if raw_x is not None:
                                self.current_touch_x = raw_x
                            if raw_y is not None:
                                self.current_touch_y = raw_y
                            
                            # Apply smoothing for motion events
                            if self.touch_state and not touch_event:
                                smoothed_x, smoothed_y = self.smooth_position(
                                    self.current_touch_x, 
                                    self.current_touch_y
                                )
                            else:
                                # Use raw position for touch down/up
                                smoothed_x = self.current_touch_x
                                smoothed_y = self.current_touch_y
                                # Clear history on touch events
                                if touch_event:
                                    self.position_history = []
                    
                    # Handle touch events
                    if touch_event == 'down':
                        self.touch_start_pos = (smoothed_x, smoothed_y)
                        self.touch_start_time = current_time
                        # Send immediate position and down event
                        self.event_queue.put(('position', smoothed_x, smoothed_y))
                        self.event_queue.put(('down', smoothed_x, smoothed_y))
                        self.add_message(f"Touch DOWN at ({smoothed_x}, {smoothed_y})", priority=True)
                        
                    elif touch_event == 'up':
                        # Check if this was a tap
                        if self.touch_start_pos and self.touch_start_time:
                            distance = ((smoothed_x - self.touch_start_pos[0])**2 + 
                                      (smoothed_y - self.touch_start_pos[1])**2)**0.5
                            duration = current_time - self.touch_start_time
                            
                            if distance <= self.max_tap_distance and duration <= self.max_tap_duration:
                                # This was a tap - send at original position
                                tap_x, tap_y = self.touch_start_pos
                                self.event_queue.put(('position', tap_x, tap_y))
                                self.event_queue.put(('up', tap_x, tap_y))
                                self.add_message(f"TAP at ({tap_x}, {tap_y})", priority=True)
                            else:
                                # Normal touch up
                                self.event_queue.put(('position', smoothed_x, smoothed_y))
                                self.event_queue.put(('up', smoothed_x, smoothed_y))
                                self.add_message(f"Touch UP at ({smoothed_x}, {smoothed_y})", priority=True)
                        else:
                            self.event_queue.put(('position', smoothed_x, smoothed_y))
                            self.event_queue.put(('up', smoothed_x, smoothed_y))
                        
                        self.touch_start_pos = None
                        self.touch_start_time = 0
                        
                    elif self.touch_state and (x_updated or y_updated):
                        # Motion event - throttle to reduce spam
                        if current_time - self.last_event_time >= self.min_event_interval:
                            # Check if movement is significant
                            if self.last["xy"] != [smoothed_x, smoothed_y]:
                                distance = ((smoothed_x - self.last["xy"][0])**2 + 
                                          (smoothed_y - self.last["xy"][1])**2)**0.5
                                
                                if distance >= self.min_move_threshold:
                                    self.event_queue.put(('move', smoothed_x, smoothed_y))
                                    self.last_event_time = current_time
                                    if self.debug:
                                        print(f"[Touch] Move to ({smoothed_x}, {smoothed_y})")
                    
                    # Clear buffer
                    event_buffer = []
                    last_syn_time = current_time
                else:
                    # Add event to buffer
                    event_buffer.append(event)
                
        except Exception as e:
            self.add_message(f"ERROR: {str(e)}", priority=True)
            self.running = False
    
    def start(self):
        """Start the touch input thread"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self.getScreenInfo)
            self.thread.daemon = True
            self.thread.start()
            self.add_message("Touch thread started")
    
    def stop(self):
        """Stop the touch input thread"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
            self.add_message("Touch thread stopped")
    
    def update_messages(self):
        """Update displayed messages"""
        current_time = time.time()
        
        if self.current_message and (current_time - self.message_timestamp) > self.message_duration:
            self.current_message = ""
        
        while not self.message_queue.empty():
            try:
                timestamp, message, priority = self.message_queue.get_nowait()
                if not self.current_message or priority or (current_time - self.message_timestamp) > 0.5:
                    self.current_message = message
                    self.message_timestamp = timestamp
            except queue.Empty:
                break
        
        '''if self.current_message:
            self.txt.setValue(self.current_message)
        else:
            self.txt.setValue("Touch ready")'''
    
    def createTouchEvents(self, pygame):
        """Process queued events and generate pygame events"""
        # Update messages
        self.update_messages()
        
        events_processed = 0
        max_events_per_frame = 10
        
        while not self.event_queue.empty() and events_processed < max_events_per_frame:
            try:
                event_type, x, y = self.event_queue.get_nowait()
                events_processed += 1
                
                if event_type == 'position':
                    # Update position without generating event
                    self.current["xy"] = [x, y]
                    self.last["xy"] = [x, y]
                    pygame.mouse.set_pos([x, y])
                    '''self.pos_txt.setValue(f"Position: ({x}, {y})")'''
                
                elif event_type == 'move':
                    # Update position and generate motion event
                    self.current["xy"] = [x, y]
                    '''self.pos_txt.setValue(f"Position: ({x}, {y})")'''
                    
                    # Generate motion event
                    e = {'pos': [x, y], 'buttons': (1, 0, 0) if self.touch_state else (0, 0, 0)}
                    pygame.event.post(pygame.event.Event(pygame.MOUSEMOTION, e))
                    self.last["xy"] = [x, y]
                
                elif event_type == 'down':
                    # Send mouse down event
                    e = {'pos': [x, y], 'button': 1}
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONDOWN, e))
                    if self.debug:
                        print(f"[Touch] Generated MOUSEBUTTONDOWN at ({x}, {y})")
                
                elif event_type == 'up':
                    # Send mouse up event
                    e = {'pos': [x, y], 'button': 1}
                    pygame.event.post(pygame.event.Event(pygame.MOUSEBUTTONUP, e))
                    if self.debug:
                        print(f"[Touch] Generated MOUSEBUTTONUP at ({x}, {y})")
                    
            except queue.Empty:
                break
        
        # Draw all text elements
        '''self.txt.draw()
        self.status_txt.draw()
        self.pos_txt.draw()'''
    
    def set_debug(self, enabled):
        """Enable or disable debug mode"""
        self.debug = enabled
        if enabled:
            print(f"[Touch] Debug mode enabled")
            print(f"[Touch] Settings: history_size={self.history_size}, "
                  f"min_move_threshold={self.min_move_threshold}px, "
                  f"min_event_interval={self.min_event_interval}s, "
                  f"max_tap_distance={self.max_tap_distance}px, "
                  f"max_tap_duration={self.max_tap_duration}s")
    
    def __del__(self):
        """Cleanup on deletion"""
        self.stop()