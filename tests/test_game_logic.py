from logic_utils import check_guess, update_score, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


def test_score_win_on_first_attempt():
    # Best possible result: guess it first try
    assert update_score(0, "Win", 1) == 100

def test_score_win_on_second_attempt():
    # Each extra attempt costs 10 points
    assert update_score(0, "Win", 2) == 90

def test_score_win_on_fifth_attempt():
    # Mid-game win
    assert update_score(0, "Win", 5) == 60

def test_score_floor_at_ten_points():
    # Winning on attempt 10 hits the minimum of 10 (not 0, not negative)
    assert update_score(0, "Win", 10) == 10

def test_score_floor_does_not_go_below_ten():
    # Attempt 11+ should still give 10, not drop below
    assert update_score(0, "Win", 11) == 10
    assert update_score(0, "Win", 20) == 10

def test_score_wrong_guess_does_not_change_score():
    # Wrong guesses ("Too High", "Too Low") leave score unchanged
    assert update_score(50, "Too High", 3) == 50
    assert update_score(50, "Too Low", 3) == 50

def test_score_loss_stays_at_zero():
    # A game with no correct guess: update_score is never called with "Win",
    # so score stays at 0 throughout
    score = 0
    score = update_score(score, "Too Low", 1)
    score = update_score(score, "Too High", 2)
    score = update_score(score, "Too Low", 3)
    assert score == 0


# ── Edge case tests for parse_guess ──────────────────────────────────────────

def test_decimal_input_is_rejected():
    # Decimals are not accepted — the user must enter a whole number.
    ok, value, err = parse_guess("49.9", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None

def test_decimal_at_boundary_is_rejected():
    # Even "50.0" (which would round/truncate to a valid integer) is rejected.
    ok, value, err = parse_guess("50.0", 1, 100)
    assert ok is False
    assert value is None

def test_zero_is_rejected_as_out_of_range():
    # The valid range starts at 1. Zero is directly adjacent — classic boundary test.
    ok, value, err = parse_guess("0", 1, 100)
    assert ok is False
    assert value is None
    assert err is not None

def test_scientific_notation_is_rejected():
    # "1e2" equals 100 mathematically but parse_guess only accepts plain integers.
    # int("1e2") raises ValueError, so it returns "That is not a number."
    ok, value, err = parse_guess("1e2", 1, 100)
    assert ok is False
    assert err == "That is not a number."
