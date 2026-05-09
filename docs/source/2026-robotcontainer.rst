RobotContainer.java 介紹
======================

`RobotContainer` 是這個專案的控制中心。它負責：

- 建立 `CommandXboxController` 操作介面
- 建立 `CommandSwerveDrivetrain` 與 `superstructure`
- 建立 `PhotonVision` 與 `AutoAlign`
- 設定預設驅動命令與按鍵綁定
- 建立 `AutoChooser` 與 SmartDashboard 選項
- 啟動 `FollowPathCommand.warmupCommand()` 以提前準備路徑追隨

駕駛控制與按鍵對應
~~~~~~~~~~~~~~~~~~~~

- `drivetrain.setDefaultCommand(...)`：讀取操縱桿數值並將其轉換成速度請求
- `joystick.leftTrigger()` 與 `joystick.rightTrigger()`：分別啟用進料與發射命令
- `joystick.povDown()` / `joystick.povUp()`：控制爬升相關命令
- `controller.b()` / `controller.a()`：切換射手角度設定
- `RobotModeTriggers.disabled()`：在停用時讓驅動系統保持空閒

程式碼輔助
~~~~~~~~~~

以下是 RobotContainer.java 的關鍵程式碼片段：

.. code-block:: java

   public class RobotContainer {

     private final CommandXboxController joystick = new CommandXboxController(0);
     private final CommandSwerveDrivetrain drivetrain = TunerConstants.createDrivetrain();
     private final superstructure superstructure = new superstructure(shooter, intake, hopper, led, autoAlign, climber);
     private final AutoChooser autoChooser;

     public RobotContainer() {
       this.autoChooser = new AutoChooser(drivetrain, superstructure, robotStatus);
       configureBindings();
     }

     private void configureBindings() {
       drivetrain.setDefaultCommand(
           drivetrain.applyRequest(() -> {
             boolean slowMode = joystick.getLeftTriggerAxis() > 0.3 && joystick.getRightTriggerAxis() > 0.3;
             double translationMultiplier = slowMode ? 0.5 : 1.0;
             return drive
                 .withVelocityX(-joystick.getLeftY() * MaxTeleOpSpeed)
                 .withVelocityY(-joystick.getLeftX() * MaxTeleOpSpeed)
                 .withRotationalRate(-joystick.getRightX() * MaxAngularRate);
           }));

       joystick.leftTrigger().whileTrue((superstructure.intake()))
           .onFalse(superstructure.stopintake());
       joystick.rightTrigger().whileTrue(this.superstructure.shootCommand())
           .onFalse(this.superstructure.stopShoot());
     }

   }

這個類別展示了複雜的子系統整合和多控制器按鍵綁定。