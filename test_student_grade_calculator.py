import unittest

from CIS261_WK10_VIBE import calculate_average, calculate_grade, create_student_record


class StudentGradeCalculatorTests(unittest.TestCase):
    def test_calculate_average(self):
        self.assertAlmostEqual(calculate_average(90, 80, 95), 88.33333333333333)

    def test_calculate_grade(self):
        self.assertEqual(calculate_grade(88), "B")
        self.assertEqual(calculate_grade(92), "A")
        self.assertEqual(calculate_grade(59), "F")

    def test_create_student_record(self):
        record = create_student_record("Alice", "S001", 90, 80, 95)
        self.assertEqual(record["name"], "Alice")
        self.assertEqual(record["id"], "S001")
        self.assertAlmostEqual(record["average"], 88.33)
        self.assertEqual(record["grade"], "B")


if __name__ == "__main__":
    unittest.main()
