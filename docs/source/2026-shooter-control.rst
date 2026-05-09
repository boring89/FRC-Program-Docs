馬達控制與 PID 系統
==================

FRC 機器人中的馬達控制是實現精確運動的關鍵。本頁面介紹 PID 控制器、ProfiledPID 以及相關的馬達控制技術。

PID 控制器基礎
~~~~~~~~~~~~~

PID (Proportional-Integral-Derivative) 控制器是 FRC 中最常用的控制演算法：

- **P (比例項)**：根據當前誤差調整輸出，誤差越大輸出越大
- **I (積分項)**：累積過去誤差，用於消除穩態誤差
- **D (微分項)**：根據誤差變化率調整輸出，增加系統穩定性

程式碼輔助
~~~~~~~~~~

WPILib 中的 PIDController 使用範例：

.. code-block:: java

   import edu.wpi.first.math.controller.PIDController;

   public class ExampleSubsystem extends SubsystemBase {
       private final PIDController pidController = new PIDController(1.0, 0.0, 0.1);

       public void setPosition(double targetPosition) {
           double currentPosition = getCurrentPosition();
           double output = pidController.calculate(currentPosition, targetPosition);
           setMotorOutput(output);
       }
   }

ProfiledPID 控制器
~~~~~~~~~~~~~~~~~

ProfiledPID 結合了 PID 控制和運動規劃，能夠實現平滑的加速和減速：

- 限制最大速度和加速度
- 生成平滑的運動軌跡
- 避免系統振盪

程式碼輔助
~~~~~~~~~~

ProfiledPIDController 使用範例：

.. code-block:: java

   import edu.wpi.first.math.controller.ProfiledPIDController;
   import edu.wpi.first.math.trajectory.TrapezoidProfile;

   public class ArmSubsystem extends SubsystemBase {
       private final ProfiledPIDController pidController = new ProfiledPIDController(
           1.0, 0.0, 0.1,
           new TrapezoidProfile.Constraints(Units.degreesToRadians(90), Units.degreesToRadians(180))
       );

       public void setAngleGoal(double targetAngle) {
           double output = pidController.calculate(getCurrentAngle(), targetAngle);
           setMotorOutput(output);
       }
   }

TalonFX 馬達控制器
~~~~~~~~~~~~~~~~~

CTRE TalonFX 控制器提供硬體級的 PID 控制，具有更好的性能：

- 內建 PID 控制器
- 支持多種控制模式 (位置、速度、電壓等)
- 支援 Motion Magic 運動規劃
- 支援 SysId 系統識別

程式碼輔助
~~~~~~~~~~

TalonFX PID 配置範例：

.. code-block:: java

   import com.ctre.phoenix6.configs.TalonFXConfiguration;
   import com.ctre.phoenix6.controls.PositionVoltage;

   public class TurretIOTalon extends TurretIO {
       private final TalonFX turretMotor;
       private final PositionVoltage positionRequest = new PositionVoltage(0);

       public void configureMotors() {
           TalonFXConfiguration configs = new TalonFXConfiguration();

           // PID 參數配置
           configs.Slot0.kP = 42.0;  // 比例增益
           configs.Slot0.kI = 0.0;   // 積分增益
           configs.Slot0.kD = 1.5;   // 微分增益
           configs.Slot0.kS = 0.63542;  // 靜摩擦補償
           configs.Slot0.kV = 1.5255;   // 速度補償
           configs.Slot0.kA = 0.13204;  // 加速度補償

           turretMotor.getConfigurator().apply(configs);
       }

       public void setAngle(Rotation2d robotHeading, Angle targetRad, ShootState state) {
           double position = calculateTargetPosition(robotHeading, targetRad, state);
           turretMotor.setControl(positionRequest.withPosition(position));
       }
   }

旋轉砲台控制
~~~~~~~~~~~

砲台控制需要考慮機器人朝向和目標位置的相對關係：

- 將場地座標轉換為砲台相對座標
- 處理砲台角度限制和連續性
- 實現目標追蹤和預測瞄準

程式碼輔助
~~~~~~~~~~

砲台角度計算範例：

.. code-block:: java

   public double Calculate(Rotation2d robotHeading, Angle targetRad, ShootState state) {
       // 將目標角度轉換為機器人相對角度
       double robotRelativeTarget = targetRad.in(Radians) - robotHeading.getRadians();

       // 正規化角度到 [-π, π] 範圍
       robotRelativeTarget = MathUtil.angleModulus(robotRelativeTarget);

       // 根據射擊狀態調整角度
       if (state == ShootState.ACTIVE_SHOOTING) {
           // 活躍射擊時的精確控制
           return robotRelativeTarget;
       } else {
           // 追蹤模式下的平滑控制
           return smoothAngle(robotRelativeTarget);
       }
   }

系統識別 (SysId)
~~~~~~~~~~~~~~~

SysId 用於測量系統參數，優化 PID 控制：

- **動態測試**：快速變化輸入，識別系統動態響應
- **準靜態測試**：緩慢變化輸入，識別靜摩擦和效率
- 生成系統模型用於控制器調校

程式碼輔助
~~~~~~~~~~

SysId 測試範例：

.. code-block:: java

   import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;

   public class TurretIOTalon extends TurretIO {
       private final SysIdRoutine sysIdRoutine;

       public TurretIOTalon() {
           sysIdRoutine = new SysIdRoutine(
               new SysIdRoutine.Config(
                   Volts.of(0.5).per(Second),  // 斜坡速率
                   Volts.of(3),                // 測試電壓
                   null,                       // 超時時間
                   (state) -> SignalLogger.writeString("state", state.toString())
               ),
               new SysIdRoutine.Mechanism(
                   (volts) -> turretMotor.setControl(voltageRequest.withOutput(volts.in(Volts))),
                   null,
                   this  // 關聯的子系統
               )
           );
       }

       public Command sysid() {
           return Commands.sequence(
               sysIdRoutine.quasistatic(SysIdRoutine.Direction.kForward),
               sysIdRoutine.quasistatic(SysIdRoutine.Direction.kReverse),
               sysIdRoutine.dynamic(SysIdRoutine.Direction.kForward),
               sysIdRoutine.dynamic(SysIdRoutine.Direction.kReverse)
           );
       }
   }

Motion Magic
~~~~~~~~~~~

CTRE 的 Motion Magic 功能提供硬體級的運動規劃：

- 平滑的 S-Curve 運動
- 限制巡航速度和加速度
- 減少系統振盪

程式碼輔助
~~~~~~~~~~

Motion Magic 配置範例：

.. code-block:: java

   public void configureMotors() {
       TalonFXConfiguration configs = new TalonFXConfiguration();

       // Motion Magic 配置
       configs.MotionMagic
           .withMotionMagicCruiseVelocity(DegreesPerSecond.of(1080))      // 巡航速度
           .withMotionMagicAcceleration(DegreesPerSecondPerSecond.of(3600)); // 加速度

       configs.Slot0.kP = 80.0;
       configs.Slot0.kI = 0.0;
       configs.Slot0.kD = 0.0;
       configs.Slot0.kG = 0.29103;  // 重力補償
       configs.Slot0.kA = 0.099301; // 加速度補償
       configs.Slot0.kS = 0.21953;  // 靜摩擦補償
       configs.Slot0.kV = 4.5976;   // 速度補償

       hoodMotor.getConfigurator().apply(configs);
   }

調校建議
~~~~~~~~

1. **開始調校 P 項**：從小值開始，逐步增加直到系統開始振盪
2. **添加 D 項**：適度增加 D 項來抑制振盪
3. **微調 I 項**：只在需要消除穩態誤差時使用
4. **使用 SysId**：進行系統識別來獲取準確的 kS、kV、kA 值
5. **測試邊界條件**：確保在極限位置和高速運動下都能穩定工作