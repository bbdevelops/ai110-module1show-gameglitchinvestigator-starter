# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game launched in the browser. It had a number of buttons to submit a guess, starts a new game, turn on and off hints, a debug tool, and a difficulty dropdown. Initially it has a lot of bugs.
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
I used Claude Code in VSCode. I started with the planning mode, where I talked about the problems we were facing. I directed it to look at the reflections.md file and the bugs I had laid out. I also gave it #BUG markers to look for with commentary on what to fix in certain areas.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
It gave me correct suggestions pretty much right away for the bugs 1, 2, and 3 from above. I was able to reopen the game and manually test the changes to see how they worked. You can see the hints tell you to go in the correct direction now, for example.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
The initial tests that it set up weren't linked properly and lead to the tests returning an error (not pass or fail). I had to have it go over the changes it made to properly have the test acces the logic utils.
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
Mainly I decided it was fixed if I wasn't able to detect it after several attempts. I would change variables like difficulty and number of guesses etc to see if that impacted the state of game such that the bugs would manifest. I also attempted to run pytest and test it that way
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
I entered guesses to see what hints it would suggest, and it intitially showed that the code was basically crossed. The point where it should have told you to go higher, it told you to go lower, and vice versa. I also discovered that the scoring system was completely messed up by manually entering numbers, and then saw the code for it had all kinds of wacky/nonsensical scoring rules.
- Did AI help you design or understand any tests? How?
Yes. I'm somewhat new at pytest and so it helped set up the new tests. It also helped explain how to run them and then subsequently explain what they meant. The new tests had to do with testing the total score and making sure it's being updated properly throughout the game.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
During part of the process, on even numbered guesses, it was converting the secret to a string. It would then compare greater/less than alphabetically, which was incorrect, and partly why the logic was broken.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Everytime you interact with the app/site the code executes from beginning to end, called reruns. The session state acts as a memory that persists throughout reruns. It can be reset. 
- What change did you make that finally gave the game a stable secret number?
Removed the section that was changing the data type to a string. Part of the fix that was made was to do simple ==, >, and < checks in the logic_utils.py file. After that the core logic was working better though there were still many things to fix.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
- This could be a testing habit, a prompting strategy, or a way you used Git.
I'd like to strengthen my fundamentals using GitHub and pytest. The process of methodically pointing out bugs/areas for improvement, using plan mode, reviewing the plan, activating, testing afterward and making sure to commit when progress has been made is a useful loop.
- What is one thing you would do differently next time you work with AI on a coding task?
Work on the README file while making changes. Also make a detailed log of updates/changes beyond the commit messages. 
- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI is capable of making useful changes and debugging if guided. The code it generated in regard to this project was sufficient, though I'm sure there are many improvements that could be made still. If anything, the capability of the AI and the code it output were limited by my lack of expertise. A strong developer vocabulary, coding experience, and DSA knowledge all increase the force that the AI multiplies.  