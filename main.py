from csv import DictReader

from event import Event

dataset_name = "dataset1"
max_events = 100


def read_events_from_file(dataset_name: str, max_events: int):
    result = []
    with open(f"dataset/{dataset_name}.csv", 'r') as csv_file:
        csv_reader = DictReader(csv_file)
        for i, line in enumerate(csv_reader):
            print(line)
            event = Event(
                timestamp=line["timestamp"],
                key=line["name"],
                value=line["account_balance"]
            )
            result.append(event)

            if i + 1 >= max_events:
                break

    return result


if __name__ == '__main__':
    events = read_events_from_file(dataset_name, max_events)
    print(events)
