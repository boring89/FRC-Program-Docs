AutoChooser 自動程式選擇器
========================

`AutoChooser` 使用多個 `SendableChooser`，讓隊伍可以在 Driver Station 上選擇：

- 起始位置：Left / Center / Right
- 是否走 Center 路徑
- 是否執行爬升結束動作
- 是否使用特定展示路徑

當起始位置選擇為 `None` 時，程式會自動比較當前機器人位姿與預定起點，根據距離選擇最近起點。

AutoChooser 的實作亮點：

- 使用 `NamedCommands.registerCommand(...)` 註冊自定義命令，方便路徑中的動作呼叫
- 以 `PathPlannerAuto` 載入路徑檔案
- 透過 `Commands.sequence(start, end)` 組合起始與結束路徑
- 使用 `Commands.none()` 作為預設空命令，避免空值錯誤

程式碼輔助
~~~~~~~~~~

以下是 AutoChooser.java 的關鍵程式碼片段：

.. code-block:: java

   public class AutoChooser {

     public final SendableChooser<AutoStart> AutoStartChooser = new SendableChooser<>();
     public final SendableChooser<IfGoCenter> IfGoCenterChooser = new SendableChooser<>();
     public final SendableChooser<IfGoclimb> IfGoClimbChooser = new SendableChooser<>();

     public AutoChooser(CommandSwerveDrivetrain drive, superstructure superstructure, RobotStatus robotStatus) {
       this.configureAutoChoosers();
       this.SetNamedCommands();
     }

     public void SetNamedCommands() {
       NamedCommands.registerCommand("intakeDown", superstructure.intake());
       NamedCommands.registerCommand("shoot", superstructure.autoshooter().withTimeout(2.0));
       NamedCommands.registerCommand("stopshoot", superstructure.stopShoot());
     }

     public Command auto() {
       AutoStart startPose = AutoStartChooser.getSelected();
       IfGoCenter ifGoCenter = IfGoCenterChooser.getSelected();
       IfGoclimb ifGoclimb = IfGoClimbChooser.getSelected();

       if (startPose == AutoStart.NONE) {
         Pose2d currentPose = this.drive.getPose2d();
         // 計算距離並選擇最近起點
         double distLeft = currentPose.getTranslation().getDistance(leftStart.getTranslation());
         // ... 比較邏輯
       }

       Command start = Commands.none();
       switch (startPose) {
         case LEFT:
           start = (ifGoCenter == IfGoCenter.GO_CENTER) ? new PathPlannerAuto("Left_center_deploy")
                   : new PathPlannerAuto("Left_Deploy");
           break;
         // ... 其他起點
       }

       Command end = Commands.none();
       switch (ifGoclimb) {
         case climb:
           // 根據起點選擇結束路徑
           break;
         // ... 其他結束邏輯
       }
       return Commands.sequence(start, end);
     }

   }

這個類別展示了複雜的自動程式選擇邏輯和路徑組合。