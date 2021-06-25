import random
import string
from csv import DictWriter
from typing import List

import names


def _generate_name(
        realistic_names: bool,
        letters: str,
        names_so_far: List[str]
):
    i = 0
    while True:
        if realistic_names:
            candidate_name = names.get_full_name()
        else:
            candidate_name = ''.join(random.choice(letters) for _ in range(16))

        if candidate_name not in names_so_far:
            if i > 2:
                print(i)
            return candidate_name

        i += 1


class DatasetGenerator:
    def __init__(self):
        self.header = ["timestamp", "name", "account_balance"]

    def generate_dataset(
            self,
            filename: str,
            number_events: int,
            max_int: int,
            number_of_names: int = 1000,
            timestamp_max_diff: int = 200,
            unique_names_only: bool = False,
            fifo: bool = True,
            realistic_names: bool = False,
    ):
        print(f"Generating data for {number_events} events..."
              f"\nmax_int={max_int}"
              f"\nnumber_of_names={number_of_names}"
              f"\ntimestamp_max_diff={timestamp_max_diff}"
              f"\nunique_names_only={unique_names_only}"
              f"\nfifo={fifo}"
              f"\nrealistic_names={realistic_names}"
              )
        data = self._generate_data(
            number_events=number_events,
            max_int=max_int,
            number_of_names=number_of_names,
            timestamp_max_diff=timestamp_max_diff,
            unique_names_only=unique_names_only,
            fifo=fifo,
            realistic_names=realistic_names,
        )
        print("Saving data to file...")
        with open(f"{filename}.csv", 'w+', newline='') as csv_file:
            csv_writer = DictWriter(csv_file, self.header)
            csv_writer.writeheader()
            csv_writer.writerows(data)

    def _generate_data(
            self,
            number_events: int,
            max_int: int,
            number_of_names: int,
            timestamp_max_diff: int,
            unique_names_only: bool,
            fifo: bool,
            realistic_names: bool,
    ):
        print("Generating names...")
        number_of_names = number_of_names if not unique_names_only else number_events
        name_list = self._generate_names(number_names=number_of_names, realistic_names=realistic_names)

        print("Generating events...")
        result = []
        timestamp = 0 if fifo else 1000
        for event_no in range(number_events):
            name = name_list[event_no] if unique_names_only else random.choice(name_list)
            account_balance = random.randint(- int(max_int / 5), max_int)

            data_point = {
                "timestamp": timestamp,
                "name": name,
                "account_balance": account_balance,
            }

            result.append(data_point)
            if fifo:
                timestamp += random.randint(1, timestamp_max_diff)
            else:
                timestamp = 1000 + random.randint(-timestamp_max_diff, timestamp_max_diff)
        return result

    @staticmethod
    def _generate_names(number_names: int, realistic_names: bool = False):
        result = []
        letters = string.ascii_lowercase
        for event_no in range(number_names):
            if event_no % 10000 == 0:
                print(event_no)
            name = _generate_name(realistic_names, letters, result)
            result.append(name)
        return result


if __name__ == '__main__':
    dataset_generator = DatasetGenerator()
    dataset_generator.generate_dataset(
        filename="dataset2_unique_names_only",
        number_events=5000000,
        max_int=1000000,
        number_of_names=10000,
        timestamp_max_diff=200,
        unique_names_only=True,
        fifo=True,
        realistic_names=False,
    )
