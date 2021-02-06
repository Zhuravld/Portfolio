import unittest
import json

from game_spec_validator import ValidationSummary, GameSpecValidator

with open('test/test_spec.json') as f:
    json_spec = json.load(f)

class Test_ValidationSummary(unittest.TestCase):

    def test_init_at_zero(self):
        self.assertEquals(
            0, ValidationSummary().severity_code
        )

    def test_update_severity(self):
        summ = ValidationSummary()
        self.assertEquals(
            1, summ._update_severity("warning")
        )
        self.assertEquals(
            2, summ._update_severity("error")
        )
        self.assertEquals(
            2, summ._update_severity("warning")
        )

    def add_failure_condition(self):
        summ = ValidationSummary()
        cond = ("warning", "There was a warning")

        summ.add_failure_condition(cond)
        self.assertEquals(
            summ.severity_code, 1
        )

        summ.add_failure_condition(cond)
        cond = ("error", "There was an error")
        self.assertEquals(
            summ.severity_code, 2
        )

    def init_from_successful_validate(self):
        failure_conditions = GameSpecValidator().validate_spec(json_spec)
        summ = ValidationSummary(failure_conditions)
        self.assertEquals(summ.severity_code, 0)

if __name__ == "__main__":
    unittest.main()
