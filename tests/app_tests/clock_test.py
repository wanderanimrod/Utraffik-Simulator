from time import sleep
from unittest import TestCase

from app.clock import Clock


class ClockTest(TestCase):

    def test_clock_should_start_at_time_zero(self):
        clock = Clock().start()
        self.assertAlmostEqual(clock.time_elapsed(), 0, places=2)

    def test_should_be_stoppable(self):
        clock = Clock().start()
        sleep(0.1)
        self.assertGreater(clock.time_elapsed(), 0.1)
        clock.stop()
        sleep(0.1)
        self.assertEqual(clock.time_elapsed(), 0)

    def test_should_start_at_time_zero_after_being_stopped(self):
        clock = Clock().start()
        clock.stop()
        clock.start()
        self.assertAlmostEqual(clock.time_elapsed(), 0, places=2)

    def test_should_get_elapsed_time_between_calls_to_time(self):
        clock = Clock().start()
        sleep(0.1)
        time_of_first_call = clock.time_elapsed()
        self.assertGreater(time_of_first_call, 0)
        sleep(0.2)
        self.assertAlmostEqual(clock.time_elapsed(), 0.2, places=2)