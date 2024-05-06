import time


def sleeper():
    """ Sleep time. """
    time.sleep(1.75)


def spinlock():
    """ Loop each character of string. """
    for _ in range(100_000_000):
        ...


def calc_performance(function):
    """ Calc time and performance of each func. """
    t1 = time.perf_counter(), time.process_time()
    function()
    t2 = time.perf_counter(), time.process_time()
    print(f"{function.__name__}()")
    print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
    print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")
    print()

if __name__ == '__main__':
    calc_performance([sleeper, spinlock])
