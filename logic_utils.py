"""Pure game-logic utilities for the Glitch Guesser number-guessing game.

All functions are stateless and have no Streamlit imports, making them
independently testable with pytest.

Docstrings generated and reviewed with Claude Code (AI documentation action).
PEP 8 style review also performed with Claude Code.
"""
# Style review: PEP 8 pass performed with Claude Code (AI Fix/Review action).
# Changes: module docstring added, Google-style docstrings, return-type
# annotations on all functions, bare `except Exception` narrowed to ValueError.


def get_range_for_difficulty(difficulty: str) -> tuple[int, int]:
    """Return the inclusive (low, high) number range for a difficulty level.

    Args:
        difficulty: One of ``"Easy"``, ``"Normal"``, or ``"Hard"``.
            Unrecognised values fall back to the Hard range (1-100).

    Returns:
        A tuple ``(low, high)`` where both endpoints are inclusive integers.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100) -> tuple[bool, int | None, str | None]:
    """Parse and validate a raw text guess from the user.

    Rejects empty strings, decimal strings, non-numeric strings, and
    integers that fall outside the ``[low, high]`` range.

    Args:
        raw: The raw string entered by the player.
        low: Minimum valid integer (inclusive). Defaults to ``1``.
        high: Maximum valid integer (inclusive). Defaults to ``100``.

    Returns:
        A three-tuple ``(ok, guess_int, error_message)``:

        - ``ok`` is ``True`` only when the input is a valid in-range integer.
        - ``guess_int`` is the parsed integer, or ``None`` on failure.
        - ``error_message`` is a human-readable explanation, or ``None`` on
          success.

    Examples:
        >>> parse_guess("42", 1, 100)
        (True, 42, None)
        >>> parse_guess("3.14", 1, 100)
        (False, None, 'Enter a whole number, not a decimal.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    if "." in raw:
        return False, None, "Enter a whole number, not a decimal."

    try:
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int) -> tuple[str, str]:
    """Compare a player's guess to the secret number and return the outcome.

    Args:
        guess: The integer the player submitted.
        secret: The target integer the player is trying to find.

    Returns:
        A two-tuple ``(outcome, message)``:

        - ``outcome`` is one of ``"Win"``, ``"Too High"``, or ``"Too Low"``.
        - ``message`` is a short emoji-decorated hint shown to the player.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    else:
        return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """Calculate and return the updated score after a guess.

    Points are awarded only on a win. Wrong guesses leave the score
    unchanged. A game ended by running out of attempts (no ``"Win"``
    outcome ever reached) therefore finishes at 0.

    Scoring formula::

        points = max(10, 100 - 10 * (attempt_number - 1))

    This gives 100 points for a first-try win, 90 for the second try, and
    so on, with a floor of 10 points so a late win still rewards the player.

    Args:
        current_score: The player's score before this guess.
        outcome: The result string from :func:`check_guess`.
            Only ``"Win"`` triggers a score update.
        attempt_number: The 1-based attempt count for the current guess.

    Returns:
        The new score as an integer (always >= ``current_score``).

    Examples:
        >>> update_score(0, "Win", 1)
        100
        >>> update_score(0, "Too High", 3)
        0
    """
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number - 1))
        return current_score + points
    return current_score
