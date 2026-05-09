RobotContainer.java 介紹
======================

`RobotContainer` 負責建構子系統、設定預設命令及按鍵綁定。
在本範例中：

- `SwerveSubsystem` 被設為預設命令 `SwerveControlCmd`
- `ArmControl` 管理按鍵與機械臂動作
- `Limelight_Right` / `Limelight_Left` 提供目標對齊輸入
- `Driver` 封裝搖桿按鈕與軸值輸入

按鍵範例
~~~~~~~~

- `driver.zeroHeading()`：按鈕觸發後重置全向輪朝向與里程計
- `driver.changeMode()`：切換機械臂模式（例如 Coral / Algae）
- `driver.LeftTrigger()` / `driver.RightTrigger()`：分別執行進料與發射命令
- `driver.LBumper()` / `driver.RBumper()`：啟用左右 Limelight 對齊驅動

程式碼輔助
~~~~~~~~~~

以下是 RobotContainer.java 的關鍵程式碼片段：

.. code-block:: java

   public class RobotContainer {

     private final SwerveSubsystem swerveSubsystem = new SwerveSubsystem();
     private final ArmControl arm = new ArmControl(pivot, elevator, hand);
     private final Limelight_Right alignL = new Limelight_Right();
     private final Limelight_Left alignR = new Limelight_Left();
     private final Driver driver = new Driver();

     public RobotContainer() {
       swerveSubsystem.setDefaultCommand(new SwerveControlCmd(
           swerveSubsystem,
           () -> -driver.getLeftY(),
           () -> driver.getLeftX(),
           () -> driver.getRightX(),
           () -> true));
       configureBindings();
     }

     private void configureBindings() {
       driver.zeroHeading().onTrue(
           new InstantCommand(() -> swerveSubsystem.zeroHeading())
               .andThen(new InstantCommand(
                   () -> swerveSubsystem.resetOdometry(
                       new Pose2d(0, 0, swerveSubsystem.getRotation2d())))));

       driver.changeMode().onTrue(new InstantCommand(() -> arm.ChangeMode()));

       // Arm Control
       driver.a().whileTrue(arm.ButtonA()).onFalse(arm.AReleased());
       // ... 其他按鍵綁定
     }

   }

這個類別展示了如何組織子系統和按鍵綁定，以及預設命令的設定。