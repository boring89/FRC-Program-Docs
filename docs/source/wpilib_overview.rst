WPILib 概論
===========

WPILib（WPI Robotics Library）是 FRC 標準的機器人程式庫。它提供一套簡單易用的類別和函式，讓隊伍可以直接控制馬達、讀取感測器、與 Driver Station 通訊，並快速建立可比賽使用的機器人程式。

WPILib 的功能包括：

- 馬達控制與速度調整
- 感測器讀取（編碼器、IMU、距離感測器等）
- 網路表格（NetworkTables）資料共享
- 自動模式、遙控模式與週期管理
- 與 Driver Station 的通訊、狀態顯示與日誌

為什麼要使用 WPILib？
---------------------

WPILib 已經為 FRC 比賽環境做了最佳化，能夠幫助你：

- 快速上手，避免從零開始撰寫底層硬體驅動程式
- 將硬體控制與機器人邏輯分離，讓程式更容易維護
- 直接支援 FRC 官方硬體與多數常見第三方設備
- 方便測試、除錯與部署到 RoboRIO

支援的程式語言
--------------

WPILib 支援三種官方語言：

- Java（WPILibJ）
- C++（WPILibC）
- Python（RobotPy）

對於剛開始的隊伍與門外漢，我建議先使用 Java，因為它的語法簡潔，錯誤檢查較多，且 WPILib Java 社群資料最多。

WPILib Java（WPILibJ）
~~~~~~~~~~~~~~~~~~~~

在 Java 中，你可以使用 WPILib 提供的類別，例如 `TimedRobot`、`Joystick`、`PWMSparkMax`、`PIDController` 等，這些類別將複雜的硬體操作封裝起來，讓你能專注在機器人行為與策略上。

如果你看到類似以下程式碼，這就是 WPILib Java 的典型用法：

.. code-block:: java

   import edu.wpi.first.wpilibj.TimedRobot;
   import edu.wpi.first.wpilibj.motorcontrol.PWMSparkMax;

   public class Robot extends TimedRobot {
       private PWMSparkMax motor = new PWMSparkMax(0);

       @Override
       public void teleopPeriodic() {
           motor.set(0.5);
       }
   }

想要知道更多 WPILib 的細節，可以參考官方文件或源碼，但對入門者來說，先了解它是「用來快速控制 FRC 硬體的程式庫」就足夠了。

來源與文件
----------

WPILib 是開放原始碼軟體，Java 和 C++ 的原始碼都可以在 GitHub 上找到。若要查詢更詳細的 API 或函式，請使用官方文件：

- Java 文件
- C++ 文件
- Python 文件

這一章希望讓你理解：WPILib 不是一個單獨的程式，而是一整套讓 FRC 機器人程式更簡單、更可重用的工具集。