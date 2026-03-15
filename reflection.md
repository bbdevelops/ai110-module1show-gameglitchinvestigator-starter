# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- **What did the game look like the first time you ran it?**

The game launched in the browser. It had a number of buttons to submit a guess, starts a new game, turn on and off hints, a debug tool, and a difficulty dropdown. Initially it has a lot of bugs.

- **List at least two concrete bugs you noticed at the start (for example: "the secret number kept changing" or "the hints were backwards").**

1) The game tells you to go higher up to 99 and lower at 100, so it's core logic is broken. The hints should tell you to go higher when the input guess is lower than the secret, and tell you to go lower when the input guess is higher than the secret.
2) New game button seems to not work. Clicked it expecting the options to refresh and a new game to start. Nothing seems to happen.
3) Entering a negative number results in "go lower" forever, which is a spiral to negative infinity, not a number between 1 and 100. You'd expect it to not accept numbers below one or above 100.
4) "Final score" is not accurately displayed or counted. The developer debug window shows negative points for wrong answers.
5) Difficulty settings change the number of attempts in ways that are incorrect. The middle difficulty has a higher number of attempts than the easy difficulty for example. Highest difficulty should have the lowest number of attempts.
6) After the initial entry, it seems like you have to press the submit guess button twice to successfully submit a guess.

---

## 2. How did you use AI as a teammate?

- **Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?**

I used Claude Code in VSCode. I started with the planning mode, where I talked about the problems we were facing. I directed it to look at the reflections.md file and the bugs I had laid out. I also gave it #BUG markers to look for with commentary on what to fix in certain areas.

- **Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).**

It gave me correct suggestions pretty much right away for the bugs 1, 2, and 3 from above. I was able to reopen the game and manually test the changes to see how they worked. You can see the hints tell you to go in the correct direction now, for example.

- **Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).**

The initial tests that it set up weren't linked properly and lead to the tests returning an error (not pass or fail). I had to have it go over the changes it made to properly have the test acces the logic utils.

---

## 3. Debugging and testing your fixes

- **How did you decide whether a bug was really fixed?**

Mainly I decided it was fixed if I wasn't able to detect it after several attempts. I would change variables like difficulty and number of guesses etc to see if that impacted the state of game such that the bugs would manifest. I also attempted to run pytest and test it that way.

- **Describe at least one test you ran (manual or using pytest) and what it showed you about your code.**

I entered guesses to see what hints it would suggest, and it intitially showed that the code was basically crossed. The point where it should have told you to go higher, it told you to go lower, and vice versa. I also discovered that the scoring system was completely messed up by manually entering numbers, and then saw the code for it had all kinds of wacky/nonsensical scoring rules.

- **Did AI help you design or understand any tests? How?**

Yes. I'm somewhat new at pytest and so it helped set up the new tests. It also helped explain how to run them and then subsequently explain what they meant. The new tests had to do with testing the total score and making sure it's being updated properly throughout the game.

---

## 4. What did you learn about Streamlit and state?

- **In your own words, explain why the secret number kept changing in the original app.**

During part of the process, on even numbered guesses, it was converting the secret to a string. It would then compare greater/less than alphabetically, which was incorrect, and partly why the logic was broken.

- **How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?**

Everytime you interact with the app/site the code executes from beginning to end, called reruns. The session state acts as a memory that persists throughout reruns. It can be reset. 

- **What change did you make that finally gave the game a stable secret number?**

Removed the section that was changing the data type to a string. Part of the fix that was made was to do simple ==, >, and < checks in the logic_utils.py file. After that the core logic was working better though there were still many things to fix.

---

## 5. Looking ahead: your developer habits

- **What is one habit or strategy from this project that you want to reuse in future labs or projects? This could be a testing habit, a prompting strategy, or a way you used Git.**

I'd like to strengthen my fundamentals using GitHub and pytest. The process of methodically pointing out bugs/areas for improvement, using plan mode, reviewing the plan, activating, testing afterward and making sure to commit when progress has been made is a useful loop.
- **What is one thing you would do differently next time you work with AI on a coding task?**

Work on the README file while making changes. Also make a detailed log of updates/changes beyond the commit messages. 
- **In one or two sentences, describe how this project changed the way you think about AI generated code.**

AI is capable of making useful changes and debugging if guided. The code it generated in regard to this project was sufficient, though I'm sure there are many improvements that could be made still. If anything, the capability of the AI and the code it output were limited by my lack of expertise. A strong developer vocabulary, coding experience, and DSA knowledge all increase the force that the AI multiplies.

---

## 6. AI Model Comparison: Claude Code vs. ChatGPT (GPT-4o)

### Bug used for comparison
Bug 1: the hint logic in `check_guess` was reversed — it returned `"Too High"`
when the guess was below the secret and `"Too Low"` when above. I used this bug
because it has a clear expected behavior, a small code surface (one if/else
block), and I already knew the correct fix — making it easy to evaluate both
models fairly.

### Prompt given to both models
> "Here is a Python function. The hints it returns are backwards — when the
> guess is too high it says go higher, and when too low it says go lower.
> What is wrong and how would you fix it?" [pasted the original broken function]

### Claude Code response
Claude’s response is highly concise and treats the user like an experienced developer who just wants to see what changed.

**Strengths:**
1) Directness: It gets straight to the point in the very first sentence.

2) Nuance: It correctly points out a subtle detail: "The status strings ("Too High" / "Too Low") were already correct — only the emoji hint messages had the directions flipped." This shows strong reading comprehension of the code.

3) Brevity: By only showing the lines of code that need to change (like a pull request diff), it saves the user from having to read through the boilerplate try/except setup again.

**Weaknesses:** 

1) Piecewise solution: If you are a beginner, you might prefer having the entire function rewritten so you can simply copy and paste it into your editor without having to manually stitch the snippets together.

### ChatGPT (GPT-4o) response
GPT-4o’s response is much more structured and pedagogical, treating the prompt as an opportunity to teach and provide a completely ready-to-run artifact.

**Strengths:**

1) Copy-Paste Ready: It provides the entire corrected function in one code block. For many users, this is the preferred output because it requires zero mental effort to implement.

2) Pedagogical Structure: It breaks the response into a clear "Problem," "Solution," and "Explanation" format, which is very easy to scan.

**Weaknesses:**

1) Repetitive: It over-explains a bit. It explains the exact same logic before the code block and then again in the "Explanation of Fix" section at the end.

### Bug Missed By Both

Because the prompt explicitly directed the models to look at the backward hints, both models suffered from a bit of anchoring bias. They fixed the text strings but missed a fundamental logic flaw in the except TypeError block:

```Python
except TypeError:
   g = str(guess)
   if g == secret:
        return "Win", "🎉 Correct!"
   if g > secret:
        return "Too High", "📈 Go HIGHER!"
   return "Too Low", "📉 Go LOWER
```

If the code falls into this block, it means it is comparing strings. In Python, string comparison is lexical (alphabetical), not numerical. This means "10" > "2" evaluates to False because "1" comes before "2". Neither model caught this because they were hyper-focused on fixing the emojis!

### Comparison
| Criterion | Claude Code | ChatGPT GPT-4o |
|---|---|---|
| Identified root cause | Yes, immediately | Yes, after longer explanation |
| Fix minimal / Pythonic | Yes — two-line swap | No — added unnecessary variable |
| Explanation clarity | Direct, code-focused | Friendly, somewhat verbose |
| Introduced new issues | No | No |

### Which was more Pythonic?
Neither model provided a uniquely more "Pythonic" fix because the actual code they generated was identical. Both models simply swapped the string literals inside the existing if/else statements.

To be truly "Pythonic" (which means following idiomatic Python conventions like readability, simplicity, and leveraging built-in features), a model would have needed to refactor the code entirely. The original code's use of a try/except TypeError block to handle mismatched types by converting them to strings is highly un-Pythonic. A truly Pythonic fix would have involved:

- Catching the type issue early and handling it explicitly (e.g., ensuring guess and secret are the same type before comparing).

- Using Python's int() to attempt to cast a string input into an integer, rather than casting the integer to a string, to avoid the lexical sorting bug mentioned earlier.

Since both models just accepted the flawed architecture and swapped the strings, they score equally on this front.

### Which explanation was easier to understand?
**Result:** It depends on one's experience level, but Claude's explanation is sharper.

For a beginner, GPT-4o is easier to understand. GPT-4o leaves nothing to the imagination. It explains the exact state of the code, shows the precise output, and provides the fully assembled function. A novice programmer doesn't have to mentally map the changes to their original code; they just read the "why" and paste the "what." However, its explanation is a bit bloated, repeating the same logic before and after the code block.

For an intermediate to advanced developer, Claude 4.6 Sonnet is easier to understand.
Claude's explanation is much more elegant. By stating, "The status strings ("Too High" / "Too Low") were already correct — only the emoji hint messages had the directions flipped," it pinpoints the exact cognitive error the human made when writing the code. It doesn't waste time re-explaining basic if/else logic; it just isolates the mismatch and shows the diff. It respects the user's time and intelligence.