# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca

from time import strftime
from time import gmtime

def print_progress_bar (iteration, total, length = 50, fill = '\u25A0', print_end = "\r"):
    prefix = strftime("%H:%M:%S", gmtime(total - iteration)) + '   INFO    '
    suffix = 'time left to confirm identity'
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '\u25A1' * (length - filledLength)
    print(f'\r{prefix} {bar} {suffix}', end = print_end)


def progress_bar(iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '\u25A0', print_end = "\r"):
    """use it in a loop """
    total = len(iterable)
    # Progress Bar Printing Function
    def printProgressBar (iteration):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '\u25A1' * (length - filledLength)
        print(f'\r{prefix} {bar} {percent}% {suffix}', end = print_end)
    # Initial Call
    printProgressBar(0)
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        printProgressBar(i + 1)
    # Print New Line on Complete
    print()