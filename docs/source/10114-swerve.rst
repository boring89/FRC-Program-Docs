SwerveControlCmd 範例
====================

`SwerveControlCmd` 是驅動預設命令，它負責：

1. 從操縱桿讀取前後、左右與轉向速度
2. 套用死區值，避免微小輸入造成車體晃動
3. 將速度值縮放成實際最大速率
4. 決定場地相對或機器相對控制
5. 將速度轉換成每個全向輪的目標狀態

其中，`fieldOrientedFunc.get()` 決定是否使用場地座標系；如果啟用，機器人方向不受自身朝向影響。

程式碼輔助
~~~~~~~~~~

以下是 SwerveControlCmd.java 的關鍵程式碼片段：

.. code-block:: java

   public class SwerveControlCmd extends Command {

     private final SwerveSubsystem swerveSubsystem;
     private final Supplier<Double> xSpdFunc, ySpdFunc, turningSpdFunc;
     private final Supplier<Boolean> fieldOrientedFunc;

     public SwerveControlCmd(SwerveSubsystem swerveSubsystem,
             Supplier<Double> xSpdFunc, Supplier<Double> ySpdFunc, Supplier<Double> turningSpdFunc,
             Supplier<Boolean> fieldOrientedFunc) {
         this.swerveSubsystem = swerveSubsystem;
         this.xSpdFunc = xSpdFunc;
         this.ySpdFunc = ySpdFunc;
         this.turningSpdFunc = turningSpdFunc;
         this.fieldOrientedFunc = fieldOrientedFunc;
         addRequirements(swerveSubsystem);
     }

     @Override
     public void execute() {
         double xSpd = xSpdFunc.get();
         double ySpd = ySpdFunc.get();
         double turningSpd = turningSpdFunc.get();

         // 套用死區
         xSpd = Math.abs(xSpd) > OIConstants.kDeadband ? xSpd : 0.0;
         ySpd = Math.abs(ySpd) > OIConstants.kDeadband ? ySpd : 0.0;
         turningSpd = Math.abs(turningSpd) > OIConstants.kDeadband ? turningSpd : 0.0;

         // 縮放速度
         xSpd = xSpd * DriveConstants.kTeleDriveMaxSpeedMeterPerSec;
         ySpd = ySpd * DriveConstants.kTeleDriveMaxSpeedMeterPerSec;
         turningSpd = turningSpd * DriveConstants.kTeleDriveMaxAngularSpeedRadiansPerSec;

         if (fieldOrientedFunc.get()) {
             this.swerveSubsystem.drive(xSpd, ySpd, turningSpd, true);
         } else {
             ChassisSpeeds chassisSpeeds = new ChassisSpeeds(xSpd, ySpd, turningSpd);
             SwerveModuleState[] moduleStates = DriveConstants.kDriveKinematics.toSwerveModuleStates(chassisSpeeds);
             swerveSubsystem.setModuleStates(moduleStates);
         }
     }

   }

這個命令展示了 Swerve 驅動的基本控制邏輯，包括輸入處理、死區應用和運動學轉換。