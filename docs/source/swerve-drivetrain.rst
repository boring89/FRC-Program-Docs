建立 Drivetrain 子系統
====================

Drivetrain 是主要的驅動系統，整合所有 SwerveModule 並處理高階控制。它負責將高層次的運動命令轉換為每個輪子的具體動作。

系統架構
--------

Drivetrain 子系統包含以下主要組件：

- **4 個 SwerveModule**：實際的輪子控制單元
- **運動學計算器**：將機器人速度轉換為輪子速度
- **姿態估計器**：追蹤機器人在場地上的位置
- **陀螺儀**：測量機器人的旋轉角度
- **速度限制器**：提供平滑的控制體驗

建立 Drivetrain.java - 主要驅動系統
-----------------------------------

.. code-block:: java

   package frc.robot.subsystems.Drivetrain;

   import com.pathplanner.lib.auto.AutoBuilder;
   import com.pathplanner.lib.config.PIDConstants;
   import com.pathplanner.lib.config.RobotConfig;
   import com.pathplanner.lib.controllers.PPHolonomicDriveController;
   import com.studica.frc.AHRS;
   import com.studica.frc.AHRS.NavXComType;

   import edu.wpi.first.math.Matrix;
   import edu.wpi.first.math.estimator.SwerveDrivePoseEstimator;
   import edu.wpi.first.math.filter.SlewRateLimiter;
   import edu.wpi.first.math.geometry.Pose2d;
   import edu.wpi.first.math.geometry.Rotation2d;
   import edu.wpi.first.math.kinematics.ChassisSpeeds;
   import edu.wpi.first.math.kinematics.SwerveDriveKinematics;
   import edu.wpi.first.math.kinematics.SwerveModulePosition;
   import edu.wpi.first.math.kinematics.SwerveModuleState;
   import edu.wpi.first.math.numbers.N1;
   import edu.wpi.first.math.numbers.N3;
   import edu.wpi.first.wpilibj.DriverStation;
   import edu.wpi.first.wpilibj2.command.Command;
   import edu.wpi.first.wpilibj2.command.SubsystemBase;
   import frc.robot.Constants.DrivetrainConstants;

   public class Drivetrain extends SubsystemBase {

       // ===== 4 個 Swerve 模組 =====
       private final SwerveModule frontLeft, frontRight, backLeft, backRight;

       // ===== 運動學和估計 =====
       private final SwerveDriveKinematics kinematics;        // 運動學計算
       private final SwerveDrivePoseEstimator poseEstimator;  // 姿態估計器

       // ===== 感測器 =====
       private final AHRS gyro;  // 陀螺儀（測量旋轉）

       // ===== 控制 =====
       private final SlewRateLimiter xLimiter, yLimiter, rotLimiter;  // 速度限制器
       private double MaxDriveSpeed = DrivetrainConstants.kTeleOpSpeedMetersPerSecond;  // 當前最大速度

**建構函式 - 初始化整個驅動系統**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public Drivetrain() {
           // ===== 初始化 4 個 Swerve 模組 =====
           this.frontLeft = new SwerveModule(
                   DrivetrainConstants.kFrontLeftModuleIDs[0],
                   DrivetrainConstants.kFrontLeftModuleIDs[1],
                   DrivetrainConstants.kFrontLeftModuleIDs[2],
                   DrivetrainConstants.kFrontLeftModuleInverted[0],
                   DrivetrainConstants.kFrontLeftModuleInverted[1]);
           this.frontRight = new SwerveModule(
                   DrivetrainConstants.kFrontRightModuleIDs[0],
                   DrivetrainConstants.kFrontRightModuleIDs[1],
                   DrivetrainConstants.kFrontRightModuleIDs[2],
                   DrivetrainConstants.kFrontRightModuleInverted[0],
                   DrivetrainConstants.kFrontRightModuleInverted[1]);
           this.backLeft = new SwerveModule(
                   DrivetrainConstants.kBackLeftModuleIDs[0],
                   DrivetrainConstants.kBackLeftModuleIDs[1],
                   DrivetrainConstants.kBackLeftModuleIDs[2],
                   DrivetrainConstants.kBackLeftModuleInverted[0],
                   DrivetrainConstants.kBackLeftModuleInverted[1]);
           this.backRight = new SwerveModule(
                   DrivetrainConstants.kBackRightModuleIDs[0],
                   DrivetrainConstants.kBackRightModuleIDs[1],
                   DrivetrainConstants.kBackRightModuleIDs[2],
                   DrivetrainConstants.kBackRightModuleInverted[0],
                   DrivetrainConstants.kBackRightModuleInverted[1]);

           // ===== 初始化陀螺儀 =====
           this.gyro = new AHRS(NavXComType.kMXP_SPI);

           // ===== 建立運動學模型 =====
           // 這告訴 WPILib 輪子在機器人上的位置
           this.kinematics = new SwerveDriveKinematics(
                   DrivetrainConstants.moduleLocations);

           // ===== 初始化姿態估計器 =====
           // 用於追蹤機器人在場地上的位置
           this.poseEstimator = new SwerveDrivePoseEstimator(
                   kinematics,
                   this.getRotation2d(),           // 當前角度
                   this.getModulePositions(),      // 當前輪子位置
                   Pose2d.kZero);                  // 起始位置

           // ===== 初始化速度限制器 =====
           // 防止突然的加速度變化
           this.xLimiter = new SlewRateLimiter(DrivetrainConstants.kTeleOpDrivePositiveSlewRate);
           this.yLimiter = new SlewRateLimiter(DrivetrainConstants.kTeleOpDrivePositiveSlewRate);
           this.rotLimiter = new SlewRateLimiter(DrivetrainConstants.kTeleOpDrivePositiveSlewRate);

           // ===== 配置自動程式 =====
           AutoBuilderConfigure();
       }

**感測器方法 - 讀取陀螺儀和位置**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       // 獲取當前朝向（度）
       public double getHeading() {
           return -gyro.getAngle();  // 負號用於方向校正
       }

       // 歸零陀螺儀
       public void zeroHeading() {
           gyro.reset();
       }

       // 獲取旋轉角度（Rotation2d 格式）
       public Rotation2d getRotation2d() {
           return Rotation2d.fromDegrees(getHeading());
       }

**模組狀態方法 - 獲取所有輪子的狀態**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       // 獲取所有輪子的位置
       public SwerveModulePosition[] getModulePositions() {
           return new SwerveModulePosition[] {
                   this.frontLeft.getPosition(),
                   this.frontRight.getPosition(),
                   this.backLeft.getPosition(),
                   this.backRight.getPosition()
           };
       }

       // 獲取所有輪子的狀態
       public SwerveModuleState[] getModuleStates() {
           return new SwerveModuleState[] {
                   this.frontLeft.getState(),
                   this.frontRight.getState(),
                   this.backLeft.getState(),
                   this.backRight.getState()
           };
       }

       // 計算機器人相對速度
       public ChassisSpeeds getRobotRelativeSpeeds() {
           return this.kinematics.toChassisSpeeds(this.getModuleStates());
       }

**姿態估計方法 - 追蹤機器人位置**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       // 獲取估計位置
       public Pose2d getPose() {
           return this.poseEstimator.getEstimatedPosition();
       }

       // 重置位置
       public void resetPose(Pose2d pose) {
           this.poseEstimator.resetPose(pose);
       }

       // 添加視覺測量（用於融合視覺和編碼器數據）
       public void addVisionMeasurement(Pose2d visionPose, double timestamp, Matrix<N3, N1> stdDevMeters) {
           this.poseEstimator.addVisionMeasurement(visionPose, timestamp, stdDevMeters);
       }

**核心驅動方法 - 控制機器人運動**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public void drive(ChassisSpeeds robotRelativeSpeeds) {
           // 離散化速度 - 使控制更穩定
           ChassisSpeeds optimizedSpeeds = ChassisSpeeds.discretize(robotRelativeSpeeds, 0.02);

           // 將機器人速度轉換為每個輪子的目標狀態
           var states = kinematics.toSwerveModuleStates(optimizedSpeeds);

           // 限制輪子速度，防止超出最大速度
           SwerveDriveKinematics.desaturateWheelSpeeds(
                   states, DrivetrainConstants.kMaxSpeedMetersPerSecond);

           // 設定每個輪子的目標狀態
           this.frontLeft.setState(states[0]);
           this.frontRight.setState(states[1]);
           this.backLeft.setState(states[2]);
           this.backRight.setState(states[3]);
       }

**遙控操作方法 - 處理搖桿輸入**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public void teleOpDrive(double Xinput, double Yinput, double Rotinput) {
           // 應用速度變化率限制
           Xinput = this.xLimiter.calculate(Xinput);
           Yinput = this.yLimiter.calculate(Yinput);
           Rotinput = this.rotLimiter.calculate(Rotinput);

           // 建立場地相對速度
           // 這意味著前進方向永遠是場地上的"前"，不管機器人朝向如何
           ChassisSpeeds fieldRelativeSpeeds = new ChassisSpeeds(
                   Xinput * MaxDriveSpeed,                    // X 方向速度
                   Yinput * MaxDriveSpeed,                    // Y 方向速度
                   Rotinput * DrivetrainConstants.kMaxAngularSpeedRadiansPerSecond  // 旋轉速度
           );

           // 轉換為機器人相對速度
           ChassisSpeeds robotRelativeSpeeds = ChassisSpeeds.fromFieldRelativeSpeeds(
                   fieldRelativeSpeeds,
                   getRotation2d()  // 當前機器人朝向
           );

           // 執行運動
           this.drive(robotRelativeSpeeds);
       }

**速度模式切換 - 全速/半速模式**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public void fullSpeedMode() {
           this.MaxDriveSpeed = DrivetrainConstants.kMaxSpeedMetersPerSecond;
       }

       public void halfSpeedMode() {
           this.MaxDriveSpeed = DrivetrainConstants.kTeleOpSpeedMetersPerSecond;
       }

**PathPlanner 自動程式配置**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public void AutoBuilderConfigure() {
           RobotConfig config = null;
           try {
               // 從 PathPlanner GUI 載入配置
               config = RobotConfig.fromGUISettings();
           } catch (Exception e) {
               e.printStackTrace();
           }

           // 配置 AutoBuilder 用於自動路徑
           AutoBuilder.configure(
                   this::getPose,           // 獲取位置的方法
                   this::resetPose,         // 重置位置的方法
                   this::getRobotRelativeSpeeds,  // 獲取速度的方法
                   (speeds, feedforwards) -> drive(speeds),  // 驅動方法
                   new PPHolonomicDriveController(  // 全向運動控制器
                           new PIDConstants(5.0, 0.0, 0.0),  // X 方向 PID
                           new PIDConstants(5.0, 0.0, 0.0),  // Y 方向 PID
                           new PIDConstants(5.0, 0.0, 0.0)), // 旋轉 PID
                   config,
                   () -> {
                       // 根據聯盟顏色決定路徑方向
                       var alliance = DriverStation.getAlliance();
                       if (alliance.isPresent()) {
                           return alliance.get() == DriverStation.Alliance.Red;
                       }
                       return false;
                   },
                   this);
       }

**週期性更新 - 每一個控制循環執行**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       @Override
       public void periodic() {
           // 更新姿態估計器
           this.poseEstimator.update(
                   this.getRotation2d(),
                   this.getModulePositions());
       }

**命令方法 - 建立可重用的命令**
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: java

       public Command fullSpeedCommand() {
           return runOnce(() -> fullSpeedMode());
       }

       public Command halfSpeedCommand() {
           return runOnce(() -> halfSpeedMode());
       }
   }

關鍵概念
--------

**運動學 (Kinematics)**
   將機器人的整體運動（前進、後退、旋轉）轉換為每個輪子的具體動作。

**場地相對 vs 機器人相對**
   - 場地相對：前進方向永遠是場地上的"前"
   - 機器人相對：前進方向是機器人當前的朝向

**姿態估計器**
   結合編碼器和陀螺儀數據來精確追蹤機器人在場地上的位置。

**速度離散化**
   將連續的速度命令轉換為適合數位控制的離散值。

下一步
------

現在我們已經建立了完整的 Drivetrain 子系統，接下來要建立控制命令來操作這個系統。

:doc:`swerve-commands`