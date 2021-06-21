from windowing_library import simulate_window
from ReactiveAggregator import ReactiveAggregator

if __name__ == '__main__':
    dataset_name = "dataset1"
    max_events = 100
    reactive_aggregator = ReactiveAggregator()
    simulate_window(dataset_name, reactive_aggregator, max_events=max_events)

