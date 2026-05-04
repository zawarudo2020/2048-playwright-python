# 2048 Game Playwright 自動化測試
使用playwright自動化測試網路遊戲play2048.co
使用 **Playwright + Page Object Model (POM)** 開發的 2048 遊戲自動化測試專案。


##  專案特色

- 使用 **Page Object Model** 設計模式（乾淨、可維護）
- 完整的測試案例（載入、移動、分數計算、重新開始遊戲等）
- 處理遊戲彈窗（Popup）
- 穩健的 Locator 策略
- 支持 headless 與 headed 模式
- 使用 pytest 框架

##  技術棧

- **Python 3.10+**
- **Playwright**（同步 API）
- **pytest**
- **Page Object Model**

##  安裝步驟

1. **複製專案**

```bash
cd 2048-playwright-python
python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
playwright install chromium

# 顯示畫面（方便除錯）
pytest -v --headed

# 安靜模式（無頭執行）
pytest -v
# 執行單一測試檔案
pytest tests/test_2048_game.py -v --headed

# 執行單一測試案例
pytest tests/test_2048_game.py::test_2048_game_loads_successfully -v --headed
```

2048-playwright-python/
├── pages/
│   └── game_2048_page.py 
├── tests/
│   └── test_2048_game.py
├── pytest.ini
├── requirements.txt
└── README.md
