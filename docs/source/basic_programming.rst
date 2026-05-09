Programming Guide
=================

本章節介紹 FRC 使用的 WPILib Java 程式架構，並解釋常見語法、TimedRobot 範例、第三方函式庫管理，以及 CTRE Phoenix 6 / REVlib 的基本用法。

WPILib Java 是什麼？
-------------------

WPILib 是 FIRST 官方提供的機器人控制程式庫。它幫助你：

- 控制馬達、編碼器、感測器和其他硬體
- 撰寫比賽模式（自動、遙控）程式
- 與 FRC Driver Station 和網路通訊

Java 是 FRC 支援的語言之一，適合已經熟悉物件導向概念的隊伍。

Java 基礎與常見語法
------------------

如果你是門外漢，先認識這些基本概念：

- `class`: Java 的主要程式單位，例如 `Robot` 或 `Shooter`。
- `method`: 函式或程序，例如 `robotInit()`、`teleopPeriodic()`。
- `import`: 載入外部程式庫，例如 `import edu.wpi.first.wpilibj.TimedRobot;`。
- `package`: 組織程式碼的資料夾結構。
- `new`: 建立物件實例，例如 `new CANSparkMax(1, MotorType.kBrushless);`。

以下是最簡單的 Java 程式碼範例：

.. code-block:: java

   public class Example {
       public static void main(String[] args) {
           System.out.println("Hello, FRC!");
       }
   }

TimedRobot 架構與寫法
---------------------

大多數 FRC Java 專案使用 `TimedRobot`，它會每 20 毫秒呼叫一次週期函式。常見的類別與方法：

- `robotInit()`: 機器人啟動時執行一次。
- `autonomousInit()`: 自動模式開始時執行一次。
- `autonomousPeriodic()`: 自動模式每週期執行一次。
- `teleopInit()`: 遙控模式開始時執行一次。
- `teleopPeriodic()`: 遙控模式每週期執行一次。
- `disabledInit()` / `disabledPeriodic()`: 禁用時執行。

這種架構讓你可以把初始化、單次設定和每次更新的邏輯分開。

範例：基本 TimedRobot
----------------------

下面的範例展示一個最簡單的 `TimedRobot` 類別：

.. code-block:: java

   package frc.robot;

   import edu.wpi.first.wpilibj.TimedRobot;
   import edu.wpi.first.wpilibj.motorcontrol.PWMSparkMax;

   public class Robot extends TimedRobot {
       private PWMSparkMax motor = new PWMSparkMax(0);

       @Override
       public void robotInit() {
           System.out.println("Robot initialized.");
       }

       @Override
       public void teleopPeriodic() {
           motor.set(0.5); // 以 50% 速度運轉馬達
       }
   }

新增第三方函式庫
----------------

FRC Java 專案使用 Gradle 管理相依性，必要時可以在 `build.gradle` 中加入第三方函式庫。例如：

.. code-block:: groovy

   dependencies {
       implementation "com.ctre.phoenix:phoenix:6.0.0"
       implementation "com.revrobotics:rev-hub:1.0.0"
   }

使用步驟如下：

1. 在 `build.gradle` 的 `dependencies` 區段新增相依性。
2. 儲存檔案後，Gradle 會重新同步。
3. 在 Java 檔中加入對應 `import`。

常見函式庫與用途
-----------------

CTRE Phoenix 6
~~~~~~~~~~~~~~~

CTRE Phoenix 是控制 CTRE 系列馬達控制器（如 Talon FX、Victor SPX）最常用的函式庫。Phoenix 6 為新版 API，寫法較簡潔。

基本使用步驟：

.. code-block:: java

   import com.ctre.phoenix.motorcontrol.can.TalonFX;
   import com.ctre.phoenix.motorcontrol.ControlMode;

   TalonFX leftMotor = new TalonFX(1);
   leftMotor.set(ControlMode.PercentOutput, 0.5);

REV Robotics
~~~~~~~~~~~~

REV 提供 CANSparkMax、SPARK MAX 控制器，並有自己的 Java API。常見用法：

.. code-block:: java

   import com.revrobotics.CANSparkMax;
   import com.revrobotics.CANSparkMaxLowLevel.MotorType;

   CANSparkMax sparkMax = new CANSparkMax(2, MotorType.kBrushless);
   sparkMax.set(0.5);

其他常見硬體庫
~~~~~~~~~~~~~~~~

- `navX`: 讀取陀螺儀與角度資料。
- `Limelight`: 計算目標追蹤與視覺定位。
- `PhotonVision`: 視覺辨識與相機處理。

如何讓門外漢看懂
----------------

如果你不是程式設計背景，建議：

- 先看 FRC Java 範例專案的 `Robot.java`。
- 了解 `robotInit()` 與 `teleopPeriodic()` 的差異。
- 從簡單的馬達控制開始，再逐漸加入感測器與自動模式。
- 使用 WPILib 官方文件查詢類別與 API。

常見語法小提示
----------------

- `;`：每行程式碼結尾必須加分號。
- `{}`：用來包住程式區塊。
- `//`：單行註解，`/* ... */`：多行註解。
- `import`：放在檔案最上方。

本章節目標是讓你理解 FRC Java 程式的基本結構，並能夠在 `TimedRobot` 中加入馬達控制與第三方函式庫。