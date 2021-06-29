from csv import DictReader

from event import Event
from ReactiveAggregator_static import ReactiveAggregatorStatic as ReactiveAggregator

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


def simulate_window(dataset_name: str, reactive_aggregator: ReactiveAggregator, max_events: int = None, clock_interval: int = 500, window_size: int = 5000):
    window = []
    time = 0
    with open(f"dataset/{dataset_name}.csv", 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        window_begin = - window_size

        for i, line in enumerate(csv_reader):

            # create new event
            event = Event(
                timestamp=int(line["timestamp"]),
                key=line["name"],
                value=int(line["account_balance"])
            )
            window_begin = event.timestamp - window_size

            # A. check for possible EVICTions in the window
            evict_ids = []
            for event_id, event_in_window in enumerate(window):
                if event_in_window.timestamp < window_begin:
                    # evict event_in_window!
                    evict_ids.append(event_id)
            for evict_id in evict_ids:
                start = perf_counter()
                reactive_aggregator.evict([window[evict_id]])
                time += perf_counter() - start
            window = [event_in_window for event_idx, event_in_window in enumerate(window) if event_idx not in evict_ids]

            replaced = False
            # B. check for replacements (TRIGGER) before
            for event_id, event_in_window in enumerate(window):
                if event_in_window.key == event.key:
                    start = perf_counter()
                    reactive_aggregator.trigger([event])
                    time += perf_counter() - start
                    window = [event_in_window for event_idx, event_in_window in enumerate(window) if event_idx != event_id]
                    window.append(event)
                    replaced = True
                    break;

            # C. else: INSERT the new event
            if not replaced:
                start = perf_counter()
                reactive_aggregator.insert([event])
                time += perf_counter() - start
                window.append(event)

            if max_events is not None and i + 1 >= max_events:
                break

            #print(reactive_aggregator.submit())
    print(time)
