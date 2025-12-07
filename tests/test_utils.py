import pytest
from app.utils import normalize_phone

@pytest.mark.parametrize(
    "input_phone,expected",
    [
        ("+7 (916) 123-45-67", "+79161234567"),
        ("8 916 123 45 67", "89161234567"),
        ("  +1-202-555-0173 ", "+12025550173"),
        ("(495)123-45-67", "4951234567"),
    ],
)
def test_normalize_phone(input_phone, expected):
    assert normalize_phone(input_phone) == expected
