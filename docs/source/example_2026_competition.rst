2026 Competition 範例教學
========================

這個範例展示了一個更完整的 FRC 比賽專案，包含高階記錄、影像偵測、自動路徑選擇與系統識別測試。
本教學說明專案結構、主要元件與如何理解其中的功能。

專案概覽
--------

專案位於 `copilot_source\program\2026-Competition`。
GitHub 連結：https://github.com/FRC-Team-10114/2026-Competition

這個專案是隊伍 10114 在 2026 年 FRC 比賽季的完整機器人程式碼。專案名稱為 2026-Competition，使用 Java 語言開發，基於 WPILib 的 LoggedRobot 架構，整合了先進的記錄系統、視覺處理、自動路徑選擇，以及系統識別測試功能。

主要結構如下：

- `src/main/java/frc/robot/Robot.java`：機器人啟動、模式切換與資料記錄
- `src/main/java/frc/robot/RobotContainer.java`：操縱桿綁定、預設命令、事件與日誌
- `src/main/java/frc/robot/commands/AutoChooser.java`：自動程式選擇器與路徑邏輯
- `src/main/java/frc/robot/subsystems/Drivetrain/CommandSwerveDrivetrain.java`：Swerve 驅動模組
- `src/main/java/frc/robot/subsystems/Vision/PhotonVision.java`：視覺辨識與定位

專案的特點包括：

- 使用 LoggedRobot 進行高階資料記錄和回放
- 整合 PhotonVision 視覺系統，支持目標檢測和定位
- 自動程式選擇器，支援多種起始位置和路徑組合
- 包含系統識別測試，用於調校驅動系統參數
- 支援 SmartDashboard 和 NetworkTables 進行即時監控
- 包含爬升和射手控制等比賽特定功能

這個專案代表了一個現代 FRC 比賽機器人的完整實現，適合學習高階程式設計技巧和系統整合。

教學內容
--------

.. toctree::
   :maxdepth: 1

   2026-robot
   2026-robotcontainer
   2026-autochooser
   2026-vision
   2026-sysid
   2026-shooter-control
   2026-shooter-calculator
   2026-why-example
   2026-how-to-read
---------------

此專案的 `Robot` 類別繼承 `LoggedRobot`，這表示它支援 WPILib 記錄框架。
主要工作包括：

- 以 `Logger.recordMetadata()` 記錄專案資訊
- 若真實機器人則新增 `WPILOGWriter` 與 `NT4Publisher`
- 若模擬則使用 `NT4Publisher`
- 在 `robotInit()` 設定本地路徑搜尋器 `LocalADStarAK`
- 在 `robotPeriodic()` 更新回放/記錄與命令排程器

這份程式碼同時支援比賽時常見的 `autonomousInit()`、`teleopInit()` 與 `testInit()`。

RobotContainer.java 介紹
------------------------

`RobotContainer` 是這個專案的控制中心。它負責：

- 建立 `CommandXboxController` 操作介面
- 建立 `CommandSwerveDrivetrain` 與 `superstructure`
- 建立 `PhotonVision` 與 `AutoAlign`
- 設定預設驅動命令與按鈕綁定
- 建立 `AutoChooser` 與 SmartDashboard 選項
- 啟動 `FollowPathCommand.warmupCommand()` 以提前準備路徑追隨

駕駛控制與按鍵對應
~~~~~~~~~~~~~~~~~~~~

- `drivetrain.setDefaultCommand(...)`：讀取操縱桿數值並將其轉換成速度請求
- `joystick.leftTrigger()` 與 `joystick.rightTrigger()`：分別啟用進料與發射命令
- `joystick.povDown()` / `joystick.povUp()`：控制爬升相關命令
- `controller.b()` / `controller.a()`：切換射手角度設定
- `RobotModeTriggers.disabled()`：在停用時讓驅動系統保持空閒

自動程式設置
----------------

`AutoChooser` 使用多個 `SendableChooser`，讓隊伍可以在 Driver Station 上選擇：

- 起始位置：Left / Center / Right
- 是否走 Center 路徑
- 是否執行爬升結束動作
- 是否使用特定展示路徑

當起始位置選擇為 `None` 時，程式會自動比較當前機器人位姿與預定起點，根據距離選擇最近起點。

AutoChooser 的實作亮點：

- 使用 `NamedCommands.registerCommand(...)` 註冊自定義命令，方便路徑中的動作呼叫
- 以 `PathPlannerAuto` 載入路徑檔案
- 透過 `Commands.sequence(start, end)` 組合起始與結束路徑
- 使用 `Commands.none()` 作為預設空命令，避免空值錯誤

高階功能
~~~~~~~~~~

1. **記錄與回放**：
   - `HootAutoReplay` 允許記錄時間戳與搖桿資料，方便離線回放與分析
   - `Logger`、`WPILOGWriter` 與 `NT4Publisher` 提供資料記錄與網路檢視

2. **影像定位**：
   - `PhotonVision` 與 `AutoAlign` 組合可支援目標對齊功能
   - 這個專案在 `RobotContainer` 中建立了視覺事件與狀態觸發器

3. **系統識別測試**：
   - `sysidTest()` 綁定按鈕組合，執行 `sysIdDynamic()` / `sysIdQuasistatic()`
   - 這是進行驅動系統辨識與調整的重要工具

為何這個專案適合作為範例？
~~~~~~~~~~~~~~~~~~~~~~~~~~

- 展現比賽機器人完整架構與多種子系統互動
- 引入 FRC 常見功能：自動選擇、記錄、視覺、爬升與射手控制
- 示範如何透過 `CommandScheduler` 維護執行流程
- 透過 `SmartDashboard` 選擇與回報機器人狀態

如何閱讀這個專案
----------------

1. 從 `Robot.java` 開始，理解記錄與機器人生命週期。
2. 閱讀 `RobotContainer.java`，掌握操縱桿綁定與預設命令。
3. 開啟 `AutoChooser.java`，了解自動模式如何根據選項組合路徑。
4. 欣賞 `CommandSwerveDrivetrain` 與 `PhotonVision` 的實作，理解競賽驅動需求。

建議練習
~~~~~~~~

- 在 `AutoChooser` 新增自己的路徑選項與 `NamedCommands`。
- 將 `RobotContainer` 的慢速模式改成按鈕切換。
- 嘗試在 `SmartDashboard` 顯示更多狀態資訊，比如當前目標位置或攝影機辨識結果。
