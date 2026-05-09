系統識別測試 (SysId)
==================

`sysidTest()` 綁定按鈕組合，執行 `sysIdDynamic()` / `sysIdQuasistatic()`。
這是進行驅動系統辨識與調整的重要工具。

SysId 測試的用途：

- **動態測試 (Dynamic)**：快速變化輸入，用於識別系統的動態響應
- **準靜態測試 (Quasistatic)**：緩慢變化輸入，用於識別靜態摩擦和效率
- 協助調校 PID 控制器參數
- 生成系統模型用於模擬和預測

程式碼輔助
~~~~~~~~~~

以下是 sysidTest 方法的程式碼片段：

.. code-block:: java

   public void sysidTest() {
     // Run SysId routines when holding back/start and X/Y.
     // Note that each routine should be run exactly once in a single log.
     joystick.back().and(joystick.y()).whileTrue(drivetrain.sysIdDynamic(Direction.kForward));
     joystick.back().and(joystick.x()).whileTrue(drivetrain.sysIdDynamic(Direction.kReverse));
     joystick.start().and(joystick.y()).whileTrue(drivetrain.sysIdQuasistatic(Direction.kForward));
     joystick.start().and(joystick.x()).whileTrue(drivetrain.sysIdQuasistatic(Direction.kReverse));
   }

按鍵對應：

- Back + Y：動態測試向前
- Back + X：動態測試向後
- Start + Y：準靜態測試向前
- Start + X：準靜態測試向後

測試流程
~~~~~~~~

1. 在 Driver Station 連接機器人
2. 啟用測試模式
3. 按住對應按鍵組合執行測試
4. 使用 SysId 工具分析記錄資料
5. 根據結果調整控制器參數

這個功能對於精確調校 Swerve 驅動系統至關重要。