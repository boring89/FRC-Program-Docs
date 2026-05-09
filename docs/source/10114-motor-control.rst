馬達控制基礎
============

10114 OffSeason 專案中的馬達控制實現了基本的 PID 控制和視覺輔助瞄準。本頁面介紹專案中使用的控制技術。

PID 控制器應用
~~~~~~~~~~~~~

專案中多處使用了 WPILib 的 PIDController：

- **Swerve 驅動控制**：位置和朝向控制
- **機械臂控制**：位置設定和運動控制
- **視覺瞄準**：目標追蹤和對齊

程式碼輔助 - SwerveSubsystem PID
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

   public class SwerveSubsystem extends SubsystemBase {
       // PID 控制器用於路徑追隨
       private final PIDController xController = new PIDController(10.0, 0.0, 0.0);
       private final PIDController yController = new PIDController(10.0, 0.0, 0.0);
       private final PIDController headingController = new PIDController(7.5, 0.0, 0.0);

       // PathPlanner 自動路徑配置
       public static void configurePathPlanner() {
           AutoBuilder.configure(
               this::getPose,
               this::resetOdometry,
               this::getChassisSpeeds,
               (speeds, feedforwards) -> drive(speeds, feedforwards),
               new PPHolonomicDriveController(
                   new PIDConstants(10.0, 0.0, 0.0),  // X 方向 PID
                   new PIDConstants(10.0, 0.0, 0.0),  // Y 方向 PID
                   new PIDConstants(7.5, 0.0, 0.0)    // 旋轉 PID
               ),
               config,
               () -> false,
               this
           );
       }
   }

機械臂 PID 控制
~~~~~~~~~~~~~

機械臂子系統使用 PID 控制器進行精確位置控制：

.. code-block:: java

   public class Elevator extends SubsystemBase {
       private final PIDController ElevatorController;

       public Elevator() {
           ElevatorController = new PIDController(
               Constants.ElevatorConstants.kP,
               Constants.ElevatorConstants.kI,
               Constants.ElevatorConstants.kD
           );
       }

       public Command setPoint(double setpoint) {
           return this.run(() -> {
               double output = ElevatorController.calculate(getPosition(), setpoint);
               setMotor(output);
           });
       }
   }

視覺輔助瞄準
~~~~~~~~~~~

Limelight 子系統使用 PID 控制器實現目標追蹤：

.. code-block:: java

   public class Limelight_Left extends SubsystemBase {
       private final PIDController xController, yController, rotController;

       public Limelight_Left() {
           xController = new PIDController(0.01, 0, 0.0);
           yController = new PIDController(0.03, 0, 0.0);
           rotController = new PIDController(0.01, 0, 0);
       }

       public double xOut() {
           return xController.calculate(tx, 0);  // tx 是目標的水平偏移
       }

       public double yOut() {
           return yController.calculate(ty, 0);  // ty 是目標的垂直偏移
       }

       public double rotOut() {
           return rotController.calculate(ts, 0);  // ts 是目標的傾斜角度
       }
   }

Swerve 運動學
~~~~~~~~~~~

Swerve 驅動使用運動學計算將底盤速度轉換為輪子狀態：

.. code-block:: java

   public void drive(double xSpeed, double ySpeed, double rot, boolean fieldRelative) {
       ChassisSpeeds chassisSpeeds;

       if (fieldRelative) {
           chassisSpeeds = ChassisSpeeds.fromFieldRelativeSpeeds(
               xSpeed, ySpeed, rot, getRotation2d());
       } else {
           chassisSpeeds = new ChassisSpeeds(xSpeed, ySpeed, rot);
       }

       // 使用運動學將底盤速度轉換為輪子狀態
       SwerveModuleState[] moduleStates = kinematics.toSwerveModuleStates(chassisSpeeds);

       // 優化輪子角度以減少不必要的旋轉
       SwerveDriveKinematics.desaturateWheelSpeeds(moduleStates, DriveConstants.kTeleDriveMaxSpeedMeterPerSec);

       setModuleStates(moduleStates);
   }

PathPlanner 整合
~~~~~~~~~~~~~~~

專案整合了 PathPlanner 進行自動路徑規劃：

.. code-block:: java

   // Choreo 路徑載入
   private final Optional<Trajectory<SwerveSample>> trajectory = Choreo.loadTrajectory("New Path");

   public void followTrajectory(SwerveSample sample) {
       // 使用 Choreo 的樣本來控制機器人
       Pose2d pose = sample.getPose();
       ChassisSpeeds speeds = sample.getChassisSpeeds();

       drive(speeds.vxMetersPerSecond,
             speeds.vyMetersPerSecond,
             speeds.omegaRadiansPerSecond,
             false);  // 機器人相對座標
   }

調校建議
~~~~~~~~

1. **PID 參數調校**：
   - 從 P 項開始，逐步增加直到出現振盪
   - 添加少量 D 項抑制振盪
   - 謹慎使用 I 項，避免積分飽和

2. **視覺瞄準調校**：
   - 調整 PID 增益使瞄準平滑但不過慢
   - 考慮目標距離對控制響應的影響
   - 測試不同光照條件下的穩定性

3. **運動學優化**：
   - 確保輪子位置測量準確
   - 定期檢查輪子角度偏移校正
   - 優化最大速度限制以獲得最佳性能

這個專案展示了 FRC 機器人控制的基本模式，為進一步的高階控制技術奠定了基礎。