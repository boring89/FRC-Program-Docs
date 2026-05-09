Shooter Calculator 算法詳解
========================

Shooter Calculator 是射手子系統的核心，負責計算射擊參數。本頁面詳細解釋其算法原理和實現。

算法概述
~~~~~~~~

Shooter Calculator 實現了先進的射擊計算：

- **運動補償**：考慮機器人移動對射擊軌跡的影響
- **延遲補償**：預測子彈飛行時間內的目標位置變化
- **查表插值**：使用預測數據進行參數查詢
- **多目標支援**：支援不同目標的射擊計算

核心概念
~~~~~~~~

1. **Phase Delay Compensation**：補償從命令發出到實際執行之間的延遲
2. **Lookahead Pose**：預測射擊時的機器人位置
3. **Iterative Solver**：迭代計算精確的瞄準角度

程式碼輔助 - 基本結構
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

   public class ShooterCalculator {
       private final InterpolatingTreeMap<Double, Angle> hoodMap;
       private final InterpolatingTreeMap<Double, AngularVelocity> rollMap;
       private final double phaseDelay = 0.03; // 30ms 延遲

       public record ShootingState(
           Rotation2d turretFieldAngle,
           Angle hoodAngle,
           AngularVelocity flywheelRPS
       ) {}

       public ShootingState calculateShootingToHub() {
           // 實現射擊計算邏輯
       }
   }

運動補償算法
~~~~~~~~~~~

算法考慮了機器人在子彈飛行期間的移動：

.. code-block:: java

   public ShootingState calculateShootingToHub() {
       // 1. 獲取當前狀態
       Pose2d estimatedPose = drive.getPose2d();
       ChassisSpeeds robotVelocity = drive.getFieldVelocity();

       // 2. 延遲補償 - 預測 phaseDelay 後的位置
       estimatedPose = estimatedPose.exp(new Twist2d(
           robotVelocity.vxMetersPerSecond * phaseDelay,
           robotVelocity.vyMetersPerSecond * phaseDelay,
           robotVelocity.omegaRadiansPerSecond * phaseDelay
       ));

       // 3. 計算砲塔位置
       Pose2d turretPosition = estimatedPose.transformBy(
           new Transform2d(robotToTurret.getTranslation().toTranslation2d(),
                          robotToTurret.getRotation().toRotation2d())
       );

       // 4. 計算砲塔相對速度 (包含旋轉效應)
       double turretVelocityX = robotVelocity.vxMetersPerSecond
           + robotVelocity.omegaRadiansPerSecond
           * (robotToTurret.getY() * Math.cos(robotAngle)
              - robotToTurret.getX() * Math.sin(robotAngle));

       double turretVelocityY = robotVelocity.vyMetersPerSecond
           + robotVelocity.omegaRadiansPerSecond
           * (robotToTurret.getX() * Math.cos(robotAngle)
              - robotToTurret.getY() * Math.sin(robotAngle));

       // 5. 迭代求解 Lookahead Pose
       return calculateWithLookahead(turretPosition, turretVelocityX, turretVelocityY);
   }

迭代求解器
~~~~~~~~~~

使用迭代方法計算精確的瞄準點：

.. code-block:: java

   private ShootingState calculateWithLookahead(Pose2d turretPosition,
                                               double turretVelX, double turretVelY) {
       double timeOfFlight = 0.0;
       Pose2d lookaheadPose = turretPosition;
       double distance = turretPosition.getTranslation().getDistance(target);

       // 迭代 5 次以收斂
       for (int i = 0; i < 5; i++) {
           timeOfFlight = timeOfFlightMap.get(distance);

           double offsetX = turretVelX * timeOfFlight;
           double offsetY = turretVelY * timeOfFlight;

           lookaheadPose = new Pose2d(
               turretPosition.getTranslation().plus(new Translation2d(offsetX, offsetY)),
               turretPosition.getRotation()
           );

           distance = lookaheadPose.getTranslation().getDistance(target);
       }

       // 計算最終瞄準角度
       Translation2d vectorToTarget = target.minus(lookaheadPose.getTranslation());
       Rotation2d targetFieldAngle = vectorToTarget.getAngle();

       return new ShootingState(
           targetFieldAngle,
           hoodMap.get(distance),
           rollMap.get(distance)
       );
   }

查表插值系統
~~~~~~~~~~~

使用 InterpolatingTreeMap 進行參數查表：

.. code-block:: java

   public ShooterCalculator(CommandSwerveDrivetrain drive, RobotStatus robotStatus) {
       // 初始化 Hood 角度查表
       hoodMap = new InterpolatingTreeMap<>(
           InverseInterpolator.forDouble(),
           (start, end, t) -> {
               double startDeg = start.in(Degree);
               double endDeg = end.in(Degree);
               double interpolated = MathUtil.interpolate(startDeg, endDeg, t);
               return Degree.of(interpolated);
           });

       // 初始化 Flywheel 速度查表
       rollMap = new InterpolatingTreeMap<>(
           InverseInterpolator.forDouble(),
           (start, end, t) -> {
               double startRPS = start.in(RotationsPerSecond);
               double endRPS = end.in(RotationsPerSecond);
               double interpolated = MathUtil.interpolate(startRPS, endRPS, t);
               return RotationsPerSecond.of(interpolated);
           });

       // 添加測試數據點
       rollMap.put(0.796222, RotationsPerSecond.of(32.3));
       rollMap.put(1.545207, RotationsPerSecond.of(33.3));
       // ... 更多數據點

       hoodMap.put(0.796222, Degree.of(27.0));
       hoodMap.put(1.545207, Degree.of(32.0));
       // ... 更多數據點
   }

多目標支援
~~~~~~~~~~

支援不同區域的射擊目標：

.. code-block:: java

   public ShootingState calculateShootingToAlliance() {
       // 根據區域選擇目標
       Translation2d target;
       if (robotStatus.getVerticalSide() == RobotStatus.VerticalSide.TOP) {
           target = AllianceFlipUtil.apply(siteConstants.topLeftCenterPoint.toTranslation2d());
       } else {
           target = AllianceFlipUtil.apply(siteConstants.topRightCenterPoint.toTranslation2d());
       }

       // 使用不同的查表進行計算
       return new ShootingState(
           targetFieldAngle,
           Hood_MAX_RADS,  // 聯盟射擊使用固定 Hood 角度
           ToAillancerollMap.get(lookaheadDistance)
       );
   }

數據收集與調校
~~~~~~~~~~~~~

射手參數需要通過測試來確定：

1. **距離測量**：記錄不同距離的成功射擊參數
2. **數據記錄**：使用 Logger 記錄實際參數
3. **插值優化**：調整查表數據點以獲得更好的準確度

程式碼輔助 - 數據記錄
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: java

   @Override
   public void periodic() {
       Logger.recordOutput("shooter/targetDistance", currentTargetDistance);
       Logger.recordOutput("shooter/hoodAngle", hoodAngle.in(Degrees));
       Logger.recordOutput("shooter/flywheelRPS", flywheelRPS.in(RotationsPerSecond));
       Logger.recordOutput("shooter/turretAngle", turretAngle.getDegrees());
   }

性能優化
~~~~~~~~

算法的關鍵優化點：

- **迭代次數**：5 次迭代通常足夠收斂
- **延遲補償**：精確測量系統延遲時間
- **查表密度**：在關鍵距離範圍增加數據點密度
- **實時性能**：確保計算在單個控制週期內完成

故障處理
~~~~~~~~

處理邊界情況和異常：

.. code-block:: java

   public ShootingState calculateShootingToHub() {
       try {
           // 主要計算邏輯
           return calculateWithLookahead(turretPosition, turretVelX, turretVelY);
       } catch (Exception e) {
           // 故障時返回安全預設值
           Logger.recordOutput("shooter/error", e.getMessage());
           return new ShootingState(
               Rotation2d.fromDegrees(0),
               Degree.of(25),  // 安全角度
               RotationsPerSecond.of(30)  // 安全速度
           );
       }
   }

這個算法代表了現代 FRC 射手系統的先進實現，結合了運動學、控制理論和實時計算技術。