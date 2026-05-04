import pytest
from pages.game_2048_page import Game2048Page

@pytest.fixture
def game_page(page):
    game = Game2048Page(page)
    game.navigate()

    return game


def test_2048_game_loads_successfully(game_page):
    """測試遊戲是否正常載入"""
    assert game_page.get_current_score() >= 0
    print(f"✓ 遊戲載入成功，目前分數: {game_page.get_current_score()}")


def test_score_increases_after_moving(game_page):
    """測試移動後分數應該增加或維持"""
    initial_score = game_page.get_current_score()

    # 隨機移動 25 步
    directions = ["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]
    import random

    for _ in range(25):
        if game_page.is_game_over():
            break
        direction = random.choice(directions)
        game_page.press_key(direction)

    final_score = game_page.get_current_score()
    assert final_score >= initial_score, f"分數應該不會減少！初始 {initial_score} → 現在 {final_score}"

    print(f"✓ 移動後分數從 {initial_score} 變成 {final_score}")


def test_can_start_new_game(game_page):
    """測試能否重新開始遊戲"""
    # 先玩幾步
    for _ in range(15):
        game_page.press_key("ArrowRight")

    # 點擊 New Game
    game_page.page.get_by_text("New Game").click()
    game_page.page.wait_for_timeout(500)

    new_score = game_page.get_current_score()
    assert new_score == 0 or new_score < 20, "新遊戲開始後分數應接近 0"

    print("✓ 可以成功重新開始新遊戲")
