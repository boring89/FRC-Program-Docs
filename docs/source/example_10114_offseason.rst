10114 OffSeason 範例教學
=======================

這個範例展示了一個 FRC Command-Based 機器人專案，包含機械臂控制、全向輪(Swerve)驅動與目標對齊控制。
本教學針對初學者說明程式架構、主要類別與常見設計模式。

專案概覽
--------

GitHub 連結：https://github.com/boring89/10114-OffSeason-2025

這個專案是一個完整的 FRC 機器人程式範例，專注於 2025 年 offseason 期間的開發。專案名稱為 10114-OffSeason-2025，屬於隊伍 10114 的 offseason 專案。程式使用 Java 語言，基於 WPILib 的 Command-Based 架構，整合了 Swerve 全向輪驅動系統、機械臂控制，以及視覺對齊功能。

主要結構如下：

- `src/main/java/frc/robot/Robot.java`：機器人生命週期與模式切換
- `src/main/java/frc/robot/RobotContainer.java`：按鍵綁定與預設命令設定
- `src/main/java/frc/robot/commands/Control/Drivetrain/SwerveControlCmd.java`：全向輪操作邏輯
- `src/main/java/frc/robot/subsystems/Arm/ArmControl.java`：機械臂狀態與按鈕對應
- `src/main/java/frc/robot/subsystems/Drivetrain/SwerveSubsystem.java`：驅動機構與感測器

專案的特點包括：

- 使用 Swerve 全向輪系統，提供靈活的移動能力
- 機械臂控制，支持多種位置設定和動作
- 整合 Limelight 視覺系統，用於目標對齊
- 支援 PathPlanner 和 Choreo 路徑規劃工具
- 包含自動程式框架，雖然目前被註解

這個專案適合學習 Command-Based 程式設計模式，以及如何整合多個子系統進行協調控制。

教學內容
--------

.. toctree::
   :maxdepth: 1

   10114-robot
   10114-robotcontainer
   10114-swerve
   10114-arm
   10114-motor-control
   10114-why-example
   10114-how-to-read
---------------

`Robot` 類別繼承 `TimedRobot`，這是 WPILib 最常見的機器人入口。
它負責：

- 初始化 `RobotContainer`
- 在每個週期呼叫 `CommandScheduler.getInstance().run()`
- 處理 `autonomousInit()`、`teleopInit()`、`testInit()` 等模式切換

在此範例中，`robotPeriodic()` 確保命令排程器持續執行，這是 Command-Based 專案的必要設定。

主要特點
~~~~~~~~

- 程式保留了 PathPlanner 及 Choreo 相關的路徑加載。
- `autonomousInit()` 的自動程式碼目前被註解掉，意味著本專案現階段主要著重於手動控制。
- 使用 `DriverStation.getAlliance()` 判斷是否為紅隊，以便日後自動程式考慮場地方向。

RobotContainer.java 介紹
------------------------

`RobotContainer` 負責建構子系統、設定預設命令及按鍵綁定。
在本範例中：

- `SwerveSubsystem` 被設為預設命令 `SwerveControlCmd`
- `ArmControl` 管理按鍵與機械臂動作
- `Limelight_Right` / `Limelight_Left` 提供目標對齊輸入
- `Driver` 封裝搖桿按鈕與軸值輸入

按鍵範例
~~~~~~~~

- `driver.zeroHeading()`：按鈕觸發後重置全向輪朝向與里程計
- `driver.changeMode()`：切換機械臂模式（例如 Coral / Algae）
- `driver.LeftTrigger()` / `driver.RightTrigger()`：分別執行進料與發射命令
- `driver.LBumper()` / `driver.RBumper()`：啟用左右 Limelight 對齊驅動

SwerveControlCmd 範例
----------------------

`SwerveControlCmd` 是驅動預設命令，它負責：

1. 從操縱桿讀取前後、左右與轉向速度
2. 套用死區值，避免微小輸入造成車體晃動
3. 將速度值縮放成實際最大速率
4. 決定場地相對或機器相對控制
5. 將速度轉換成每個全向輪的目標狀態

其中，`fieldOrientedFunc.get()` 決定是否使用場地座標系；如果啟用，機器人方向不受自身朝向影響。

ArmControl 範例
----------------

`ArmControl` 將按鈕輸入轉換為一系列命令：

- `ButtonA()`、`ButtonB()`、`ButtonX()`、`ButtonY()` 分別對應不同位置設定
- `LeftTriggerPressed()` 會進行進料並監測 `hand.isCoralIn()` 狀態
- `RightTriggerPressed()` 觸發發射控制
- `Commands.either(...)` 可讓按鈕輸入根據模式判斷要執行哪套命令

這是一個典型的 Command-Based 設計，將「何時觸發」與「要做什麼」分離，讓按鍵邏輯更容易閱讀與調整。

為何這個專案適合作為範例？
~~~~~~~~~~~~~~~~~~~~~~~~~~

- 示範 Swerve 全向輪的基本控制流程
- 展示多重按鍵模式與命令序列組合
- 包含視覺對齊與自動模式切換的起始架構
- 使用 WPILib 的 Command Scheduler 來管理機器人行為

如何閱讀這個專案
----------------

1. 從 `Robot.java` 開始，理解機器人生命週期。
2. 進入 `RobotContainer.java`，查看元件與按鈕綁定。
3. 閱讀 `SwerveControlCmd.java`，理解駕駛控制的轉換與輸出。
4. 閱讀 `ArmControl.java`，了解機械臂如何用命令組合表達不同動作。

建議練習
~~~~~~~~

- 將 `SwerveControlCmd` 的 `fieldOrientedFunc` 改成條件按鈕開關。
- 在 `RobotContainer` 中啟用 `m_autonomousCommand`，測試簡單的自動路徑。
- 新增一個 `Command`，讓機械臂回到安全待機位置。
