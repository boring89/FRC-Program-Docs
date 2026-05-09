專案設定與常數定義
==================

在開始編寫 Swerve 驅動程式之前，我們需要建立一個新的 WPILib Java 專案並定義所有必要的常數。

專案建立
--------

1. 開啟 VS Code
2. 使用 WPILib 建立新的 Java Command-Based 專案
3. 設定團隊編號和專案名稱

建立 Constants.java 檔案
-------------------------

建立一個新的 Java 類別來存放所有常數：

.. code-block:: java

   package frc.robot;

   import edu.wpi.first.math.geometry.Translation2d;
   import edu.wpi.first.math.util.Units;

   public final class Constants {

**模組常數 - 定義輪子和馬達的基本參數**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

這些常數定義了 Swerve 模組的物理參數：

.. code-block:: java

     public static final class ModuleConstants {
       // William 常數 - 用於校正齒輪箱效率
       // 這個值通常通過測試來確定齒輪箱的實際效率
       public static final double WilliamConstant = 1.042;

       // 輪子直徑轉換為米
       // 將英吋轉換為米，因為 WPILib 使用米為單位
       public static final double kWheelDiameterMeters = Units.inchesToMeters(4);

       // 齒輪比設定
       // 驅動馬達的齒輪比（輸出轉速 / 輸入轉速）
       public static final double kDriveMotorGearRatio = 1 / 5.95;
       // 轉向馬達的齒輪比
       public static final double kTurningMotorGearRatio = 1 / 19.6;

       // 編碼器轉換因子 - 將編碼器讀數轉換為實際距離/角度
       // 驅動編碼器：將馬達轉數轉換為輪子行進距離（米）
       public static final double kDriveEncoderRot2Meter = kDriveMotorGearRatio * Math.PI * kWheelDiameterMeters;
       // 轉向編碼器：將馬達轉數轉換為輪子角度（弧度）
       public static final double kTurningEncoderRot2Rad = kTurningMotorGearRatio * 2 * Math.PI;

       // RPM 轉換為實際速度
       public static final double kDriveEncoderRPM2MeterPerSec = kDriveEncoderRot2Meter / 60;
       public static final double kTurningEncoderRPM2RadPerSec = kTurningEncoderRot2Rad / 60;

       // 馬達參數計算
       // NEO 馬達的自由轉速（轉/分）
       public static final double kDrivingMotorFreeSpeedRps = MotorConstants.kNeoFreeSpeedRpm / 60;
       // 輪子周長
       public static final double kWheelCircumferenceMeters = kWheelDiameterMeters * Math.PI;
       // 總減速比（包含 William 常數）
       public static final double kDrivingMotorReduction = 5.95 * WilliamConstant;
       // 輪子的最大自由轉速（轉/秒）
       public static final double kDriveWheelFreeSpeedRps = (kDrivingMotorFreeSpeedRps * kWheelCircumferenceMeters)
           / kDrivingMotorReduction;
     }

**馬達常數 - 定義馬達的基本參數**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

     public static final class MotorConstants {
       // NEO 馬達的額定自由轉速（轉/分）
       public static final double kNeoFreeSpeedRpm = 6784;
     }

**驅動系統常數 - 定義整個驅動系統的參數**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

     public static final class DrivetrainConstants {
       // ===== 速度限制設定 =====
       // 機器人的最大速度（米/秒）
       public static final double kMaxSpeedMetersPerSecond = 6.5;
       // 遙控操作時的速度（較慢更安全）
       public static final double kTeleOpSpeedMetersPerSecond = 2;
       // 最大旋轉速度（弧度/秒）
       public static final double kMaxAngularSpeedRadiansPerSecond = 2 * 1.8 * Math.PI;

       // ===== CAN ID 設定 =====
       // 每個模組需要 3 個 CAN ID：{驅動馬達, 轉向馬達, 絕對編碼器}
       public static final int[] kFrontLeftModuleIDs = { 4, 8, 12 };
       public static final int[] kFrontRightModuleIDs = { 3, 7, 11 };
       public static final int[] kBackLeftModuleIDs = { 2, 6, 10 };
       public static final int[] kBackRightModuleIDs = { 1, 5, 9 };

       // ===== 馬達方向設定 =====
       // {驅動馬達是否反轉, 轉向馬達是否反轉}
       // 這些值需要根據實際接線和測試來調整
       public static final boolean[] kFrontLeftModuleInverted = { false, true };
       public static final boolean[] kFrontRightModuleInverted = { true, true };
       public static final boolean[] kBackLeftModuleInverted = { false, true };
       public static final boolean[] kBackRightModuleInverted = { true, true };

       // ===== 模組位置設定 =====
       // 每個輪子相對於機器人中心的座標（米）
       // 這決定了運動學計算的準確性
       public static final Translation2d[] moduleLocations = new Translation2d[] {
           new Translation2d(0.278, 0.278),   // 前左輪位置
           new Translation2d(0.278, -0.278),  // 前右輪位置
           new Translation2d(-0.278, 0.278),  // 後左輪位置
           new Translation2d(-0.278, -0.278)  // 後右輪位置
       };

       // ===== 速度變化率限制 =====
       // 防止突然的加速度變化，提供更平滑的控制
       public static final double kTeleOpDrivePositiveSlewRate = 5;   // 正向加速度限制
       public static final double kTeleOpDriveNegativeSlewRate = 20;  // 負向加速度限制（剎車更快）
     }
   }

常數說明
--------

**William 常數**
   用於校正齒輪箱的實際效率。這個值需要通過實際測試來確定，通常在 1.0-1.1 之間。

**CAN ID 配置**
   每個 Swerve 模組需要 3 個 CAN ID：
   - 驅動馬達（REV Robotics Spark）
   - 轉向馬達（REV Robotics Spark）
   - 絕對編碼器（CTRE CANcoder）

**馬達方向設定**
   這些布林值決定馬達的旋轉方向。需要根據實際接線和測試來調整。

**模組位置**
   每個輪子相對於機器人質心的座標。這些值對於運動學計算的準確性至關重要。

下一步
------

現在我們已經定義了所有必要的常數，接下來要建立 SwerveModule 類別。

:doc:`swerve-module`