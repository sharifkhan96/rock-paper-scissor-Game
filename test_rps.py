"""
Unit Tests for Advanced Rock-Paper-Scissors Game
Demonstrates: unittest, mocking, fixtures, parametrized tests, test organization
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from rps_advanced import (
    Choice, GameResult, GameStats, HumanPlayer, ComputerPlayer,
    RandomStrategy, CounterStrategy, GameConfig, RockPaperScissorsGame,
    PlayerFactory
)


class TestChoice(unittest.TestCase):
    """Test suite for Choice enum."""
    
    def test_choice_beats_logic(self):
        """Test that win conditions work correctly."""
        self.assertTrue(Choice.ROCK.beats(Choice.SCISSORS))
        self.assertTrue(Choice.SCISSORS.beats(Choice.PAPER))
        self.assertTrue(Choice.PAPER.beats(Choice.ROCK))
        
        self.assertFalse(Choice.ROCK.beats(Choice.PAPER))
        self.assertFalse(Choice.SCISSORS.beats(Choice.ROCK))
        self.assertFalse(Choice.PAPER.beats(Choice.SCISSORS))
    
    def test_choice_from_input(self):
        """Test factory method for creating choices."""
        self.assertEqual(Choice.from_input('r'), Choice.ROCK)
        self.assertEqual(Choice.from_input('rock'), Choice.ROCK)
        self.assertEqual(Choice.from_input('ROCK'), Choice.ROCK)
        
        self.assertEqual(Choice.from_input('p'), Choice.PAPER)
        self.assertEqual(Choice.from_input('s'), Choice.SCISSORS)
        
        self.assertIsNone(Choice.from_input('invalid'))
        self.assertIsNone(Choice.from_input(''))
    
    def test_choice_string_representation(self):
        """Test string representation of choices."""
        self.assertIn('Rock', str(Choice.ROCK))
        self.assertIn('🪨', str(Choice.ROCK))


class TestGameStats(unittest.TestCase):
    """Test suite for GameStats dataclass."""
    
    def setUp(self):
        """Set up test fixture."""
        self.stats = GameStats()
    
    def test_initial_stats(self):
        """Test initial state of statistics."""
        self.assertEqual(self.stats.wins, 0)
        self.assertEqual(self.stats.losses, 0)
        self.assertEqual(self.stats.ties, 0)
        self.assertEqual(self.stats.total_games, 0)
        self.assertEqual(self.stats.win_rate, 0.0)
    
    def test_update_stats_win(self):
        """Test updating stats with a win."""
        self.stats.update(GameResult.WIN, Choice.ROCK)
        
        self.assertEqual(self.stats.wins, 1)
        self.assertEqual(self.stats.total_games, 1)
        self.assertEqual(self.stats.win_rate, 100.0)
    
    def test_update_stats_loss(self):
        """Test updating stats with a loss."""
        self.stats.update(GameResult.LOSS, Choice.PAPER)
        
        self.assertEqual(self.stats.losses, 1)
        self.assertEqual(self.stats.total_games, 1)
        self.assertEqual(self.stats.win_rate, 0.0)
    
    def test_update_stats_tie(self):
        """Test updating stats with a tie."""
        self.stats.update(GameResult.TIE, Choice.SCISSORS)
        
        self.assertEqual(self.stats.ties, 1)
        self.assertEqual(self.stats.total_games, 1)
    
    def test_win_rate_calculation(self):
        """Test win rate calculation with mixed results."""
        self.stats.update(GameResult.WIN, Choice.ROCK)
        self.stats.update(GameResult.WIN, Choice.PAPER)
        self.stats.update(GameResult.LOSS, Choice.SCISSORS)
        self.stats.update(GameResult.TIE, Choice.ROCK)
        
        # 2 wins out of 4 games = 50%
        self.assertEqual(self.stats.win_rate, 50.0)
    
    def test_choice_history(self):
        """Test that choice history is tracked."""
        choices = [Choice.ROCK, Choice.PAPER, Choice.SCISSORS]
        
        for choice in choices:
            self.stats.update(GameResult.WIN, choice)
        
        self.assertEqual(len(self.stats.choice_history), 3)
        self.assertEqual(self.stats.choice_history, choices)
    
    def test_to_dict_serialization(self):
        """Test conversion to dictionary."""
        self.stats.update(GameResult.WIN, Choice.ROCK)
        
        data = self.stats.to_dict()
        
        self.assertIn('wins', data)
        self.assertIn('total_games', data)
        self.assertIn('win_rate', data)
        self.assertEqual(data['wins'], 1)


class TestStrategies(unittest.TestCase):
    """Test suite for AI strategies."""
    
    def test_random_strategy(self):
        """Test that random strategy returns valid choices."""
        strategy = RandomStrategy()
        
        for _ in range(10):
            choice = strategy.make_choice()
            self.assertIn(choice, list(Choice))
    
    def test_counter_strategy_empty_history(self):
        """Test counter strategy with no history."""
        stats = GameStats()
        strategy = CounterStrategy(stats)
        
        choice = strategy.make_choice()
        self.assertIn(choice, list(Choice))
    
    def test_counter_strategy_with_history(self):
        """Test counter strategy counters most common choice."""
        stats = GameStats()
        
        # Player uses ROCK three times
        for _ in range(3):
            stats.update(GameResult.LOSS, Choice.ROCK)
        
        strategy = CounterStrategy(stats)
        choice = strategy.make_choice()
        
        # Strategy should choose PAPER to beat ROCK
        self.assertEqual(choice, Choice.PAPER)


class TestPlayers(unittest.TestCase):
    """Test suite for player classes."""
    
    def test_computer_player_creation(self):
        """Test creating a computer player."""
        player = ComputerPlayer("TestBot")
        
        self.assertEqual(player.name, "TestBot")
        self.assertIsInstance(player.stats, GameStats)
    
    def test_computer_player_strategy_change(self):
        """Test changing computer player strategy."""
        player = ComputerPlayer("TestBot")
        new_strategy = RandomStrategy()
        
        player.set_strategy(new_strategy)
        # If this doesn't raise an error, strategy was set
        choice = player.make_choice()
        self.assertIn(choice, list(Choice))
    
    @patch('builtins.input', return_value='r')
    def test_human_player_choice(self, mock_input):
        """Test human player input with mocking."""
        player = HumanPlayer("TestHuman")
        choice = player.make_choice()
        
        self.assertEqual(choice, Choice.ROCK)
        mock_input.assert_called_once()
    
    @patch('builtins.input', side_effect=['invalid', 'r'])
    def test_human_player_invalid_then_valid(self, mock_input):
        """Test human player with invalid then valid input."""
        player = HumanPlayer("TestHuman")
        choice = player.make_choice()
        
        self.assertEqual(choice, Choice.ROCK)
        self.assertEqual(mock_input.call_count, 2)


class TestPlayerFactory(unittest.TestCase):
    """Test suite for PlayerFactory."""
    
    def test_create_easy_difficulty(self):
        """Test creating easy difficulty AI."""
        stats = GameStats()
        player = PlayerFactory.create_computer_player('easy', stats)
        
        self.assertIsInstance(player, ComputerPlayer)
        self.assertIsInstance(player._strategy, RandomStrategy)
    
    def test_create_medium_difficulty(self):
        """Test creating medium difficulty AI."""
        stats = GameStats()
        player = PlayerFactory.create_computer_player('medium', stats)
        
        self.assertIsInstance(player, ComputerPlayer)
        self.assertIsInstance(player._strategy, CounterStrategy)


class TestGameConfig(unittest.TestCase):
    """Test suite for GameConfig singleton."""
    
    def test_singleton_pattern(self):
        """Test that only one instance exists."""
        config1 = GameConfig()
        config2 = GameConfig()
        
        self.assertIs(config1, config2)
    
    def test_config_attributes(self):
        """Test configuration attributes."""
        config = GameConfig()
        
        self.assertEqual(config.difficulty, "medium")
        self.assertTrue(config.enable_emoji)


class TestGame(unittest.TestCase):
    """Test suite for main game logic."""
    
    def setUp(self):
        """Set up test fixture."""
        self.human = HumanPlayer("TestPlayer")
        self.computer = ComputerPlayer("TestBot")
        self.game = RockPaperScissorsGame(self.human, self.computer)
    
    def test_determine_result_tie(self):
        """Test game result determination for tie."""
        result = self.game._determine_result(Choice.ROCK, Choice.ROCK)
        self.assertEqual(result, GameResult.TIE)
    
    def test_determine_result_win(self):
        """Test game result determination for win."""
        result = self.game._determine_result(Choice.ROCK, Choice.SCISSORS)
        self.assertEqual(result, GameResult.WIN)
    
    def test_determine_result_loss(self):
        """Test game result determination for loss."""
        result = self.game._determine_result(Choice.ROCK, Choice.PAPER)
        self.assertEqual(result, GameResult.LOSS)
    
    @patch('builtins.input', return_value='r')
    def test_play_round_updates_stats(self, mock_input):
        """Test that playing a round updates statistics."""
        initial_games = self.human.stats.total_games
        
        self.game.play_round()
        
        self.assertEqual(self.human.stats.total_games, initial_games + 1)


# ==================== PARAMETRIZED TESTS ====================
class TestChoiceBeatsParametrized(unittest.TestCase):
    """Parametrized tests for choice win conditions."""
    
    def test_all_winning_combinations(self):
        """Test all possible winning combinations."""
        winning_combinations = [
            (Choice.ROCK, Choice.SCISSORS, True),
            (Choice.SCISSORS, Choice.PAPER, True),
            (Choice.PAPER, Choice.ROCK, True),
            (Choice.ROCK, Choice.PAPER, False),
            (Choice.SCISSORS, Choice.ROCK, False),
            (Choice.PAPER, Choice.SCISSORS, False),
            (Choice.ROCK, Choice.ROCK, False),
            (Choice.PAPER, Choice.PAPER, False),
            (Choice.SCISSORS, Choice.SCISSORS, False),
        ]
        
        for choice1, choice2, expected in winning_combinations:
            with self.subTest(choice1=choice1, choice2=choice2):
                self.assertEqual(choice1.beats(choice2), expected)


# ==================== INTEGRATION TESTS ====================
class TestGameIntegration(unittest.TestCase):
    """Integration tests for full game flow."""
    
    @patch('builtins.input', side_effect=['r', 'n'])
    def test_full_game_session(self, mock_input):
        """Test a complete game session."""
        human = HumanPlayer("Player")
        computer = ComputerPlayer("AI")
        game = RockPaperScissorsGame(human, computer)
        
        # This would normally run the full game loop
        # For testing, we'll just test a single round
        result = game.play_round()
        
        self.assertIn(result, [GameResult.WIN, GameResult.LOSS, GameResult.TIE])
        self.assertGreater(human.stats.total_games, 0)


# ==================== TEST RUNNER ====================
def run_tests():
    """Run all tests with verbose output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestChoice))
    suite.addTests(loader.loadTestsFromTestCase(TestGameStats))
    suite.addTests(loader.loadTestsFromTestCase(TestStrategies))
    suite.addTests(loader.loadTestsFromTestCase(TestPlayers))
    suite.addTests(loader.loadTestsFromTestCase(TestPlayerFactory))
    suite.addTests(loader.loadTestsFromTestCase(TestGameConfig))
    suite.addTests(loader.loadTestsFromTestCase(TestGame))
    suite.addTests(loader.loadTestsFromTestCase(TestChoiceBeatsParametrized))
    suite.addTests(loader.loadTestsFromTestCase(TestGameIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
