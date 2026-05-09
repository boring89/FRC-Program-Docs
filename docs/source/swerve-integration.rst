系統整合與測試
==============

現在我們已經建立了所有的組件，最後一步是將它們整合到 RobotContainer 中，並進行測試和調校。

系統整合
--------

建立 RobotContainer.java - 機器人容器
--------------------------------------

RobotContainer 是所有子系統和命令的中央集線器：

.. code-block:: java

   package frc.robot;

   import edu.wpi.first.wpilibj2.command.Command;
   import edu.wpi.first.wpilibj2.command.InstantCommand;
   import frc.robot.commands.TeleOpCommand;
   import frc.robot.subsystems.Controller.DriverJoystick;
   import frc.robot.subsystems.Drivetrain.Drivetrain;

   public class RobotContainer {

     // ===== 子系統實例 =====
     private final DriverJoystick driverJoystick = new DriverJoystick(0);
     private final Drivetrain drivetrain = new Drivetrain();

     public RobotContainer() {
         // ===== 設定預設命令 =====
         // 當沒有其他命令運行時，執行遙控操作
         this.drivetrain.setDefaultCommand(
             new TeleOpCommand(drivetrain, driverJoystick)
         );

         // ===== 配置按鈕綁定 =====
         configureBindings();
     }

     private void configureBindings() {
         // ===== 按鈕功能綁定 =====

         // B 按鈕：歸零機器人朝向
         this.driverJoystick.zeroHeading()
             .onTrue(new InstantCommand(() -> drivetrain.zeroHeading()));

         // 右肩按鈕：切換速度模式
         // 按下時全速，放開時半速
         this.driverJoystick.fullSpeedMode()
             .onTrue(drivetrain.fullSpeedCommand())
             .onFalse(drivetrain.halfSpeedCommand());
     }

     // ===== 自動程式命令 =====
     public Command getAutonomousCommand() {
         // 這裡可以返回自動程式命令
         // 目前返回 null，表示沒有自動程式
         return null;
     }
   }

專案結構總覽
------------

完成後的專案結構應該如下：

::

   src/main/java/frc/robot/
   ├── Constants.java                    # 所有常數定義
   ├── RobotContainer.java               # 系統整合
   ├── Main.java                         # 程式入口點
   ├── Robot.java                        # 主要機器人類別
   ├── commands/
   │   └── TeleOpCommand.java           # 遙控操作命令
   └── subsystems/
       ├── Controller/
       │   └── DriverJoystick.java      # 搖桿控制器
       └── Drivetrain/
           ├── Drivetrain.java          # 主要驅動系統
           ├── SwerveModule.java        # 單個模組控制
           └── ModuleConfigs.java       # 馬達配置

測試與調校
----------

編譯和部署
~~~~~~~~~~

1. **編譯專案**：使用 VS Code 的 Gradle 任務編譯
2. **部署到機器人**：使用 Driver Station 部署程式
3. **測試基本功能**：確認機器人可以移動和旋轉

硬體調校
~~~~~~~~

**CAN ID 設定**：
   - 確保所有馬達和編碼器的 CAN ID 正確
   - 使用 REV Hardware Client 或 Phoenix Tuner 確認

**馬達方向**：
   - 調整 ``kModuleInverted`` 陣列中的布林值
   - 測試每個輪子是否朝正確方向旋轉

**編碼器校正**：
   - 確保絕對編碼器安裝角度正確
   - 檢查輪子角度是否與編碼器讀數匹配

PID 調校
~~~~~~~~

**驅動馬達 PID**：
   - P 參數：從 0.1 開始，逐步增加直到出現振盪
   - I 參數：通常設為 0，除非有靜態誤差
   - D 參數：用於抑制振盪，通常很小

**轉向馬達 PID**：
   - P 參數：較高，因為需要精確角度控制
   - I 參數：小量用於克服靜摩擦
   - D 參數：中等大小，防止過沖

常見問題排除
~~~~~~~~~~~~

**輪子不轉動**：
   - 檢查 CAN ID 是否正確
   - 確認馬達電源和接線
   - 驗證馬達方向設定

**角度不正確**：
   - 調整馬達方向設定
   - 檢查絕對編碼器安裝角度
   - 確認編碼器偏移值

**控制不平滑**：
   - 增加速度限制器參數
   - 調整 PID 參數
   - 檢查編碼器轉換因子

**陀螺儀漂移**：
   - 定期校正陀螺儀
   - 使用場地重置功能
   - 考慮添加視覺定位校正

進階功能
~~~~~~~~

**添加視覺定位**：
   - 整合 Limelight 或 PhotonVision
   - 使用 ``addVisionMeasurement()`` 融合數據

**自定義運動學**：
   - 修改輪子位置以適應特殊底盤設計
   - 添加輪子直徑補償

**碰撞避免**：
   - 添加加速度限制
   - 實現防翻覆保護

總結
----

恭喜！你已經成功建立了一個完整的 Swerve 驅動系統！

**學習要點：**

- **模組化設計**：將複雜系統分解為可管理的組件
- **運動學原理**：理解輪子協調運動的數學基礎
- **PID 控制**：學習閉環控制系統的調校
- **Command-Based 架構**：掌握現代 FRC 程式設計模式

**下一步建議：**

1. 仔細測試每個功能
2. 根據你的機器人調整常數
3. 學習 PathPlanner 建立自動程式
4. 探索進階功能如視覺定位

記住，調校是一個反覆的過程。從簡單的移動測試開始，逐步增加複雜度。祝你在 FRC 競賽中取得好成績！