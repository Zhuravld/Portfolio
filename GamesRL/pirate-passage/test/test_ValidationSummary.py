import unittest

from game_spec_validator import ValidationSummary, GameSpecValidator

test_spec = {
    "shape": [4, 4],
    "start": [0, 0],
    "goal": [3, 3],
    "inaccessible": [[2, 1], [1,2]],
    "pirate_routes": {
        "0": [[1,1], [1,2], [2,2], [2,1]]
    }
}


class Test_ValidationSummary(unittest.TestCase):
    def test_init_at_zero(self):
        self.assertEqual(0, ValidationSummary().severity_code)

    def test_update_severity(self):
        summ = ValidationSummary()
        self.assertEqual(1, summ._update_severity("warning"))
        self.assertEqual(2, summ._update_severity("error"))
        self.assertEqual(2, summ._update_severity("warning"))

    def add_failure_condition(self):
        summ = ValidationSummary()
        cond = ("warning", "There was a warning")

        summ.add_failure_condition(cond)
        self.assertEqual(summ.severity_code, 1)

        summ.add_failure_condition(cond)
        cond = ("error", "There was an error")
        self.assertEqual(summ.severity_code, 2)

    def init_from_successful_validate(self):
        failure_conditions = GameSpecValidator().validate_spec(test_spec)
        summ = ValidationSummary(failure_conditions)
        self.assertEqual(summ.severity_code, 0)


if __name__ == "__main__":
    unittest.main()
