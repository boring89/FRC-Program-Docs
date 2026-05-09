如何閱讀這個專案
===============

1. 從 `Robot.java` 開始，理解機器人生命週期。
2. 進入 `RobotContainer.java`，查看元件與按鍵綁定。
3. 閱讀 `SwerveControlCmd.java`，理解駕駛控制的轉換與輸出。
4. 閱讀 `ArmControl.java`，了解機械臂如何用命令組合表達不同動作。

學習路徑
~~~~~~~~

**初學者建議**：

- 先閱讀 Robot.java 和 RobotContainer.java，掌握整體架構
- 理解 SwerveControlCmd 的輸入處理邏輯
- 分析 ArmControl 中 Commands.either 的使用方式

**進階學習**：

- 研究 SwerveSubsystem 的運動學實現
- 分析 Limelight 視覺系統的整合方式
- 學習如何擴展命令序列以實現更複雜動作

程式碼導讀
~~~~~~~~~~

- **Robot.java**：入口點，負責初始化和模式切換
- **RobotContainer.java**：組裝工廠，連接所有元件
- **SwerveControlCmd.java**：驅動邏輯的核心
- **ArmControl.java**：機械臂控制的狀態機實現

建議練習
~~~~~~~~

1. 修改 SwerveControlCmd 中的死區值，觀察對控制的影響
2. 在 ArmControl 中添加新的按鈕綁定
3. 實現一個新的機械臂位置設定
4. 整合額外的感測器輸入到控制邏輯中