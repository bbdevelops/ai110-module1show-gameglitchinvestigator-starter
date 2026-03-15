# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game launched in the browser with a number of buttons to submit a guess, starts  new game, turn on and off hints, a debug tool, and a difficulty dropdown.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
1) The game tells you to go higher up to 99 and lower at 100, so it's core logic is broken. The hints should tell you to go higher when the input guess is lower than the secret, and tell you to go lower when the input guess is higher than the secret.
2) New game button seems to not work. Clicked it expecting the options to refresh and a new game to start. Nothing seems to happen.
3) Entering a negative number results in "go lower" forever, which is a spiral to negative infinity, not a number between 1 and 100. You'd expect it to not accept numbers below one or above 100.
4) "Final score" is not accurately displayed or counted. The developer debug window shows negative points for wrong answers.
5) Difficulty settings change the number of attempts in ways that are incorrect. The middle difficulty has a higher number of attempts than the easy difficulty for example. Highest difficulty should have the lowest number of attempts.
6) After the initial entry, it seems like you have to press the submit guess button twice to successfully submit a guess.


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
