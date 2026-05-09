Robot Setup
===========

Hardware Overview
-----------------

FRC 機器人由許多子系統構成，從控制核心到驅動、感測與電源分配都不可忽視。常見的主要零件如下。

Electronic Control
~~~~~~~~~~~~~~~~~~

- RoboRIO: 機器人中央控制器，是整個系統的大腦。它負責執行 WPILib 程式、處理感測器資料、控制馬達與通訊。
- Power Distribution Panel (PDP): 傳統電力分配板，用來提供 12V 電源給馬達控制器、機器人電腦和其他電子設備，並內建電流感測器。
- Power Distribution Hub (PDH): WPILib 新一代電力分配模組，功能與 PDP 類似，但支援更簡單的數位訊號與更方便的電流監測。
- Advanced Power Distribution (AMPD): 更高階的電力模組，整合電流監測與電源管理，適合複雜布線需求的隊伍。

Motor Controllers
~~~~~~~~~~~~~~~~~

馬達控制器是馬達與控制器之間的橋樑。常見型號包括：

- Talon FX / Talon SRX（CTRE Phoenix）
- Victor SPX（CTRE Phoenix）
- CANSparkMax（REV Robotics）
- SPARK MAX（REV Robotics）
- PWM SparkMax、Jaguar、Victor 亦可用於較簡單的 PWM 馬達連接 （已棄用）。

這些控制器通常透過 CAN 線路或 PWM 線連接到 RoboRIO 或 PDH，並由程式發送電力與速度指令。

Motors
~~~~~~

FRC 常用馬達種類：

- CIM Motor: 大扭力、高耐用性，常用於驅動系統。
- NEO / NEO 550: 內建編碼器的無刷馬達，常與 CANSparkMax 搭配使用。
- Falcon 500: CTRE 的無刷馬達，內建控制器與編碼器，常見於驅動與高性能系統。
- Bag Motor / Mini CIM: 較小型、轉速較高，通常用於機構或射球機構。

Drive Base
~~~~~~~~~~

機器人底盤驅動系統有多種設計：

- Tank Drive: 左右兩側各一組馬達，簡單易用。
- Swerve Drive: 每個輪子可獨立轉向與推進，靈活度高但控制複雜。
- Mecanum Drive: 使用斜向輪，可原地平動。

Sensor & Vision
~~~~~~~~~~~~~~

感測器與視覺模組用於定位、導航與目標追蹤：

- Limelight: 常見的視覺目標追蹤相機，用於瞄準與自動對準。
- NavX / Pigeon IMU: 提供陀螺儀、加速度計與姿態資料。
- Encoder: 測量軸轉速或位置，常用於閉迴路控制。
- Ultrasonic / Lidar: 用於距離感測與避障。

Power & Pneumatics
------------------

電力與氣動系統也是機器人穩定運作的關鍵。

- Battery: 通常使用 12V FRC 標準電池。
- Voltage Regulator Module (VRM): 為控制器與感測器提供穩定 5V 或 12V 電源。
- Compressor / Solenoid Module: 氣動系統供氣與電磁閥控制。

Detailed Power Distribution Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- PDP (Power Distribution Panel): 傳統 FRC 電力分配板，提供 12 個電路，並支援電流感測。
- PDH (Power Distribution Hub): 新型分配模組，提供 CAN 連線與更多電流監控功能，通常與 WPILib 更加整合。
- AMPD (Advanced Power Distribution): 更高階的電源分配與管理設備，可支援更複雜的系統需求。

Network Configuration
---------------------

在部署前，請確認機器人與 Driver Station 均連接到 FRC 專用網路：

- Robot IP 通常為 `10.TE.AM.2`（例如 `10.8.9.2`）。
- Driver Station 必須設定正確 TEAM 號碼。
- 檢查網路線、交換器和 Wi-Fi 設備是否正確連接。

基本接線提示
~~~~~~~~~~~~~~~~

- RoboRIO: 連到 PDH/PDP 的 12V 電源，並接上網路線與 PC。
- 馬達控制器: 使用 CAN 或 PWM 線連接至控制器，並將電力線接到 PDH/PDP。
- 感測器: 如編碼器、NavX，通常連接到 RoboRIO 的數位輸入或 SPI 介面。
- Limelight: 直接連接到網路，並與 RoboRIO 透過網路表格（NetworkTables）交換資料。

安全與檢查
-------------

1. 開機前先檢查線材是否牢固。
2. 確認電池電壓在安全範圍內。
3. 檢查所有馬達控制器與感測器是否有正確 ID 與接線。
4. 使用 Driver Station 的 `Test` 標籤頁確認馬達與輸入裝置功能正常。

這些設備與架構是 FRC 機器人硬體的核心。理解它們的功能與連接方式，對於後續程式設計與調整非常重要。