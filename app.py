import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

# ── Bug 5 fix: use session_state to control the selectbox value so we can
# revert it programmatically if the user cancels a difficulty change.
if "difficulty_select" not in st.session_state:
    st.session_state.difficulty_select = "Normal"
if "active_difficulty" not in st.session_state:
    st.session_state.active_difficulty = "Normal"

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    key="difficulty_select",
)

# Detect a pending difficulty change and ask the user to confirm.
if difficulty != st.session_state.active_difficulty:
    st.warning(
        f"⚠️ Switching to **{difficulty}** will reset your current game. "
        "Do you want to continue?"
    )
    col_yes, col_no = st.columns(2)
    with col_yes:
        if st.button("Yes, reset game"):
            st.session_state.active_difficulty = difficulty
            low_new, high_new = get_range_for_difficulty(difficulty)
            st.session_state.secret = random.randint(low_new, high_new)
            st.session_state.attempts = 1
            st.session_state.score = 0
            st.session_state.status = "playing"
            st.session_state.history = []
            st.rerun()
    with col_no:
        if st.button("No, keep playing"):
            # Revert the selectbox to the active difficulty.
            st.session_state.difficulty_select = st.session_state.active_difficulty
            st.rerun()
    st.stop()

# Use only the confirmed difficulty from here on.
difficulty = st.session_state.active_difficulty

# ── FIX: Corrected attempt limits so Easy > Normal > Hard (more attempts = easier).
attempt_limit_map = {
    "Easy": 10,
    "Normal": 7,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "high_score" not in st.session_state:
    st.session_state.high_score = 0

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts + 1}"
)

# ── Bug 6 fix: use st.form so that pressing Enter OR clicking the button
# both trigger a single rerun with the guess value captured together.
with st.form("guess_form", clear_on_submit=True):
    raw_guess = st.text_input("Enter your guess:")
    submit = st.form_submit_button("Submit Guess 🚀")

col1, col2 = st.columns(2)
with col1:
    new_game = st.button("New Game 🔁")
with col2:
    show_hint = st.checkbox("Show hint", value=True)

# ── FIX: Reset all state on new game. Status is reset so st.stop() below
# does not fire and block the new game from starting.
if new_game:
    st.session_state.status = "playing"
    st.session_state.attempts = 1
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

# ── FIX: Guard is placed after new_game handling so a reset always runs first.
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        st.session_state.history.append({"guess": raw_guess, "outcome": "Invalid"})
        st.error(err)
    else:
        assert guess_int is not None
        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.history.append({"guess": guess_int, "outcome": outcome})

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if st.session_state.score > st.session_state.high_score:
            st.session_state.high_score = st.session_state.score

        st.session_state.attempts += 1

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts > attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Stretch 2 (Agent Mode): Sidebar panels are placed here, AFTER the submit
# logic, so session_state.history and high_score already reflect the current
# guess when the sidebar renders — eliminating the one-guess display lag.
st.sidebar.divider()
st.sidebar.subheader("Session High Score")
st.sidebar.metric("Best Score", st.session_state.get("high_score", 0))

st.sidebar.divider()
st.sidebar.subheader("Guess History")
history = st.session_state.get("history", [])
if not history:
    st.sidebar.caption("No guesses yet.")
else:
    for entry in reversed(history):
        guess_val = entry["guess"]
        outcome = entry["outcome"]
        if outcome == "Invalid":
            st.sidebar.caption(f"? {guess_val} — invalid input")
        elif outcome == "Win":
            st.sidebar.caption(f"✅ {guess_val} — correct!")
        elif outcome == "Too High":
            st.sidebar.caption(f"⬇️ {guess_val} — too high")
        elif outcome == "Too Low":
            st.sidebar.caption(f"⬆️ {guess_val} — too low")

# ── Debug panel placed here so it renders AFTER the submit logic updates
# session_state, meaning it always reflects the current guess's result.
with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
