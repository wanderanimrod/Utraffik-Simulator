from app.simulation import run


def run_sim():
    run()


if __name__ == '__main__':
    import timeit
    run_times = timeit.repeat(repeat=10, stmt='run_sim()', setup='from __main__ import run_sim', number=1)
    print "*" * 20, "min: ", min(run_times), "*" * 20
    print "*" * 20, "run times:", run_times, "*" * 20