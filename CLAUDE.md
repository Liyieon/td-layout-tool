# CLAUDE.md — layout_tool（TouchDesigner 排版工具）

穩定慣例與契約。進行中狀態寫在 `docs/ai/HANDOFF.md`，不要寫這裡。
TD 內 `/project1/layout_tool/agents_md` DAT 是同一份契約的詳細版（隨 .tox 走）；兩邊衝突時以 DAT 為準，並回頭修這份。

## 環境
- TouchDesigner 2025.33070，**Non-Commercial 授權：TOP 上限 1280px**（大圖、匯出、大圓形會等比縮）。
- 透過 twozero MCP 操作 live TD：先 `td_list_instances`，用檔名 **stem** 比對專案（`Editorial_Tool.N.toe` 的 N 會一直增加）。首次動作前讀 `td_get_hints('bootstrap')`。
- 元件 `/project1/layout_tool`；可攜版 `layout_tool.tox`（本資料夾）。
- 使用者語言：繁體中文。里程碑時要給功能總覽。

## 網路結構（`/project1/layout_tool`，parentshortcut `ltool`）
- `ext_layouttool` — 主 extension（~1800 行），所有邏輯都在這裡。`agents_md` — 詳細契約 DAT。
- `control_bar`（上）+ `body_row`（`tools_strip` 左工具列 + `canvas_area`）。
- `canvas_area/artboard` — 所有物件（panel COMP）；`bg_view`（layer -2，背景 TOP）、`grid_under`（layer -1），物件 layer 1..N。
- `canvas_area/overlay`（選取框、8 控制點、吸附線、框選）、`inspector_popup`（分區參數面板，r_* 列）、`color_picker`（色盤）。
- `canvas_area/canvas_input`（panelexec，唯一滑鼠入口）、`canvas_dragdrop`（拖放 callbacks）。
- `ui_icons/icon_sheet`（SDF glslTOP，8x6，42 icons）+ `ic_*` cropTOPs。
- `bg_in`（inTOP，背景輸入）、`out_top`（即時輸出）。

## 核心模型（不要改架構）
- **物件 = artboard 內的 panel COMP；物件自己的 `Object` custom page 是唯一真值**：
  `Docx Docy Docw Doch Zorder Selected Locked Objtype Generated Frame Framecolor* Framealpha Fontsizedoc Textrole Imagefile Imagefit Sourcetop Rectstyle Strokewidth Strokecolor* Strokealpha`。
- 內建 panel par 一律是**表達式**：`x = Docx*Zoom`、`layer = Zorder`…；pan 由 artboard 承擔。`Objtype` ∈ `text | rect | image | ellipse`。
- 畫布尺寸由 par 推導，**永不量測**：`CanvasSize() = (root.w - Chromew, root.h - Chromeh)`，必須等於 `canvas_area.par.w/h`。
- 單一輸入路徑：`canvas_input` → doc 空間 hit-test；物件全部 `clickthrough`。拖曳期間寫在 undo 外，mouse up 時倒回再於一個 undo block 內重套。
- 影像來源：**root `Images` 頁的 `ImgN` 槽是真值**；物件 `Sourcetop` 表達式 = `parent.ltool.ImageSlotTop(me)`（`Imgrev` 當依賴）。連 TOP 優先於檔案。
- 使用者「填了圖」的影像區塊 = 使用者內容：`ImportImage`/`PlaceTop` 清掉 `Generated`；`GenerateLayout` 再用 `_hasPicture` 保險。
- Re-roll：Locked 不動；unlocked Generated 刪掉重生；unlocked 手放物件保留並換格；`KEEP_ASPECT = ('ellipse','image')` 保持比例；生成的矩形一律 stroke。
- 存檔格式 v2（v1 矩形讀成 fill）；`SKIP_PARS` 為樣板擁有、不存的 par；讀檔只寫 CONSTANT 模式的 par。

## Root custom pages（公開介面）
Doc（`Docw Doch Paper Paperalpha Docbase Clipframe`）· View（`Zoom Panx Pany Zoomfit Zoomreset Inspshow`）· Snap · Grid（含 `Gen*`、`Gridseed`、`Gridfront`）· State（`Status Imgrev Picker*`）· Style（`Toolsw Chromew Chromeh`）· Export（`Docpath Savedoc Loaddoc Imagecopy Assetfolder`）· Background（`Bgenable Bgfit Bgopacity`）· Images（`ImgN`，自動維護）。
**每個 custom par 都有中英雙語 `help`**，新增 par 時照做。TD 只在按住 Alt、滑鼠停在參數**名稱**上時才顯示。

## 程式慣例
- 被 DAT／表達式呼叫的 extension 方法必須**大寫開頭**（promoted）。
- 用 `parent.ltool` 或相對路徑，**不用絕對路徑**；檔案路徑相對 `project.folder`（外部圖片複製進 `assets/images`）。
- 所有 mutation 包 `ui.undo.startBlock/endBlock`；按鈕走 `DoAction(name, ...)`；參數面板寫入走 `FieldSet`。
- 沿用既有命名與註解密度；小改用精準字串替換，不整份覆寫 DAT。

## TD 陷阱（都踩過）
- **不要從腳本讀 `panelCOMP.width/.height`**：與 display 切換同幀會永久凍結 layout。用 par 推導。
- Panel layout 慢一幀；`run()` 與 parexec callback 在之後的幀才觸發 → **測試要跨幀**（`run(..., delayFrames=N)` + textport 印結果），同步測試無效。
- menu par 出現在另一個 menu 的表達式裡會傳 INDEX 不是名稱 → 用 `.eval()`。
- **相對 OP 路徑字串以擁有者為基準解析**：不要在不同 owner 間共用路徑字串（BIND 就是這樣壞的）。寫 OP par 時給 OP 物件。
- parameterexecuteDAT 不會監看之後才建立的 par／op。
- OP par 表達式回傳 None → 出現路徑 "None" 警告；表達式要有 fallback（見 `sel.par.top`）。
- `Zorder` 是 INT：重排用 list swap，不要加小數。
- 匯出不能信 Status 字串：`ExportFinish` 會檢查像素並重抓（`EXPORT_RETRIES`）；匯出解析度必須是表達式（`Docw*Exportscale`）。
- 存檔：先確認目標檔名不存在再 `project.save()`（`general.inc` 會自動加號）；同時 `layout_tool.save('layout_tool.tox')`。

## 驗證（每次改動後）
1. `td_get_errors('/project1/layout_tool', recursive=True)` → 0 錯誤 0 警告。
2. 跨幀自動測試（textport 印 PASS/FAIL），測完**還原使用者的版面**（刪測試物件）。
3. `td_get_screenshot('/project1/layout_tool/canvas_area')` 目視確認。
4. `.click()`／模擬滑鼠會繞過 clickthrough gate → 關鍵互動請使用者用真滑鼠確認。
5. 存 `.toe` + 匯出 `.tox`。

## Do not
- 刪除任何 op 前先問使用者（含自動生成的 DAT）。
- 不要動 `/project1/Dragon_skin_Particle`（使用者自己的元件，它的警告不是這個工具的）。
- 不做旋轉、per-pair kerning（雙方同意延後；panel COMP 不能旋轉）。
- 不把進行中狀態寫進這份檔案 → `docs/ai/HANDOFF.md`。
- 不把 `.toe`、`Backup/`、`assets/images/`、使用者截圖／錄影推上公開 repo（見 `.gitignore`）。

## 交接流程（solo：只有 Claude Code，多台電腦）
- 開工：`git pull` → `python scripts/device_lock.py status`；空閒才 `acquire --device "<機器名>" --note "..."`；讀 `docs/ai/HANDOFF.md`，先跟使用者報告現況。
- 收工：`release`；**整份覆寫** `docs/ai/HANDOFF.md`（做完了嗎／改了哪裡／不能碰／要人決定）；新增 `docs/ai/log/<日期>-<機器>.md`（不改舊的）；`git add`/`commit`/`push`。**push 是最常被漏掉的一步。**
