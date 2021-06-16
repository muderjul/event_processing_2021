import random
from csv import DictWriter
import names


class DatasetGenerator:
    def __init__(self):
        self.header = ["timestamp", "name", "account_balance"]

    def generate_dataset(self, filename, number_events: int, max_int: int, timestamp_max_diff: int = 200):
        print(f"Generating data for {number_events} events..."
              f"max_int={max_int}"
              f"timestamp_max_diff={timestamp_max_diff}")
        data = self._generate_data(number_events, max_int, timestamp_max_diff)
        print("Saving data to file...")
        with open(f"{filename}.csv", 'w+', newline='') as csv_file:
            csv_writer = DictWriter(csv_file, self.header)
            csv_writer.writeheader()
            csv_writer.writerows(data)

    def _generate_data(self, number_events: int, max_int: int, timestamp_max_diff: int):
        print("Generating names...")
        number_names = int(number_events / 10)
        name_list = self._generate_names(number_names=number_names)

        print("Generating events...")
        result = []
        timestamp = 0
        for event_no in range(number_events):
            name = random.choice(name_list)
            account_balance = random.randint(- int(max_int / 5), max_int)

            data_point = {
                "timestamp": timestamp,
                "name": name,
                "account_balance": account_balance,
            }

            result.append(data_point)
            timestamp += random.randint(1, timestamp_max_diff)
        return result

    @staticmethod
    def _generate_names(number_names):
        result = []
        for event_no in range(number_names):
            name = names.get_full_name()
            result.append(name)
        return result


if __name__ == '__main__':
    dataset_generator = DatasetGenerator()
    dataset_generator.generate_dataset(
        filename="dataset1",
        number_events=25000,
        max_int=100000,
        timestamp_max_diff=200
    )
