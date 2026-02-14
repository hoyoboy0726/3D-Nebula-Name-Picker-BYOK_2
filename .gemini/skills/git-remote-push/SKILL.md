---
name: git-remote-push
description: 處理將本地更改推送到遠端倉庫（如 GitHub）。自動偵測遠端預設分支，同步分支命名，並處理權限問題。
---

# Git 遠端推送工作流 (Git Remote Push Workflow)

當使用者要求將程式碼「推送」、「上傳」至 GitHub 或任何遠端倉庫時，請遵循此工作流。

## 1. 環境偵測 (Environment Discovery)

在執行推送前，必須先確認遠端狀態：
- **執行指令**：`git remote -v` 獲取遠端 URL。
- **執行指令**：`git ls-remote --symref origin HEAD` 識別遠端的預設分支名稱（通常為 `main` 或 `master`）。

## 2. 分支同步策略 (Branch Sync Strategy)

不要假設本機分支名稱與遠端一致。
- **檢查目前分支**：`git branch --show-current`。
- **執行推送**：
    - 若本機分支為 `master` 且遠端預設為 `main`，執行 `git push origin master:main`。
    - 若遠端已有內容，且需要覆蓋或同步，應根據情況加上 `--force` 並告知使用者原因。
    - **原則**：直接使用遠端最新的分支資訊進行對應推送，不需詢問使用者是否重新命名本機分支。

## 3. 權限與安全性處理 (Permissions & Security)

- **403 Forbidden 錯誤**：若推送失敗顯示權限不足，主動建議使用者將帳號嵌入 URL：
    - `git remote set-url origin https://<username>@github.com/<username>/<repo>.git`
- **憑證檢查**：提醒使用者 Windows 認證管理員 (Credential Manager) 可能存有舊憑證。

## 4. 驗證 (Verification)

推送完成後，執行 `git ls-remote origin` 確認遠端 `HEAD` 是否已更新，或提供遠端倉庫連結供使用者確認。

## 5. 注意事項

- **禁止自動 Push**：始終向使用者說明即將執行的 Git 指令及其影響，取得同意後再執行。
- **Gitignore 檢查**：在推送前確認 `.gitignore` 已包含必要排除項（如 `node_modules`, `.env`）。
