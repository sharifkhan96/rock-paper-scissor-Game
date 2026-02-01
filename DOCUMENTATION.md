# Advanced Python Concepts Documentation

## Rock-Paper-Scissors Game - Advanced Implementation

This document explains all the advanced Python concepts implemented in the enhanced version.

---

## 1. Object-Oriented Programming (OOP)

### Classes and Inheritance
- **Abstract Base Classes (ABC)**: `Player` is an abstract base class that defines the interface for all player types
- **Inheritance**: `HumanPlayer` and `ComputerPlayer` inherit from `Player`
- **Polymorphism**: Different player types implement `make_choice()` differently

```python
class Player(ABC):
    @abstractmethod
    def make_choice(self) -> Choice:
        pass

class HumanPlayer(Player):
    def make_choice(self) -> Choice:
        # Human-specific implementation
```

### Encapsulation
- **Property Decorators**: Used for controlled access to attributes
- **Private Attributes**: Prefixed with `_` (e.g., `_name`, `_stats`)
- **Getters**: Properties expose data in controlled manner

```python
@property
def name(self) -> str:
    return self._name

@property
def win_rate(self) -> float:
    return (self.wins / self.total_games * 100) if self.total_games > 0 else 0.0
```

---

## 2. Design Patterns

### Strategy Pattern
Allows switching AI behavior at runtime:
- `RandomStrategy`: Random choices
- `CounterStrategy`: Counters player's most common choice
- `PatternStrategy`: Detects and exploits patterns

```python
class ComputerPlayer(Player):
    def set_strategy(self, strategy: PlayerStrategy) -> None:
        self._strategy = strategy
```

### Singleton Pattern
`GameConfig` ensures only one configuration instance exists:

```python
class GameConfig:
    _instance: Optional[GameConfig] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Factory Pattern
`PlayerFactory` creates players based on difficulty:

```python
@staticmethod
def create_computer_player(difficulty: str, opponent_stats: GameStats) -> ComputerPlayer:
    strategies = {'easy': RandomStrategy(), 'medium': CounterStrategy(opponent_stats)}
    return ComputerPlayer(strategy=strategies.get(difficulty))
```

---

## 3. Advanced Type Hints

### Type Annotations
Every function and method has type hints:

```python
def make_choice(self) -> Choice:
def update(self, result: GameResult, choice: Choice) -> None:
def _determine_result(choice1: Choice, choice2: Choice) -> GameResult:
```

### Optional Types
Used for values that might be None:

```python
from typing import Optional
def load_game(self) -> Optional[GameStats]:
```

### Protocols (Structural Typing)
Define interfaces without inheritance:

```python
class PlayerStrategy(Protocol):
    def make_choice(self) -> Choice:
        ...
```

---

## 4. Enums

Enhanced enumerations with methods and properties:

```python
class Choice(Enum):
    ROCK = ('r', '🪨', 'rock')
    
    def beats(self, other: Choice) -> bool:
        """Circular logic for win conditions"""
        winning_combinations = {
            Choice.ROCK: Choice.SCISSORS,
            Choice.SCISSORS: Choice.PAPER,
            Choice.PAPER: Choice.ROCK
        }
        return winning_combinations[self] == other
    
    @classmethod
    def from_input(cls, user_input: str) -> Optional[Choice]:
        """Factory method to create Choice from user input"""
```

---

## 5. Dataclasses

Automatically generates `__init__`, `__repr__`, and other methods:

```python
from dataclasses import dataclass, field

@dataclass
class GameStats:
    wins: int = 0
    losses: int = 0
    ties: int = 0
    choice_history: list[Choice] = field(default_factory=list)
```

**Key Features**:
- Default values
- `field(default_factory=list)` prevents mutable default argument issues
- Automatic equality and string representations

---

## 6. Decorators

### Function Decorators
Add functionality to existing functions:

```python
def log_game_action(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] {func.__name__} executed")
        return result
    return wrapper

@log_game_action
def play_round(self) -> GameResult:
    # Function code
```

### Decorator Factories
Create configurable decorators:

```python
def validate_input(valid_inputs: set[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # Validation logic
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

### Property Decorators
Create computed attributes:

```python
@property
def win_rate(self) -> float:
    return (self.wins / self.total_games * 100) if self.total_games > 0 else 0.0
```

---

## 7. Context Managers

Manage resources and setup/teardown operations:

```python
class GameSession:
    def __enter__(self) -> GameSession:
        self.start_time = datetime.now()
        print(f"Game Started: {self.start_time}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        print(f"Duration: {duration:.2f} seconds")
        return False

# Usage
with GameSession(player1, player2):
    # Game code
# Automatic cleanup
```

---

## 8. Magic Methods (Dunder Methods)

Special methods that customize class behavior:

```python
def __init__(self, key: str, emoji: str, name: str):
    # Constructor

def __str__(self) -> str:
    # String representation for users
    return f"{self._name.capitalize()} {self.emoji}"

def __repr__(self) -> str:
    # String representation for developers
    return f"{self.__class__.__name__}(name='{self._name}')"

def __new__(cls):
    # Object creation (used in Singleton)

def __enter__(self) -> GameSession:
    # Context manager entry

def __exit__(self, exc_type, exc_val, exc_tb):
    # Context manager exit
```

---

## 9. Advanced Data Structures

### Sets for Efficient Lookup
```python
valid_inputs = {'r', 'p', 's', 'rock', 'paper', 'scissors'}
```

### List Comprehensions
```python
'choice_history': [c.key for c in self.choice_history]
```

### Dictionaries for Mapping
```python
strategies = {
    'easy': RandomStrategy(),
    'medium': CounterStrategy(opponent_stats),
    'hard': PatternStrategy(opponent_stats)
}
```

---

## 10. File I/O and Serialization

### JSON Serialization
```python
def save_game(self, stats: GameStats) -> None:
    with open(self.save_path, 'w') as f:
        json.dump(stats.to_dict(), f, indent=2)

def load_game(self) -> Optional[GameStats]:
    with open(self.save_path, 'r') as f:
        data = json.load(f)
```

### Path Management
```python
from pathlib import Path
self.save_path = Path("game_history.json")
if self.save_path.exists():
    # Load file
```

---

## 11. Exception Handling

Graceful error management:

```python
try:
    with open(self.save_path, 'w') as f:
        json.dump(stats.to_dict(), f, indent=2)
except IOError as e:
    print(f"❌ Error saving game: {e}")
except json.JSONDecodeError as e:
    print(f"❌ Error loading game: {e}")
```

---

## 12. Functional Programming Concepts

### Higher-Order Functions
Functions that take or return functions:

```python
from functools import wraps

def decorator(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

### Lambda Functions (Implicit)
```python
most_common = max(set(history), key=history.count)
```

---

## 13. Module Organization

### Imports
```python
from __future__ import annotations  # Forward references
from abc import ABC, abstractmethod  # Abstract base classes
from dataclasses import dataclass, field  # Data classes
from enum import Enum  # Enumerations
from typing import Protocol, Optional, Callable, Any  # Type hints
from functools import wraps  # Decorator utilities
import random  # Random number generation
import json  # JSON serialization
from pathlib import Path  # File path operations
from datetime import datetime  # Date and time
```

---

## 14. Advanced String Formatting

### F-strings with Expressions
```python
print(f"Win Rate: {self.win_rate:.2f}%")
print(f"Duration: {duration:.2f} seconds")
print(f"[{timestamp}] {func.__name__} executed")
```

### Multi-line Strings
```python
return (f"\n{'='*50}\n"
        f"📊 GAME STATISTICS\n"
        f"{'='*50}\n"
        f"Total Games: {self.total_games}\n")
```

---

## 15. Static Methods and Class Methods

### Static Methods
Don't need access to instance or class:

```python
@staticmethod
def _determine_result(choice1: Choice, choice2: Choice) -> GameResult:
    if choice1 == choice2:
        return GameResult.TIE
```

### Class Methods
Factory methods that return class instances:

```python
@classmethod
def from_input(cls, user_input: str) -> Optional[Choice]:
    for choice in cls:
        if user_input.lower() in (choice.key, choice._name):
            return choice
    return None
```

---

## Key Improvements Over Original

1. **Better Code Organization**: Separated concerns into classes and modules
2. **Type Safety**: Type hints catch errors before runtime
3. **Extensibility**: Easy to add new strategies, player types, or game modes
4. **Maintainability**: Clear structure and documentation
5. **Reusability**: Components can be used in other projects
6. **Testability**: Each component can be tested independently
7. **Professional Features**: 
   - Save/load game progress
   - Multiple AI difficulties
   - Statistics tracking
   - Session management
   - Error handling

---

## Running the Game

```bash
python rps_advanced.py
```

## Testing Individual Components

```python
# Test Enum
from rps_advanced import Choice
rock = Choice.ROCK
scissors = Choice.SCISSORS
print(rock.beats(scissors))  # True

# Test Strategy
from rps_advanced import RandomStrategy
strategy = RandomStrategy()
choice = strategy.make_choice()
print(choice)
```

---

This implementation demonstrates production-quality Python code with enterprise-level design patterns and best practices!
