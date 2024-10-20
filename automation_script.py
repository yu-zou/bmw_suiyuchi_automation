from pynput import keyboard
import win32gui
import win32process
import time
import argparse
import win32api

recorded_events = []
combined_recorded_events = []

# Get the title of the currently active window.
def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    return win32gui.GetWindowText(hwnd)

# Find game windows that contain a specific substring.
def find_game_windows(target_substring):
    game_windows = []
    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if target_substring in title:
                game_windows.append(title)
        return True
    win32gui.EnumWindows(callback, None)
    return game_windows

# Check if there is a game window with the specific substring.
def is_game_window(target_substring):
    return bool(find_game_windows(target_substring))

def on_press(key, target_substring):
    if is_game_window(target_substring) and key != keyboard.Key.esc:
        start_time = time.time()
        if isinstance(key, keyboard.Key):
            # If special keys
            recorded_events.append(('press', key.name, start_time, 0))
        else:
            # If it's a character key
            recorded_events.append(('press', str(key.char), start_time, 0))

def on_release(key, target_substring):
    if is_game_window(target_substring) and key != keyboard.Key.esc:
        end_time = time.time()
        if isinstance(key, keyboard.Key):
            # If special keys
            recorded_events.append(('release', key.name, end_time, 0))
        else:
            # If it's a character key
            recorded_events.append(('release', str(key.char), end_time, 0))
    if key == keyboard.Key.esc:
        return False

# Combine consecutive same-key press or release to single item
# Add duration to each release
def combine_keys(recorded_events, file):
    print('Recorded Events: ', recorded_events)
    last_event = recorded_events[0]
    for _ in recorded_events:
        if _[0] == last_event[0] and _[1] == last_event[1]:
            continue
        combined_recorded_events.append(last_event)
        last_event = _
    combined_recorded_events.append(last_event)

    for i in range(len(combined_recorded_events)):
        if i != 0:
            duration = combined_recorded_events[i][-2] - combined_recorded_events[i-1][-2]
            combined_recorded_events[i] = \
                (combined_recorded_events[i][0], combined_recorded_events[i][1], combined_recorded_events[i][2], duration)
    print('Combined record events: ', combined_recorded_events)
    print('Saving combined recorded events')
    with open(file, 'w') as f:
        for _ in combined_recorded_events:
            f.write(_[0] + ' ' + _[1] + ' ' + str(_[2]) + ' ' + str(_[3]) + '\n')

# Replay the recorded keyboard events.
def replay_events(target_substring):
    game_window_hwnd = None
    handles = []
    def callback(hwnd, handles):
        nonlocal game_window_hwnd
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if target_substring in title:
                game_window_hwnd = hwnd
                handles.append(game_window_hwnd)
        return True
    win32gui.EnumWindows(callback, handles)

    if len(handles) != 0:
        game_window_hwnd = handles[-1]
        if win32gui.IsWindow(game_window_hwnd) and win32gui.IsWindowEnabled(game_window_hwnd):
            controller = keyboard.Controller()
            repeat_count = int(input("Enter the number of times to replay: "))
            win32gui.SetForegroundWindow(game_window_hwnd)
            for _ in range(repeat_count):
                for event_type, key, end_time, duration in combined_recorded_events:
                    print(event_type, key, end_time, duration)
                    if event_type == 'press':
                        # if len(key) > 1:
                        #     # If it's a special key combination
                        #     keys_to_press = [getattr(keyboard.Key, k) for k in key.split('+')]
                        #     # with controller.pressed(*keys_to_press):
                        #         # time.sleep(duration)
                        # else:
                        time.sleep(duration)
                        controller.press(keyboard.Key[key] if key in keyboard.Key._member_names_ else key)
                            # time.sleep(duration)
                    else:
                        # if len(key) > 1:
                        #     # Release special key combination
                        #     keys_to_release = [getattr(keyboard.Key, k) for k in key.split('+')]
                        #     with controller.pressed(*keys_to_release):
                        #         time.sleep(duration)
                        # else:
                        time.sleep(duration)
                        controller.release(keyboard.Key[key] if key in keyboard.Key._member_names_ else key)
                time.sleep(20)
                # with controller.pressed(keyboard.Key.shift_l):
                #     time.sleep(1)
                #     controller.press('m')
                #     time.sleep(1)
                #     controller.release('m')
                # controller.press(keyboard.Key.shift_l)
                # controller.press('m')
                # time.sleep(1)
                # controller.release('m')
                # controller.release(keyboard.Key.shift_l)
    else:
        print(f"Could not find window with substring '{target_substring}'.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard recording and replay for a specific game window.')
    parser.add_argument('window_substring', type=str, help='Substring of the specific game window title.')
    parser.add_argument('file', type=str, help='Recording file.', default=None)
    parser.add_argument('--load', action='store_true', help='Load recorded file.')
    args = parser.parse_args()

    game_windows = find_game_windows(args.window_substring)
    if not game_windows:
        print(f"Cannot find any window containing '{args.window_substring}'. Program exits.")
        exit()
    else:
        print("The following possible windows are found:")
        for index, title in enumerate(game_windows):
            print(f"{index + 1}. {title}")
        choice = input("Please enter the number of the window you want to operate, or press any other key to exit: ")
        selected_index = int(choice) - 1
        time.sleep(1) # To filter out enter key
        if 0 <= selected_index < len(game_windows):
            selected_title = game_windows[selected_index]
            if (args.load):
                print("Start loading keyboard event file.")
                print("Loading completed.")
                with open(args.file, 'r') as f:
                    for line in f:
                        [op, key, timepoint, duration] = line.split()
                        # print(op, key, float(time), float(duration))
                        combined_recorded_events.append((op, key, float(timepoint), float(duration)))

            else:
                recorded_events = []
                def start_listener():
                    listener = keyboard.Listener(on_press=lambda key: on_press(key, selected_title), on_release=lambda key: on_release(key, selected_title))
                    listener.start()
                    print("Start recording keyboard events. Press Esc to stop recording.")
                    listener.join()
                    print("Recording completed.")
                start_listener()
                combine_keys(recorded_events, args.file)

            print("Do you want to replay the recorded events? (y/n)")
            replay_choice = input()
            if replay_choice.lower() == 'y':
                print("Start replaying keyboard events.")
                replay_events(selected_title)
            else:
                print("No replay.")
        else:
            print("Invalid number.")