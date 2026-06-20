import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GAME_DIR = PROJECT_ROOT / "game"
sys.path.insert(0, str(GAME_DIR))

from settings import BOSS_SCORE_STEP, HEIGHT, WIDTH
from state import reset_game


class ResetGameTest(unittest.TestCase):
    def test_reset_game_creates_initial_player_state(self):
        game = reset_game()

        self.assertEqual(game["ship_x"], WIDTH // 2)
        self.assertEqual(game["ship_y"], HEIGHT // 2)
        self.assertEqual(game["player_life"], 3)
        self.assertFalse(game["game_over"])

    def test_reset_game_creates_empty_entity_lists(self):
        game = reset_game()

        self.assertEqual(game["bullets"], [])
        self.assertEqual(game["enemies"], [])
        self.assertEqual(game["powerups"], [])
        self.assertEqual(game["explosions"], [])

    def test_reset_game_initializes_score_progression(self):
        game = reset_game()

        self.assertEqual(game["score"], 0)
        self.assertEqual(game["next_boss_score"], BOSS_SCORE_STEP)
        self.assertEqual(game["boss_level"], 0)


if __name__ == "__main__":
    unittest.main()
