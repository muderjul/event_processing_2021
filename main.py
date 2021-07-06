from windowing_library import simulate_window
from ReactiveAggregator_static import ReactiveAggregatorStatic as ReactiveAggregator

def runTest(dataset_name, window_size, max_events, sliding_granularity, progress):
    ran = False
    tree_size = window_size
    while not ran:
        try:
            reactive_aggregator = ReactiveAggregator(tree_size)
            (tuples, time) = simulate_window(dataset_name, reactive_aggregator, max_events=max_events, window_size=window_size, sliding_granularity=sliding_granularity, progress=progress)
            ran = True
            return (tuples, time)
        except ValueError as e:
            tree_size += 1

if __name__ == '__main__':
    dataset_name = "dataset2_unique_names_only_5m"
    print("from Scratch")
    for i in [2**x for x in range(14)]:
        combinedTime = 0
        time = 0
        print("Running test: Max Events: %d, window_size = %d, sliding_granularity = %d" % (i, i, 1))
        k = 0
        l = 1000
        for j in range(l):
            if 180-combinedTime-(time*(l-j)) < 0:
                continue
            (tuples, time) = runTest(dataset_name, i, i, i, progress=False)
            combinedTime += time
            k += 1
            if k%10 == 0:
                print("%f, \t%d" % (combinedTime/k*1000000, k), end='\r')
        print(combinedTime/k*1000000)

    print("ds4")
    for i in [2**x for x in range(14)]:
        test = (-1, i, 1)
        print("Running test: Max Events: %d, window_size = %d, sliding_granularity = %d" % test)
        (tuples, time) = runTest("dataset4_20_names_only_5m", test[1], test[0], test[2], progress=True)
        print(time/tuples*1000000, " "*50)

    print("ds5")
    for i in [2**x for x in range(14)]:
        test = (-1, i, 1)
        print("Running test: Max Events: %d, window_size = %d, sliding_granularity = %d" % test)
        (tuples, time) = runTest("dataset5_500_names_only_5m", test[1], test[0], test[2], progress=True)
        print(time/tuples*1000000, " "*50)

    print("sliding")
    for i in [2**x for x in range(14)]:
        for j in set([1, 4, 64, i//16, i//4, i]):
            if i < j or j == 0:
                continue
            test = (-1, i, j)
            print("Running test: Max Events: %d, window_size = %d, sliding_granularity = %d" % test)
            (tuples, time) = runTest(dataset_name, test[1], test[0], test[2], progress=True)
            print(time/tuples*1000000, " "*50)

    print("throughput additional")
    for i in [10, 25, 50, 75, 100, 150, 200]:
        test = (-1, i, 1)
        print("Running test: Max Events: %d, window_size = %d, sliding_granularity = %d" % test)
        (tuples, time) = runTest(dataset_name, test[1], test[0], test[2], progress=True)
        print(time/tuples*1000000, " "*50)
