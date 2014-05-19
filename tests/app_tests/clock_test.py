from time import sleep, time
from unittest import TestCase

from app.clock import Clock


class ClockTest(TestCase):

    def setUp(self):
        self.assert_almost_equal = lambda evaluated, expected: self.assertAlmostEqual(evaluated, expected, places=2)

    def get_started_clock(self):
        return Clock().start()

    def test_clock_should_start_at_time_zero(self):
        clock = self.get_started_clock()
        self.assert_almost_equal(clock.time_elapsed(), 0)

    def test_should_be_stoppable(self):
        clock = self.get_started_clock()
        sleep(0.1)
        self.assertGreater(clock.time_elapsed(), 0.1)
        clock.stop()
        sleep(0.1)
        self.assertEqual(clock.time_elapsed(), 0)

    def test_should_start_at_time_zero_after_being_stopped(self):
        clock = self.get_started_clock()
        clock.stop()
        clock.start()
        self.assert_almost_equal(clock.time_elapsed(), 0)

    def test_should_get_elapsed_time_between_calls_to_time(self):
        clock = self.get_started_clock()
        sleep(0.1)
        time_of_first_call = clock.time_elapsed()
        self.assertGreater(time_of_first_call, 0)
        sleep(0.2)
        self.assert_almost_equal(clock.time_elapsed(), 0.2)

    def test_should_start_at_a_time_passed_into_the_start_method(self):
        start_time = time()
        sleep(0.2)
        clock = Clock().start(at=start_time)
        self.assert_almost_equal(clock.time_elapsed(), (time() - start_time))


class ClockSynchronisationTests(TestCase):

    def setUp(self):
        self.assert_almost_equal = lambda evaluated, expected: self.assertAlmostEqual(evaluated, expected, places=2)

    def test_clocks_started_at_different_real_times_but_with_the_same_logical_start_time_should_agree_about_time(self):
        start_time = time()
        clock_1 = Clock().start(at=start_time)
        sleep(0.2)
        clock_2 = Clock().start(at=start_time)
        time_diff = clock_1.time_elapsed() - clock_2.time_elapsed()
        self.assert_almost_equal(time_diff, 0)