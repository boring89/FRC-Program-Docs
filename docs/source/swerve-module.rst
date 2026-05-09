建立 SwerveModule 類別
====================

SwerveModule 是單個輪子的控制單位，包含驅動馬達、轉向馬達和絕對編碼器。每個 Swerve 驅動系統通常有 4 個這樣的模組。

模組組成
--------

每個 SwerveModule 包含以下組件：

- **驅動馬達**：REV Robotics Spark Flex，負責提供前進動力
- **轉向馬達**：REV Robotics Spark Max，負責控制輪子方向
- **絕對編碼器**：CTRE CANcoder，記住輪子的絕對角度位置

建立 ModuleConfigs.java - 馬達配置
-----------------------------------

首先建立馬達的配置類，設定 PID 參數和基本配置：

.. code-block:: java

   package frc.robot.subsystems.Drivetrain;

   import com.revrobotics.spark.config.ClosedLoopConfig.FeedbackSensor;
   import com.revrobotics.spark.config.SparkBaseConfig.IdleMode;
   import com.revrobotics.spark.config.SparkFlexConfig;
   import com.revrobotics.spark.config.SparkMaxConfig;

   import frc.robot.Constants.ModuleConstants;

   public class ModuleConfigs {
       public static final SparkFlexConfig driveConfig = new SparkFlexConfig();
       public static final SparkMaxConfig steerConfig = new SparkMaxConfig();

       static {
           // ===== 驅動馬達配置 =====
           // 計算轉換因子
           double drivingFactor = ModuleConstants.kWheelDiameterMeters * Math.PI
                   / ModuleConstants.kDrivingMotorReduction;
           double turningFactor = ModuleConstants.kTurningMotorGearRatio * 2 * Math.PI;
           double drivingVelocityFeedForward = 1 / ModuleConstants.kDriveWheelFreeSpeedRps;

           // 設定驅動馬達基本參數
           driveConfig
                   .idleMode(IdleMode.kBrake)  // 剎車模式，停止時鎖定
                   .smartCurrentLimit(50);     // 電流限制（安培）

           // 設定編碼器轉換因子
           driveConfig.encoder
                   .positionConversionFactor(drivingFactor)        // 位置轉換：轉數 → 米
                   .velocityConversionFactor(drivingFactor / 60.0); // 速度轉換：RPM → 米/秒

           // 設定閉環控制（PID + 前饋）
           driveConfig.closedLoop
                   .feedbackSensor(FeedbackSensor.kPrimaryEncoder)  // 使用內建編碼器
                   .pid(0.13, 0.000, 0)                           // PID 參數（P, I, D）
                   .velocityFF(drivingVelocityFeedForward)         // 前饋補償
                   .outputRange(-1, 1);                           // 輸出範圍（-100% 到 100%）

           // ===== 轉向馬達配置 =====
           steerConfig
                   .idleMode(IdleMode.kBrake)
                   .smartCurrentLimit(40);

           steerConfig.encoder
                   .positionConversionFactor(turningFactor)       // 位置轉換：轉數 → 弧度
                   .velocityConversionFactor(turningFactor / 60.0); // 速度轉換：RPM → 弧度/秒

           steerConfig.closedLoop
                   .feedbackSensor(FeedbackSensor.kPrimaryEncoder)
                   .pid(1.65, 0.0007, 0)                         // 轉向 PID 參數
                   .outputRange(-1, 1)
                   .positionWrappingEnabled(true)                 // 啟用位置環繞
                   .positionWrappingInputRange(-Math.PI, Math.PI); // 角度範圍：-π 到 π
       }
   }

建立 SwerveModule.java - 單個模組控制
-------------------------------------

現在建立主要的 SwerveModule 類別：

.. code-block:: java

   package frc.robot.subsystems.Drivetrain;

   import com.ctre.phoenix6.hardware.CANcoder;
   import com.revrobotics.RelativeEncoder;
   import com.revrobotics.spark.SparkClosedLoopController;
   import com.revrobotics.spark.SparkFlex;
   import com.revrobotics.spark.SparkMax;
   import com.revrobotics.spark.SparkBase.ControlType;
   import com.revrobotics.spark.SparkBase.PersistMode;
   import com.revrobotics.spark.SparkBase.ResetMode;
   import com.revrobotics.spark.SparkLowLevel.MotorType;

   import edu.wpi.first.math.geometry.Rotation2d;
   import edu.wpi.first.math.kinematics.SwerveModulePosition;
   import edu.wpi.first.math.kinematics.SwerveModuleState;
   import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
   import edu.wpi.first.wpilibj2.command.SubsystemBase;

   public class SwerveModule extends SubsystemBase{

       // ===== 硬體組件 =====
       private final SparkFlex driveMotor;      // 驅動馬達（強力馬達）
       private final SparkMax steerMotor;       // 轉向馬達
       private final CANcoder absEncoder;       // 絕對編碼器（記住角度）

       // ===== 控制器和編碼器 =====
       private final RelativeEncoder driveEncoder, steerEncoder;
       private final SparkClosedLoopController driveController, steerController;

**建構函式 - 初始化所有組件**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public SwerveModule(
           int driveMotorID,      // 驅動馬達的 CAN ID
           int steerMotorID,      // 轉向馬達的 CAN ID
           int absEncoderID,      // 絕對編碼器的 CAN ID
           boolean isDriveMotorInverted,  // 驅動馬達是否反轉
           boolean isSteerMotorInverted   // 轉向馬達是否反轉
       ) {
           // 初始化馬達
           this.driveMotor = new SparkFlex(driveMotorID, MotorType.kBrushless);
           this.steerMotor = new SparkMax(steerMotorID, MotorType.kBrushless);

           // 獲取控制器（用於 PID 控制）
           this.driveController = this.driveMotor.getClosedLoopController();
           this.steerController = this.steerMotor.getClosedLoopController();

           // 獲取編碼器（測量位置和速度）
           this.driveEncoder = this.driveMotor.getEncoder();
           this.steerEncoder = this.steerMotor.getEncoder();

           // 初始化絕對編碼器
           this.absEncoder = new CANcoder(absEncoderID);

           // 配置馬達設定
           configure(isDriveMotorInverted, isSteerMotorInverted);

           // 重置編碼器位置
           resetEncoders();
       }

**配置方法 - 設定馬達參數**
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public void configure(boolean isDriveMotorInverted, boolean isSteerMotorInverted) {
           // 將配置應用到驅動馬達
           this.driveMotor.configure(
               ModuleConfigs.driveConfig.inverted(isDriveMotorInverted),
               ResetMode.kResetSafeParameters,  // 重置安全參數
               PersistMode.kPersistParameters   // 保存參數到快閃記憶體
           );

           // 將配置應用到轉向馬達
           this.steerMotor.configure(
               ModuleConfigs.steerConfig.inverted(isSteerMotorInverted),
               ResetMode.kResetSafeParameters,
               PersistMode.kPersistParameters
           );
       }

**編碼器方法 - 讀取和重置位置**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       // 讀取絕對編碼器的角度（弧度）
       public double getAbsoluteEncoderPosition() {
           double angle = this.absEncoder.getAbsolutePosition().getValueAsDouble() * 2 * Math.PI;
           // 在 SmartDashboard 上顯示角度，用於調試
           SmartDashboard.putNumber("absolutEncoderAngle", angle);
           return angle;
       }

       // 重置編碼器位置
       // 將相對編碼器的位置設定為絕對編碼器的讀數
       public void resetEncoders() {
           this.driveEncoder.setPosition(0);
           this.steerEncoder.setPosition(getAbsoluteEncoderPosition());
       }

       // 獲取當前位置和速度
       public double getDrivePosition() { return this.driveEncoder.getPosition(); }
       public double getSteerPosition() { return this.steerEncoder.getPosition(); }
       public double getDriveVelocity() { return this.driveEncoder.getVelocity(); }
       public double getSteerVelocity() { return this.steerEncoder.getVelocity(); }

**狀態獲取方法 - 取得模組狀態**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       // 獲取模組位置（距離和角度）
       public SwerveModulePosition getPosition() {
           return new SwerveModulePosition(
               this.getDrivePosition(),           // 行進距離（米）
               Rotation2d.fromRadians(this.getSteerPosition())  // 輪子角度
           );
       }

       // 獲取模組狀態（速度和角度）
       public SwerveModuleState getState() {
           return new SwerveModuleState(
               this.getDriveVelocity(),           // 輪子速度（米/秒）
               Rotation2d.fromRadians(this.getSteerPosition())  // 輪子角度
           );
       }

**控制方法 - 設定目標狀態**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public void setState(SwerveModuleState state) {
           // 優化角度：選擇轉動較少的方嚮
           // 例如：如果目標是 350°，但當前是 10°，會改為 -10°
           state.optimize(Rotation2d.fromRadians(this.getSteerPosition()));

           // 設定驅動馬達速度（使用 PID 控制）
           this.driveController.setReference(
               state.speedMetersPerSecond,     // 目標速度
               ControlType.kVelocity          // 速度控制模式
           );

           // 設定轉向馬達角度（使用 PID 控制）
           this.steerController.setReference(
               state.angle.getRadians(),       // 目標角度（弧度）
               ControlType.kPosition          // 位置控制模式
           );
       }
   }

關鍵概念
--------

**角度優化**
   ``state.optimize()`` 方法確保輪子總是選擇轉動角度較小的方向旋轉，提高效率。

**絕對 vs 相對編碼器**
   - 絕對編碼器記住輪子的絕對角度，即使電源關閉
   - 相對編碼器只記錄自上次重置以來的相對位置

**PID 控制**
   - 驅動馬達使用速度控制（維持目標速度）
   - 轉向馬達使用位置控制（達到目標角度）

下一步
------

現在我們已經建立了 SwerveModule，接下來要建立整合所有模組的 Drivetrain 子系統。

:doc:`swerve-drivetrain`