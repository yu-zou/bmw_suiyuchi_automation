from pynput import keyboard
import win32gui
import time
import argparse
from tqdm import tqdm

recorded_events = []
smoothened_recorded_events = []

window_title = "chiaki-ng"

# Find game windows matching a specific substring.
def find_game_windows(window_title):
    return win32gui.FindWindow(None, window_title)

# Check if there is a game window with the specific substring.
def is_game_window(window_title):
    return bool(find_game_windows(window_title))

def on_press(key, window_title):
    if is_game_window(window_title) and key != keyboard.Key.esc:
        start_time = time.time()
        if isinstance(key, keyboard.Key):
            # If special keys
            recorded_events.append(('press', key.name, start_time, 0))
        else:
            # If it's a character key
            recorded_events.append(('press', str(key.char), start_time, 0))

def on_release(key, window_title):
    if is_game_window(window_title) and key != keyboard.Key.esc:
        end_time = time.time()
        if isinstance(key, keyboard.Key):
            # If special keys
            recorded_events.append(('release', key.name, end_time, 0))
        else:
            # If it's a character key
            recorded_events.append(('release', str(key.char), end_time, 0))
    if key == keyboard.Key.esc:
        return False

# Smoothen recorded keys by combining consecutive same-key press or release to
# single item
# Add duration to each release
def smoothen_keys(recorded_events, file):
    print('Recorded Events: ', recorded_events)
    last_event = recorded_events[0]
    for _ in recorded_events:
        if _[0] == last_event[0] and _[1] == last_event[1]:
            continue
        smoothened_recorded_events.append(last_event)
        last_event = _
    smoothened_recorded_events.append(last_event)

    for i in range(len(smoothened_recorded_events)):
        if i != 0:
            duration = smoothened_recorded_events[i][-2] - smoothened_recorded_events[i-1][-2]
            smoothened_recorded_events[i] = \
                (smoothened_recorded_events[i][0], smoothened_recorded_events[i][1], smoothened_recorded_events[i][2], duration)
    print('Smoothend record events: ', smoothened_recorded_events)
    print('Saving smoothend recorded events')
    with open(file, 'w') as f:
        for _ in smoothened_recorded_events:
            f.write(_[0] + ' ' + _[1] + ' ' + str(_[2]) + ' ' + str(_[3]) + '\n')

# Replay the recorded keyboard events.
def replay_events(window_title):
    game_window_hwnd = win32gui.FindWindow(None, window_title)

    if game_window_hwnd:
        controller = keyboard.Controller()
        repeat_count = int(input("Enter the number of times to replay: "))
        win32gui.SetForegroundWindow(game_window_hwnd)
        for _ in tqdm(range(repeat_count)):
            for event_type, key, end_time, duration in smoothened_recorded_events:
                if event_type == 'press':
                    time.sleep(duration)
                    controller.press(keyboard.Key[key] if key in keyboard.Key._member_names_ else key)
                else:
                    time.sleep(duration)
                    controller.release(keyboard.Key[key] if key in keyboard.Key._member_names_ else key)
            time.sleep(30)
            # Check if window is still alive, if not alive raise exception
            if win32gui.GetForegroundWindow() != game_window_hwnd:
                raise Exception("\nWindow is not in foreground, terminated.\n")
    else:
        raise Exception("Could not find window %s" % (window_title))

def start_listener():
    listener = keyboard.Listener(
        on_press=lambda key: on_press(key, window_title),
        on_release=lambda key: on_release(key, window_title)
    )
    print("Start recording keyboard events. Press Esc to stop recording.")
    listener.start()
    listener.join()
    print("Recording completed.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Keyboard recording and replay for a specific game window.')
    parser.add_argument('file', type=str, help='Recording file.', default=None)
    parser.add_argument('--load', action='store_true', help='Load recorded file.')
    args = parser.parse_args()

    game_window = find_game_windows(window_title)
    if not game_window:
        raise Exception("Could not find window %s" % (window_title))
    if (args.load):
        print("Start loading keyboard event file...",)
        with open(args.file, 'r') as f:
            for line in f:
                [op, key, timepoint, duration] = line.split()
                # print(op, key, float(time), float(duration))
                smoothened_recorded_events.append((op, key, float(timepoint), float(duration)))
        print("Loading completed.")

    else:
        recorded_events = []
        start_listener()
        smoothen_keys(recorded_events, args.file)

    print("Do you want to replay the recorded events? (y/n)")
    replay_choice = input()
    if replay_choice.lower() == 'y':
        print("Start replaying keyboard events.")
        replay_events(window_title)
    else:
        print("No replay.")