Robot.java 介紹
===============

此專案的 `Robot` 類別繼承 `LoggedRobot`，這表示它支援 WPILib 記錄框架。
主要工作包括：

- 以 `Logger.recordMetadata()` 記錄專案資訊
- 若真實機器人則新增 `WPILOGWriter` 與 `NT4Publisher`
- 若模擬則使用 `NT4Publisher`
- 在 `robotInit()` 設定本地路徑搜尋器 `LocalADStarAK`
- 在 `robotPeriodic()` 更新回放/記錄與命令排程器

這份程式碼同時支援比賽時常見的 `autonomousInit()`、`teleopInit()` 與 `testInit()`。

程式碼輔助
~~~~~~~~~~

以下是 Robot.java 的關鍵程式碼片段：

.. code-block:: java

   public class Robot extends LoggedRobot {

     private final HootAutoReplay m_timeAndJoystickReplay = new HootAutoReplay()
             .withTimestampReplay()
             .withJoystickReplay();

     public Robot() {
       Logger.recordMetadata("ProjectName", "NIMA");

       if (Robot.isReal()) {
           Logger.addDataReceiver(new WPILOGWriter());
           Logger.addDataReceiver(new NT4Publisher());
       } else {
           Logger.addDataReceiver(new NT4Publisher());
       }

       Logger.start();
       m_robotContainer = new RobotContainer();
     }

     @Override
     public void robotInit() {
       Pathfinding.setPathfinder(new LocalADStarAK());
     }

     @Override
     public void robotPeriodic() {
       m_timeAndJoystickReplay.update();
       CommandScheduler.getInstance().run();
     }

   }

這個類別展示了 LoggedRobot 的基本設置，以及高階記錄功能的整合。