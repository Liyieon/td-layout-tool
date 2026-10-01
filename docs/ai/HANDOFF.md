# HANDOFF — layout_tool

最後更新：2026-10-01 · 機器：LAPTOP-Q2P9AM5O · 每次收工整份覆寫，不要附加。

## 做完了嗎？
功能面「階段一」完成並經使用者實機確認：
- 選取／拖曳／8 控制點縮放／框選／方向鍵微調／undo
- 對齊、分佈、吸附輔助線；8 種頁面比例（預設 1920×1080）；畫板遮罩（超出頁面不顯示但可移動）
- 文字：預設 Inter，5 種角色自動配字重；字型／字重選單、字距、行距、對齊
- 形狀：矩形（預設框線，可切填色）、圓形
- 圖片：OS 拖放、選檔、拖 TOP 到畫布或 Images 頁、背景 TOP 輸入
- 網格 + 種子式隨機排版（Locked 不動、手放物件保留並換格、生成矩形為框線）
- 色盤、中英雙語參數說明（按住 Alt 看）
- PNG 匯出（含像素檢查重抓）、JSON 存讀檔、`out_top` 即時輸出
- 最近一個修正（2026-10-01）：拖進「生成的灰色影像區塊」的圖，re-roll 後消失。原因是區塊仍標 `Generated=1` 被重生；現在填圖即清除該旗標。
- 工具內 0 錯誤 0 警告。

## 在哪裡
- 元件：`/project1/layout_tool`（TD 內），可攜版 `layout_tool.tox`（本 repo 根目錄，**公開 repo 只放這個與文件**）。
- 最新專案檔：`Editorial_Tool.24.toe`（本機，未進 repo）；舊版在 `Backup/`。
- 詳細契約：TD 內 `agents_md` DAT；摘要在 `CLAUDE.md`。
- extension 原始碼只存在 `.tox` 裡（`ext_layouttool` DAT）。**下次連上 TD 時，把它匯出成 `src/ext_layouttool.py` 與 `src/agents_md.md` 放進 repo**，方便 diff／審閱。

## 不能碰
- `/project1/Dragon_skin_Particle`（使用者自己的元件）。
- 使用者目前的版面（seed 122）：測試後要還原，測試物件要刪掉。
- 不要在公開 repo 放 `.toe`、`Backup/`、`assets/images/`、`export/`、`layouts/`、螢幕錄影。

## 需要人決定／確認
- 真滑鼠確認：Images 頁拖 TOP、Alt+hover 的中英說明、色盤拖曳。
- 授權條款：repo 目前沒有 LICENSE（預設保留所有權利）；想開放別人使用就要選一個。
- 可選下一階段：旋轉（需走 TOP 渲染路線）、圖層面板、畫布上直接編輯文字、縮放時也吸附、per-pair kerning、多畫板。
- 未決：是否刪除 TD 自動產生、沒用到的 `grid_top_compute` / `grid_top_info` DAT（刪除前要先問）。
