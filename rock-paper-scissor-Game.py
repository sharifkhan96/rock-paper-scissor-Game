"""
Advanced Rock-Paper-Scissors Game
Demonstrates: OOP, Design Patterns, Type Hints, Enums, Abstract Classes,
Context Managers, Decorators, Property Decorators, and more.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Protocol, Optional, Callable, Any
from functools import wraps
import random
import json
from pathlib import Path
from datetime import datetime


# ==================== ENUMS ====================
class Choice(Enum):
    """Enum representing game choices with enhanced metadata."""
    ROCK = ('r', '🪨', 'rock')
    PAPER = ('p', '📃', 'paper')
    SCISSORS = ('s', '✂️', 'scissors')
    
    def __init__(self, key: str, emoji: str, name: str):
        self.key = key
        self.emoji = emoji
        self._name = name
    
    def beats(self, other: Choice) -> bool:
        """Determine if this choice beats another using circular logic."""
        winning_combinations = {
            Choice.ROCK: Choice.SCISSORS,
            Choice.SCISSORS: Choice.PAPER,
            Choice.PAPER: Choice.ROCK
        }
        return winning_combinations[self] == other
    
    @classmethod
    def from_input(cls, user_input: str) -> Optional[Choice]:
        """Factory method to create Choice from user input."""
        for choice in cls:
            if user_input.lower() in (choice.key, choice._name):
                return choice
        return None
    
    def __str__(self) -> str:
        return f"{self._name.capitalize()} {self.emoji}"


class GameResult(Enum):
    """Enum representing possible game outcomes."""
    WIN = "win"
    LOSS = "loss"
    TIE = "tie"


# ==================== PROTOCOLS ====================
class PlayerStrategy(Protocol):
    """Protocol defining the interface for player strategies."""
    def make_choice(self) -> Choice:
        """Make a choice for the current round."""
        ...


# ==================== DECORATORS ====================
def log_game_action(func: Callable) -> Callable:
    """Decorator to log game actions with timestamps."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = func(*args, **kwargs)
        print(f"[{timestamp}] {func.__name__} executed")
        return result
    return wrapper


def validate_input(valid_inputs: set[str]) -> Callable:
    """Decorator factory for input validation."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if 'user_input' in kwargs:
                inp = kwargs['user_input']
                if inp.lower() not in valid_inputs:
                    raise ValueError(f"Invalid input. Expected one of: {valid_inputs}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ==================== DATA CLASSES ====================
@dataclass
class GameStats:
    """Dataclass to track game statistics."""
    wins: int = 0
    losses: int = 0
    ties: int = 0
    total_games: int = 0
    choice_history: list[Choice] = field(default_factory=list)
    
    @property
    def win_rate(self) -> float:
        """Calculate win percentage."""
        return (self.wins / self.total_games * 100) if self.total_games > 0 else 0.0
    
    def update(self, result: GameResult, choice: Choice) -> None:
        """Update statistics based on game result."""
        self.total_games += 1
        self.choice_history.append(choice)
        
        if result == GameResult.WIN:
            self.wins += 1
        elif result == GameResult.LOSS:
            self.losses += 1
        else:
            self.ties += 1
    
    def to_dict(self) -> dict:
        """Convert stats to dictionary for serialization."""
        return {
            'wins': self.wins,
            'losses': self.losses,
            'ties': self.ties,
            'total_games': self.total_games,
            'win_rate': self.win_rate,
            'choice_history': [c.key for c in self.choice_history]
        }
    
    def __str__(self) -> str:
        return (f"\n{'='*50}\n"
                f"📊 GAME STATISTICS\n"
                f"{'='*50}\n"
                f"Total Games: {self.total_games}\n"
                f"Wins: {self.wins} ✅\n"
                f"Losses: {self.losses} ❌\n"
                f"Ties: {self.ties} 🤝\n"
                f"Win Rate: {self.win_rate:.2f}%\n"
                f"{'='*50}")


# ==================== ABSTRACT BASE CLASSES ====================
class Player(ABC):
    """Abstract base class for all player types."""
    
    def __init__(self, name: str):
        self._name = name
        self._stats = GameStats()
    
    @property
    def name(self) -> str:
        """Get player name."""
        return self._name
    
    @property
    def stats(self) -> GameStats:
        """Get player statistics."""
        return self._stats
    
    @abstractmethod
    def make_choice(self) -> Choice:
        """Abstract method for making a choice."""
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self._name}')"


# ==================== CONCRETE PLAYER CLASSES ====================
class HumanPlayer(Player):
    """Human player implementation."""
    
    def make_choice(self) -> Choice:
        """Get choice from human input."""
        while True:
            user_input = input(f"\n{self.name}, choose (r/p/s) or type full name: ").strip()
            choice = Choice.from_input(user_input)
            
            if choice:
                return choice
            print("❌ Invalid choice! Try again.")


class ComputerPlayer(Player):
    """Computer player with various AI strategies."""
    
    def __init__(self, name: str, strategy: Optional[PlayerStrategy] = None):
        super().__init__(name)
        self._strategy = strategy or RandomStrategy()
    
    def make_choice(self) -> Choice:
        """Make choice using assigned strategy."""
        return self._strategy.make_choice()
    
    def set_strategy(self, strategy: PlayerStrategy) -> None:
        """Change the AI strategy (Strategy Pattern)."""
        self._strategy = strategy


# ==================== STRATEGY PATTERN IMPLEMENTATIONS ====================
class RandomStrategy:
    """Random choice strategy."""
    def make_choice(self) -> Choice:
        return random.choice(list(Choice))


class CounterStrategy:
    """Strategy that tries to counter player's most frequent choice."""
    def __init__(self, opponent_stats: GameStats):
        self.opponent_stats = opponent_stats
    
    def make_choice(self) -> Choice:
        if not self.opponent_stats.choice_history:
            return random.choice(list(Choice))
        
        # Find most common choice
        most_common = max(set(self.opponent_stats.choice_history),
                         key=self.opponent_stats.choice_history.count)
        
        # Choose what beats their most common choice
        for choice in Choice:
            if choice.beats(most_common):
                return choice
        
        return random.choice(list(Choice))


class PatternStrategy:
    """Advanced strategy that looks for patterns."""
    def __init__(self, opponent_stats: GameStats):
        self.opponent_stats = opponent_stats
    
    def make_choice(self) -> Choice:
        history = self.opponent_stats.choice_history
        
        if len(history) < 3:
            return random.choice(list(Choice))
        
        # Check if opponent is alternating or repeating
        if history[-1] == history[-2]:
            # Likely to repeat again
            predicted = history[-1]
        else:
            # Might continue pattern
            predicted = random.choice(list(Choice))
        
        # Counter the prediction
        for choice in Choice:
            if choice.beats(predicted):
                return choice
        
        return random.choice(list(Choice))


# ==================== SINGLETON PATTERN ====================
class GameConfig:
    """Singleton configuration manager."""
    _instance: Optional[GameConfig] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        self._initialized = True
        self.save_path = Path("game_history.json")
        self.difficulty = "medium"
        self.enable_emoji = True
    
    def save_game(self, stats: GameStats) -> None:
        """Save game statistics to file."""
        try:
            with open(self.save_path, 'w') as f:
                json.dump(stats.to_dict(), f, indent=2)
            print(f"💾 Game saved to {self.save_path}")
        except IOError as e:
            print(f"❌ Error saving game: {e}")
    
    def load_game(self) -> Optional[GameStats]:
        """Load game statistics from file."""
        try:
            if self.save_path.exists():
                with open(self.save_path, 'r') as f:
                    data = json.load(f)
                stats = GameStats(
                    wins=data['wins'],
                    losses=data['losses'],
                    ties=data['ties'],
                    total_games=data['total_games']
                )
                print(f"📂 Game loaded from {self.save_path}")
                return stats
        except (IOError, json.JSONDecodeError) as e:
            print(f"❌ Error loading game: {e}")
        return None


# ==================== CONTEXT MANAGER ====================
class GameSession:
    """Context manager for game sessions."""
    
    def __init__(self, player1: Player, player2: Player):
        self.player1 = player1
        self.player2 = player2
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def __enter__(self) -> GameSession:
        self.start_time = datetime.now()
        print(f"\n🎮 Game Session Started: {self.start_time.strftime('%H:%M:%S')}")
        print(f"👤 {self.player1.name} vs 🤖 {self.player2.name}\n")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        print(f"\n⏱️  Game Session Ended: {self.end_time.strftime('%H:%M:%S')}")
        print(f"Duration: {duration:.2f} seconds")
        
        if exc_type is not None:
            print(f"❌ Session ended with error: {exc_val}")
        return False


# ==================== MAIN GAME CLASS ====================
class RockPaperScissorsGame:
    """Main game controller implementing game logic."""
    
    def __init__(self, human_player: HumanPlayer, computer_player: ComputerPlayer):
        self.human = human_player
        self.computer = computer_player
        self.config = GameConfig()
    
    @log_game_action
    def play_round(self) -> GameResult:
        """Play a single round of the game."""
        print("\n" + "="*50)
        
        # Get choices
        human_choice = self.human.make_choice()
        computer_choice = self.computer.make_choice()
        
        # Display choices
        print(f"\n{self.human.name} chose: {human_choice}")
        print(f"{self.computer.name} chose: {computer_choice}")
        
        # Determine winner
        result = self._determine_result(human_choice, computer_choice)
        
        # Update statistics
        self.human.stats.update(result, human_choice)
        
        # Map result for computer (inverse of human)
        computer_result = {
            GameResult.WIN: GameResult.LOSS,
            GameResult.LOSS: GameResult.WIN,
            GameResult.TIE: GameResult.TIE
        }[result]
        self.computer.stats.update(computer_result, computer_choice)
        
        # Display result
        self._display_result(result)
        
        return result
    
    @staticmethod
    def _determine_result(choice1: Choice, choice2: Choice) -> GameResult:
        """Determine the game result."""
        if choice1 == choice2:
            return GameResult.TIE
        elif choice1.beats(choice2):
            return GameResult.WIN
        else:
            return GameResult.LOSS
    
    @staticmethod
    def _display_result(result: GameResult) -> None:
        """Display the round result with formatting."""
        messages = {
            GameResult.WIN: "🎉 Congratulations! You win! 🎉",
            GameResult.LOSS: "😔 Sorry, you lost this round. Better luck next time!",
            GameResult.TIE: "🤝 It's a tie! Great minds think alike!"
        }
        print(f"\n{messages[result]}")
    
    def play(self) -> None:
        """Main game loop."""
        print("🎮 Welcome to Advanced Rock-Paper-Scissors! 🎮")
        print("="*50)
        
        with GameSession(self.human, self.computer):
            while True:
                self.play_round()
                
                # Ask to continue
                continue_game = input("\n▶️  Play another round? (y/n): ").strip().lower()
                if continue_game != 'y':
                    break
        
        # Display final statistics
        print(self.human.stats)
        
        # Save game
        save_choice = input("\n💾 Save game statistics? (y/n): ").strip().lower()
        if save_choice == 'y':
            self.config.save_game(self.human.stats)


# ==================== FACTORY PATTERN ====================
class PlayerFactory:
    """Factory for creating different types of players."""
    
    @staticmethod
    def create_computer_player(difficulty: str, opponent_stats: GameStats) -> ComputerPlayer:
        """Create computer player with difficulty-based strategy."""
        strategies = {
            'easy': RandomStrategy(),
            'medium': CounterStrategy(opponent_stats),
            'hard': PatternStrategy(opponent_stats)
        }
        
        strategy = strategies.get(difficulty.lower(), RandomStrategy())
        return ComputerPlayer(name="AI Opponent", strategy=strategy)


# ==================== MAIN ENTRY POINT ====================
def main() -> None:
    """Main entry point for the game."""
    # Get player name
    player_name = input("Enter your name: ").strip() or "Player"
    
    # Create human player
    human_player = HumanPlayer(name=player_name)
    
    # Select difficulty
    print("\nSelect difficulty:")
    print("1. Easy (Random)")
    print("2. Medium (Counter Strategy)")
    print("3. Hard (Pattern Recognition)")
    
    difficulty_map = {'1': 'easy', '2': 'medium', '3': 'hard'}
    difficulty_choice = input("Choose (1/2/3): ").strip()
    difficulty = difficulty_map.get(difficulty_choice, 'medium')
    
    # Create computer player
    computer_player = PlayerFactory.create_computer_player(difficulty, human_player.stats)
    
    # Start game
    game = RockPaperScissorsGame(human_player, computer_player)
    game.play()
    
    print("\n👋 Thanks for playing! Goodbye!")


if __name__ == "__main__":
    main()
