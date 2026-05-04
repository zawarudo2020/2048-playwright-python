from playwright.sync_api import Page, expect
import re
from typing import Literal

Direction = Literal["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight"]

class Game2048Page:
    def __init__(self, page: Page):
        self.page = page

        # Locators
        self.grid = page.locator(".tile-container")
        self.score = page.locator(".score-container")
        self.game_over = page.locator("text=Game over!").or_(page.locator(".game-over"))
        self.new_game_btn = page.get_by_role("button", name=re.compile("New Game|Try again", re.I))

        # 新增：關閉彈窗的 locator（你可以之後再優化）
        self.close_popup_btn = page.get_by_role("banner").get_by_role("button").filter(
            has_text=re.compile(r"^$")
        )

    def navigate(self):
        """進入遊戲頁面並處理前置事項"""
        self.page.goto("https://play2048.co/", wait_until="domcontentloaded")
        
        # 改用較穩定的等待方式，避免 networkidle 卡住
        self.page.wait_for_timeout(1500)   # 給頁面一點時間載入

        # 關閉可能的彈窗（你之前提供的定位器）
        self.close_initial_popup()

        # 等待遊戲主格子出現（這是最重要的判斷條件）
        try:
            expect(self.grid).to_be_visible(timeout=10000)
            print("✓ 遊戲主畫面已載入")
        except Exception as e:
            print(f"⚠ 等待 grid 超時: {e}")
            # 如果還是失敗，可以再多等一點
            self.page.wait_for_timeout(3000)

        self.page.wait_for_timeout(800)

    def close_initial_popup(self):
        """關閉進入頁面後的彈窗（Cookie、廣告、Consent 等）"""
        try:
            # 等待彈窗按鈕出現，最多等 5 秒
            self.close_popup_btn.wait_for(state="visible", timeout=5000)
            self.close_popup_btn.click()
            print("✓ 已關閉初始彈窗")
            self.page.wait_for_timeout(600)
        except Exception:
            # 如果沒有找到彈窗，就直接跳過（避免測試失敗）
            print("ℹ 沒有偵測到彈窗，或已自動關閉")
            pass

    # 以下方法保持不變...
    def press_key(self, direction: Direction):
        self.page.keyboard.press(direction)
        self.page.wait_for_timeout(180)

    def get_current_score(self) -> int:
        """取得目前分數 - 加強版"""
        try:
            # 方法1: 找有 "Score" 文字的區塊
            score_area = self.score_text
            if score_area.count() > 0:
                text = score_area.text_content(timeout=2000) or ""
            else:
                # 方法2: 直接找 score container
                text = self.score_container.text_content(timeout=2000) or ""

            # 提取數字
            numbers = re.sub(r'[^0-9]', '', text)
            score = int(numbers) if numbers else 0
            return score
        except Exception as e:
            print(f"⚠ 取得分數失敗: {e}")
            # 方法3: 最後保險 - 找頁面上所有可能的數字
            try:
                all_numbers = self.page.locator("text=\\d+").all_text_contents()
                for t in all_numbers:
                    cleaned = re.sub(r'[^0-9]', '', t)
                    if cleaned and int(cleaned) < 1000000:   # 避免抓到超大數字
                        return int(cleaned)
            except:
                pass
            return 0

    def is_game_over(self) -> bool:
        return self.game_over.is_visible(timeout=1000)

    def start_new_game(self):
        if self.is_game_over():
            self.new_game_btn.click()
            self.page.wait_for_timeout(400)
