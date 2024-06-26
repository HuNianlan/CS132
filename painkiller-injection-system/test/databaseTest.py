import unittest
import sys
sys.path.append("src")

from database import InjectDatabase

class TestInjectDatabase(unittest.TestCase):

    def setUp(self):
        self.db = InjectDatabase()

    def test_get_pin(self):
        """Test case for getting the PIN."""
        self.assertEqual(self.db.Pin, "000000")
        self.assertEqual(self.db.getPin(), "000000")

    def test_set_pin(self):
        """Test case for setting the PIN."""
        self.assertEqual(self.db.Pin, "000000")
        self.db.resetPIN("123456")
        self.assertEqual(self.db.Pin, "123456")

    def test_get_bolus(self):
        """Test case for getting the bolus."""
        self.assertEqual(self.db.bolus, 0.0)
        self.assertEqual(self.db.getBolus(), 0.0)

    def test_set_bolus(self):
        """Test case for setting the bolus."""
        self.db.setBolus(0.3)
        self.assertEqual(self.db.bolus, 0.3)

    def test_get_baseline(self):
        """Test case for getting the baseline."""
        self.assertEqual(self.db.baseline, 0.0)
        self.assertEqual(self.db.getBaseline(), 0.0)

    def test_set_baseline(self):
        """Test case for setting the baseline."""
        self.db.setBaseline(0.05)
        self.assertEqual(self.db.baseline, 0.05)

    def test_get_limit_hour(self):
        """Test case for getting the hourly limit."""
        self.assertEqual(self.db.limit_hour, 1.0)
        self.assertEqual(self.db.getLimitHour(), 1.0)

    def test_set_limit_hour(self):
        """Test case for setting the hourly limit."""
        self.db.setLimitHour(0.8)
        self.assertEqual(self.db.limit_hour, 0.8)

    def test_get_limit_day(self):
        """Test case for getting the daily limit."""
        self.assertEqual(self.db.limit_day, 3.0)
        self.assertEqual(self.db.getLimitDay(), 3.0)

    def test_set_limit_day(self):
        """Test case for setting the daily limit."""
        self.db.setLimitDay(2.0)
        self.assertEqual(self.db.limit_day, 2.0)

    def test_get_status(self):
        """Test case for getting the status."""
        self.assertTrue(self.db.status)
        self.assertTrue(self.db.getStatus())

    def test_set_status(self):
        """Test case for setting the status."""
        self.db.setStatus()
        self.assertFalse(self.db.status)
        self.db.setStatus()
        self.assertTrue(self.db.status)

    def test_add_painkiller(self):
        """Test case for adding painkiller to maximum capacity."""
        self.db.addPainkiller()
        self.assertEqual(self.db.remaining, self.db.capacity)

    def test_get_remain(self):
        """Test case for getting the remaining."""
        self.assertEqual(self.db.remaining, 10.0)
        self.assertEqual(self.db.getRemain(), 10.0)

    def test_inject(self):
        """Test case for performing an injection."""
        self.db.remaining = 10
        self.db.bolus = 0.2
        self.db.inject()
        self.assertEqual(self.db.remaining, 9.8)
    
    def test_get_capacity(self):
        """Test case for getting the capacity."""
        self.assertEqual(self.db.capacity, 10.0)
        self.assertEqual(self.db.getCapacity(), 10.0)

    def test_get_bolus_history(self):
        """Test case for getting the bolus_history."""
        self.assertEqual(self.db.bolus_history, {})
        self.assertEqual(self.db.getBolusHistory(), {})
    
    def test_add_bolus_history(self):
        """Test case for adding and retrieving bolus history."""
        now = '2024-06-08 12:00:00'
        self.db.bolus = 0.2
        self.db.addBolusHistory(now)
        self.assertIn(now, self.db.bolus_history)
        self.assertEqual(self.db.bolus_history[now], 0.2)
    
    def test_get_event_history(self):
        """Test case for getting the event_history."""
        self.assertEqual(self.db.event_history, [])
        self.assertEqual(self.db.getEventHistory(), [])
    
    def test_event_history(self):
        """Test case for adding and retrieving event history."""
        time = '2024-06-08 12:00:00'
        event = "Event"
        self.db.addEventHistory(time, event)
        self.assertIn([time,event], self.db.getEventHistory())

    def test_get_bolus_history(self):
        """Test case for getting the baseline_history."""
        self.assertEqual(self.db.baseline_history, {})
        self.assertEqual(self.db.getBaselineHistory(), {})
    
    def test_add_bolus_history(self):
        """Test case for adding and retrieving baseline history."""
        now = '2024-06-08 12:00:00'
        self.db.addBaselineHistory(now,0.01)
        self.assertIn(now, self.db.baseline_history)
        self.assertEqual(self.db.baseline_history[now], 0.01)

if __name__ == '__main__':
    unittest.main()
