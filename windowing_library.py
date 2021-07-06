from csv import DictReader

from event import Event
from ReactiveAggregator import ReactiveAggregator

import sys
from time import perf_counter


def read_events_from_file(dataset_name: str, max_events: int):
    result = []
    with open(f"dataset/{dataset_name}.csv", 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        for i, line in enumerate(csv_reader):
            event = Event(
                timestamp=line["timestamp"],
                key=line["name"],
                value=line["account_balance"]
            )
            result.append(event)

            if i + 1 >= max_events:
                break

    return result


def simulate_window(dataset_name: str, reactive_aggregator: ReactiveAggregator, max_events: int = -1, window_size: int = 1, sliding_granularity = 1, progress=False):
    window = []
    time = 0

    # setup progress bar
    if progress:
        toolbar_width = 50
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

    with open(f"dataset/{dataset_name}.csv", 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        window_begin = - window_size
        sliding = []
        try:
            for i, line in enumerate(csv_reader):

                # progress bar
                if i%100000 == 0 and progress:
                    sys.stdout.write("=")
                    sys.stdout.flush()

                # create new event
                event = Event(
                    timestamp=i,
                    key=line["name"],
                    value=int(line["account_balance"])
                )

                # skip this loop execution if we have higher sliding_granularity
                sliding.append(event)
                if len(sliding) % sliding_granularity != 0 or i < window_size//2: # try not to scale down the tree at the beginning
                    continue

                window_begin = event.timestamp - window_size

                # A. check for possible EVICTions in the window
                evict_ids = []
                for event_id, event_in_window in enumerate(window):
                    if event_in_window.timestamp <= window_begin:
                        # evict event_in_window!
                        evict_ids.append(event_id)

                start = perf_counter()
                reactive_aggregator.evict([window[evict_id] for evict_id in evict_ids])
                time += perf_counter() - start

                window = [event_in_window for event_idx, event_in_window in enumerate(window) if event_idx not in evict_ids]


                # B. check for replacements (TRIGGER) before
                replaced = []

                # check for duplicates in sliding itself
                seen = set()  # taken and abridged from here https://stackoverflow.com/questions/480214/how-do-you-remove-duplicates-from-a-list-whilst-preserving-order
                seen_add = seen.add
                sliding = list(reversed([x for x in reversed(sliding) if not (x in seen or seen_add(x))]))

                for event in sliding:
                    for event_id, event_in_window in enumerate(window):
                        if event_in_window.key == event.key:
                            window = [event_in_window for event_idx, event_in_window in enumerate(window) if event_idx != event_id]
                            window.append(event)
                            replaced.append(event)

                start = perf_counter()
                reactive_aggregator.trigger(replaced)
                time += perf_counter() - start
                sliding = [x for x in sliding if x not in replaced]


                # C. else: INSERT the new event
                start = perf_counter()
                reactive_aggregator.insert(sliding)
                time += perf_counter() - start
                window += sliding

                if max_events != -1 and i + 1 >= max_events:
                    if progress:
                        sys.stdout.write("b\r")
                    break

                sliding = []

                if time > 180:
                    break

                #print(reactive_aggregator.submit())
        except KeyboardInterrupt:
            pass
    if progress:
        sys.stdout.write("]\r")
    return (i, time)
