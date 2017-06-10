import matplotlib.pyplot as plt

import numpy as np
import pandas as pd


def read():
    """Reads the data."""
    data = pd.read_csv('data.csv')
    data.timestamp = pd.to_datetime(data.timestamp, unit='s')
    data = data.set_index('timestamp')

    stimuli = pd.read_csv('stimuli.csv')
    stimuli.timestamp = pd.to_datetime(stimuli.timestamp, unit='s')

    return data, stimuli


def cleanup(data):
    """Applies a median filter with window size 3 to the data."""
    return data.rolling(3).median()


def get_window(stimulus, data, before=0.5, after=1):
    """Returns a window around the stimulus of the data.

    The window starts at -before and ends at after relative to the stimulus.
    The window indices are relative to the stimulus.

    Args:
        stimulus: The stimulus.
        data: The data.
        before: The offset before, relative to the stimulus.
        after: The offset after, relative to the stimulus.
    """
    before = stimulus + pd.Timedelta('{} s'.format(-before))
    after = stimulus + pd.Timedelta('{} s'.format(after))
    window = data.loc[before:after]
    window.index = (window.index - stimulus) / pd.Timedelta(seconds=1)
    return window


def find_jumps(window, offset=-10):
    """Searches for jumps by using the biggest discrete derivative with an
    offset of offset and returns the indices.

    Args:
        window: A window around a stimulus.
        offset: Number of steps between the difference.
    """
    return window.diff(offset).abs().idxmax()


def keypress(event):
    """Handles key events.

    Keys:
        q, cmd+w, escape: close the figure
        up, left: previous four samples
        down, right: next four samples

    Args:
        event: The key press event.
    """
    figure = plt.figure('EOG data')
    actions = {
        'q': lambda: plt.close(figure),
        'cmd+w': lambda: plt.close(figure),
        'escape': lambda: plt.close(figure),
        'right': lambda: __plot(figure.start + 4),
        'down': lambda: __plot(figure.start + 4),
        'left': lambda: __plot(figure.start - 4),
        'up': lambda: __plot(figure.start - 4),
    }

    try:
        actions[event.key]()
    except KeyError:
        ...


def plot(data, stimuli):
    """Prepares the plot.

    Stores the data and stimuli with the figure. Sets the start to 0.
    Plots the first set of windows.
    Connects the key events.

    Args:
        data: The data.
        stimuli: The stimuli.
    """
    figure = plt.figure('EOG data')
    figure.suptitle('EOG data (use arrows to navigate through samples)')
    figure.data = data
    figure.stimuli = stimuli
    figure.start = -4
    figure.canvas.mpl_connect('key_press_event', keypress)
    __plot(series=[8, 22, 24, 34])


def __plot(start=0, series=None):
    """Plots four windows starting at start in the figure prepared by plot.

    Args:
        start: The starting index.
    """
    figure = plt.figure('EOG data')
    if series:
        indices = series
    else:
        if start < 0:
            start = len(figure.stimuli) + start
        figure.start = start % len(figure.stimuli)

        indices = list(range(figure.start, figure.start + 4))

    for idx, stimulus in enumerate(figure.stimuli.timestamp[indices], 1):
        # Get window and jumps
        window = get_window(stimulus, figure.data)
        jumps = find_jumps(window)

        # Get colormap for jumps
        cm = plt.cm.RdYlGn(np.linspace(0, 1, len(jumps)))

        # Create subplot
        ax = figure.add_subplot(2, 2, idx)
        ax.clear()

        # Plot window and jumps
        series = ax.plot(window)
        jump_series = []
        for jump, c in zip(jumps, cm):
            jump_series.append(ax.axvline(jump, color=c, ls='--'))

        stimline = ax.axvline(0, color='k')

        # Beautify plot with labels, legend, etc.
        ax.set_xlim([-0.2, 0.6])
        ax.set_title('Stimulus {}'.format(indices[idx - 1]))
        ax.set_xlabel('time offset [seconds]')
        ax.set_ylabel('EOG')
        ax.legend(series + jump_series + [stimline],
                  [*window.keys(), *map('{}jump'.format, jumps.keys()),
                   '$t_0$'])
    figure.canvas.draw()


def main():
    data, stimuli = read()

    data = cleanup(data)

    plot(data, stimuli)

    plt.show()


if __name__ == '__main__':
    main()
