建立控制命令
============

控制命令負責將用戶輸入轉換為對 Drivetrain 子系統的具體操作。在 Command-Based 架構中，命令是操作子系統的主要方式。

命令架構
--------

FRC 的 Command-Based 架構將機器人控制分為：

- **子系統 (Subsystem)**：控制硬體組件（如 Drivetrain）
- **命令 (Command)**：定義要執行的操作
- **觸發器 (Trigger)**：連接用戶輸入到命令

建立 TeleOpCommand.java - 遙控操作命令
--------------------------------------

TeleOpCommand 處理來自搖桿的輸入並將其轉換為驅動命令：

.. code-block:: java

   package frc.robot.commands;

   import edu.wpi.first.math.MathUtil;
   import edu.wpi.first.wpilibj2.command.Command;
   import frc.robot.subsystems.Controller.DriverJoystick;
   import frc.robot.subsystems.Drivetrain.Drivetrain;

   public class TeleOpCommand extends Command {

       private final Drivetrain drivetrain;
       private final DriverJoystick driverJoystick;

       public TeleOpCommand(Drivetrain drivetrain, DriverJoystick driverJoystick) {
           this.drivetrain = drivetrain;
           this.driverJoystick = driverJoystick;
           // 聲明這個命令需要使用 drivetrain
           addRequirements(drivetrain);
       }

       @Override
       public void execute() {
           // ===== 讀取搖桿輸入並應用死區 =====
           // 死區防止小幅度的搖桿抖動造成機器人移動
           double xSpeed = MathUtil.applyDeadband(
               -driverJoystick.getLeftY(),  // 左搖桿 Y 軸（前後移動）
               0.05);                       // 死區大小（5%）

           double ySpeed = MathUtil.applyDeadband(
               -driverJoystick.getLeftX(),  // 左搖桿 X 軸（左右移動）
               0.05);

           double rot = MathUtil.applyDeadband(
               -driverJoystick.getRightX(), // 右搖桿 X 軸（旋轉）
               0.05);

           // ===== 將輸入傳送給驅動系統 =====
           drivetrain.teleOpDrive(xSpeed, ySpeed, rot);
       }

       // 這個命令永遠不會結束，除非被中斷
       // @Override
       // public boolean isFinished() {
       //     return false;
       // }
   }

建立 DriverJoystick.java - 搖桿控制器
-------------------------------------

DriverJoystick 擴展了 XboxController，添加了自定義的按鈕觸發器：

.. code-block:: java

   package frc.robot.subsystems.Controller;

   import edu.wpi.first.wpilibj.XboxController;
   import edu.wpi.first.wpilibj2.command.button.Trigger;

   public class DriverJoystick extends XboxController {

       public DriverJoystick(int port) {
           super(port);  // 指定搖桿連接的 USB 埠
       }

       // ===== 按鈕觸發器 =====
       // B 按鈕用於歸零機器人朝向
       public Trigger zeroHeading() {
           return new Trigger(this::getBButton);
       }

       // 右肩按鈕用於切換全速模式
       public Trigger fullSpeedMode() {
           return new Trigger(this::getRightBumperButton);
       }
   }

搖桿控制說明
------------

**Xbox 控制器佈局：**

- **左搖桿**：控制機器人的 X/Y 方向移動
  - Y 軸（上/下）：前進/後退
  - X 軸（左/右）：左右平移

- **右搖桿**：控制機器人旋轉
  - X 軸（左/右）：順時針/逆時針旋轉

- **按鈕控制**：
  - B 按鈕：歸零陀螺儀（重置場地朝向）
  - 右肩按鈕：切換全速/半速模式

**死區 (Deadband)**
   防止搖桿的輕微抖動造成不必要的機器人移動。通常設為 5-10%。

**速度縮放**
   將搖桿輸入（-1 到 1）縮放到實際速度範圍。

下一步
------

現在我們已經建立了控制命令，接下來要將所有組件整合到 RobotContainer 中。

:doc:`swerve-integration`