from csv import DictReader

from event import Event
from ReactiveAggregator import ReactiveAggregator


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
    with open(f"dataset/{dataset_name}.csv", 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        window_begin = - window_size

        for i, line in enumerate(csv_reader):

            # insert the new event
            event = Event(
                timestamp=int(line["timestamp"]),
                key=line["name"],
                value=int(line["account_balance"])
            )
            window_begin = event.timestamp - window_size
            reactive_aggregator.insert([event])
            window.append(event)

            # check for possible evictions in the window
            evict_ids = []
            for event_id, event_in_window in enumerate(window):
                if event_in_window.timestamp < window_begin:
                    # evict event_in_window!
                    evict_ids.append(event_id)
            for evict_id in evict_ids:
                reactive_aggregator.evict([window[evict_id]])
            window = [event_in_window for event_idx, event_in_window in enumerate(window) if event_idx not in evict_ids]

            # TODO: discuss if we should implement trigger, so do we want that events replace each other implicitly?

            if max_events is not None and i + 1 >= max_events:
                break
