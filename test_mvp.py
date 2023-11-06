import pytest
from unittest.mock import patch
# from io import StringIO
from main import game_start, validate_guess, check_input, get_board

# Test the game_start function
def test_game_start():
    with patch("builtins.input", return_value="easy"):
        assert game_start() == "easy"

    with patch("builtins.input", return_value="medium"):
        assert game_start() == "medium"

    with patch("builtins.input", return_value="hard"):
        assert game_start() == "hard"

    with patch("builtins.input", side_effect=["invalid", "easy"]):
        assert game_start() == "easy"
    

# Test the validate_guess function
def test_validate_guess():
    assert validate_guess("1234", [1, 2, 3, 4]) is True
    assert validate_guess("5678", [1, 2, 3, 4]) is False
    assert validate_guess("12345", [1, 2, 3, 4]) is False
    assert validate_guess("abcd", [1, 2, 3, 4]) is False
    assert validate_guess("8888", [1, 2, 3, 4]) is False

# Test the check_input function
def test_check_input():
    assert check_input("1234", [1, 2, 3, 4]) == {
        "board": "1234",
        "corr_num": 4,
        "corr_loc": 4,
        "continue": False,
    }

    assert check_input("5670", [1, 2, 3, 4]) == {
        "board": "5670",
        "corr_num": 0,
        "corr_loc": 0,
        "continue": True,
    }

    assert check_input("4321", [1, 2, 3, 4]) == {
        "board": "4321",
        "corr_num": 4,
        "corr_loc": 0,
        "continue": True,
    }

    assert check_input("1256", [1, 2, 3, 4]) == {
        "board": "1256",
        "corr_num": 2,
        "corr_loc": 2,
        "continue": True,
    }

# Test the get_board function (requires mocking the requests library)
def test_get_board():
    with patch("requests.get") as mock_get:
        mock_get.return_value.text = "0\n1\n2\n3"
        assert get_board("easy") == [0, 1, 2, 3]

        mock_get.return_value.text = "4\n5\n6\n7\n8\n9"
        assert get_board("medium") == [4, 5, 6, 7, 8, 9]

        mock_get.return_value.text = "0\n1\n2\n3\n4\n5\n6\n7"
        assert get_board("hard") == [0, 1, 2, 3, 4, 5, 6, 7]

if __name__ == "__main__":
    pytest.main()
