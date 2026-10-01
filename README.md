# TD Layout Tool · TouchDesigner 排版工具

在 TouchDesigner 裡做的 Illustrator 風格排版元件（`layout_tool.tox`）：選取、拖曳、縮放、對齊／分佈／吸附、文字排版細節、圖片與 TOP 置入、網格式隨機排版、PNG 匯出與即時輸出 TOP。

An Illustrator-style layout / typography COMP for TouchDesigner, built entirely from panel COMPs and one Python extension.

## 使用 · Usage
1. 用 TouchDesigner **2025.33070**（或更新）開新專案，把 `layout_tool.tox` 拖進網路編輯器。
2. 點選物件後出現參數面板；拖曳移動、8 個控制點縮放、Shift 加選或框選。
3. 圖片：從檔案總管拖進畫布，或把任何 TOP 拖到畫布上；背景可從 `bg_in` 輸入。
4. 輸出：`out_top` 是即時 TOP；也可匯出 PNG、存讀 JSON。
5. 每個自訂參數都有中英文說明——**按住 Alt，滑鼠停在參數名稱上**即可顯示。

## 功能 · Features
| | |
|---|---|
| 頁面 | 預設 1920×1080，8 種比例（2:1、16:9、4:3、5:4、4:5、3:4、9:16、1:2）；畫板外的內容不顯示但仍可移動 |
| 操作 | 選取、加選、框選、拖曳、8 點縮放、方向鍵微調、複製、刪除、圖層順序、完整 undo |
| 版面 | 6 種對齊（選取範圍或頁面）、等距分佈、吸附到物件／頁面／網格並顯示輔助線 |
| 文字 | 預設字型 Inter，標題／副標／內文自動配字重；字型、字重、字級、字距、行距、對齊、內距、陰影 |
| 形狀 | 矩形（框線或填色）、圓形；框線顏色／粗細／透明度；色盤取色 |
| 圖片 | 檔案拖放、選檔、拖 TOP；自動複製進專案；Contain／Cover／Stretch |
| 生成 | 網格 + 種子的隨機排版；鎖定的物件不動 |
| 輸出 | PNG 匯出（含像素檢查）、`out_top` 即時輸出、JSON 存讀檔 |

## 限制 · Limitations
- 非商業版授權的 TOP 上限為 1280 px。
- 沒有旋轉（panel COMP 不能旋轉）、沒有逐字 kerning（只有整段字距）。
- 預設字型 Inter 需自行安裝在系統上。

## 開發筆記 · Dev notes
給 AI 代理與接手者的契約與陷阱整理在 [`CLAUDE.md`](CLAUDE.md)，目前進度在 [`docs/ai/HANDOFF.md`](docs/ai/HANDOFF.md)。

> 尚未指定授權條款（LICENSE）；預設保留所有權利。
