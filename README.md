# 🎮 Rock Paper Scissors - Advanced Edition

> What started as a simple game turned into a deep dive into advanced Python concepts. Sometimes you just want to play rock-paper-scissors, but why not learn something along the way?

## What's This About?

Remember that basic rock-paper-scissors game we all coded when learning Python? Well, I took it and asked myself: "How many advanced Python concepts can I cram into this while still keeping it fun?"

Turns out... quite a lot.

## What Makes This Different?

Instead of just checking `if user_choice == 'r'`, this version explores:

- **OOP done right** - Abstract classes, inheritance, and all that jazz
- **Smart AI opponents** - They actually learn from your patterns (okay, mostly)
- **Design patterns** - Strategy, Singleton, Factory... the whole gang's here
- **Type safety** - Because Python can be fancy too
- **Proper testing** - Yes, even for a game this simple

## Features

- 🤖 **Three AI difficulty levels** - From "my little sibling can beat this" to "wait, did it just predict my move?"
- 📊 **Stats tracking** - Because we all need validation for our rock-paper-scissors prowess
- 💾 **Save your progress** - Your win streak deserves to be remembered
- ✨ **Clean, documented code** - Future you will thank present you

## Quick Start

```bash
# Clone this bad boy
git clone https://github.com/sharifkhan96/rock-paper-scissor-Game.git
cd rock-paper-scissor-Game

# Run it
python rock-paper-scissor-Game.py

# Run tests (if you're into that)
python test_rps.py
```

## Why Did I Build This?

Honestly? I wanted to learn advanced Python concepts but reading documentation is boring. So I built something fun instead. 

This project is basically my playground for:
- Understanding how Netflix's AI recommendation system might work (okay, on a *much* smaller scale)
- Learning design patterns without falling asleep
- Actually using those type hints everyone keeps talking about
- Writing tests that don't make me want to cry

## What I Learned

The difference between knowing `class MyClass:` and actually *understanding* OOP is huge. This project forced me to:

- Think about code architecture (turns out, it matters!)
- Write code that other humans can read (shocking, I know)
- Use decorators for more than just `@property`
- Actually appreciate type hints (they're like comments that yell at you)

## Project Structure

```
├── rock-paper-scissor-Game.py      # The main game (400+ lines of learning)
├── test_rps.py          # Tests (because bugs are annoying)
├── DOCUMENTATION.md     # Everything explained in detail
├── QUICK_REFERENCE.md   # Cheat sheet for concepts
└── README.md            # You are here 👋
```

## Cool Stuff Inside

**Pattern Recognition AI**: The "Hard" difficulty actually tracks your choices and tries to predict what you'll do next. It's surprisingly effective (and mildly terrifying).

**Context Managers**: The game session tracks how long you've been playing. Not sure why I added this, but now we know I spend too much time testing AI behavior.

**Enums with Attitude**: Each choice (rock/paper/scissors) knows what it beats. Object-oriented thinking at its finest.

## Contributing

Found a bug? Want to add a "Very Hard" AI that reads your mind? PRs are welcome! 

Just remember:
- Keep it readable (we're learning here)
- Add tests if you're feeling fancy
- Type hints are your friend

## What's Next?

Some ideas I'm considering:
- [ ] Lizard and Spock mode (Big Bang Theory fans, you know)
- [ ] Multiplayer over network (because why not overcomplicate things?)
- [ ] Machine learning AI (okay, maybe that's overkill)
- [ ] GUI version (the terminal is cool, but...)

## License

MIT - Do whatever you want with it. If it helps someone learn, that's awesome.

## Final Thoughts

This started as "let me refactor this basic script" and ended up being a lesson in software engineering. If you're learning Python and want to see how basic concepts scale up to production-level code, hopefully this helps.

Also, the medium difficulty AI is legitimately hard to beat. Don't say I didn't warn you.

---

**Star this if it helped you learn something!** ⭐

Or don't. I'm not your boss. But it would make me happy. 😊
