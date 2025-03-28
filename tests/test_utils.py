import unittest
from datetime import datetime
from src.utils.helpers import _parse_string, _ensure_timezone

class TestParseString(unittest.TestCase):
    def test_valid_dates(self):
        test_cases = {
            "13/03/2025": _ensure_timezone(datetime(2025, 3, 13)),
            "13/03/2025 16:12:51": _ensure_timezone(datetime(2025, 3, 13, 16, 12, 51)),
            "03/13/2025 16:12:51": _ensure_timezone(datetime(2025, 3, 13, 16, 12, 51)),
            "2025-03-13": _ensure_timezone(datetime(2025, 3, 13)),
            "2025-03-13 16:12:51": _ensure_timezone(datetime(2025, 3, 13, 16, 12, 51)),
        }

        for date_str, expected in test_cases.items():
            with self.subTest(date_str=date_str):
                result = _parse_string(date_str)
                self.assertEqual(result, expected)

    def test_invalid_dates(self):
        invalid_cases = [
            "32/03/2025",  # Día inválido
            "13-03-2025",  # Formato no soportado
            "2025/03/13",  # Formato incorrecto
            "March 13, 2025",  # Formato en texto
            "13/03/25",  # Año con dos dígitos
        ]

        for date_str in invalid_cases:
            with self.subTest(date_str=date_str):
                with self.assertRaises(ValueError):
                    _parse_string(date_str)

if __name__ == "__main__":
    unittest.main()