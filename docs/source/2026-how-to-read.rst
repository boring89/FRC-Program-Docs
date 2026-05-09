如何閱讀這個專案
===============

1. 從 `Robot.java` 開始，理解記錄與機器人生命週期。
2. 閱讀 `RobotContainer.java`，掌握操縱桿綁定與預設命令。
3. 研究 `AutoChooser.java`，了解自動程式選擇邏輯。
4. 分析 `PhotonVision.java`，學習視覺處理技術。
5. 查看 `sysidTest()` 方法，認識系統識別測試。

學習路徑
~~~~~~~~

**中階學習者**：

- 先掌握 LoggedRobot 的記錄機制
- 理解多控制器按鍵綁定的複雜邏輯
- 分析 AutoChooser 的路徑組合演算法

**高階學習者**：

- 深入研究 PhotonVision 的姿態估計和過濾邏輯
- 學習 SysId 測試的應用和資料分析
- 研究 superstructure 的子系統協調設計

程式碼導讀
~~~~~~~~~~

- **Robot.java**：LoggedRobot 架構和記錄系統
- **RobotContainer.java**：複雜的子系統整合和事件處理
- **AutoChooser.java**：動態自動程式選擇邏輯
- **PhotonVision.java**：先進視覺處理和里程計融合
- **sysidTest()**：系統識別和參數調校工具

建議練習
~~~~~~~~

1. 修改 AutoChooser 的選擇邏輯，添加新的路徑組合
2. 在 PhotonVision 中調整姿態估計的過濾參數
3. 實現一個新的 SysId 測試按鍵綁定
4. 分析記錄資料並優化控制器參數