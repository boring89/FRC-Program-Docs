Robot Setup
===========

Hardware Overview
-----------------

FRC 機器人由機械機構與電子控制系統組成。電子控制部分決定機器人的運作能力與穩定性，常見核心零件包括：

- NI roboRIO
- 馬達與馬達控制器
- 電力分配模組（PDP / PDP 2.0 / PDH / AMPD）
- 電壓調節模組（VRM）
- 主斷路器與分路斷路器
- 感測器與視覺系統
- 無線電與網路設備

NI roboRIO
~~~~~~~~~~

NI roboRIO 是 FRC 機器人的中央控制器，負責執行團隊自行撰寫的程式，並控制所有其他硬體。它連接馬達控制器、感測器、相機和 Driver Station，並透過 WPILib API 與各種外部裝置通訊。

Power Distribution
~~~~~~~~~~~~~~~~~~

電力分配是所有 FRC 機器人的核心。最常見的幾種電力分配模組如下：

- Power Distribution Panel (PDP): 傳統 12V 電力分配板，用於將電池電源分配給馬達控制器、roboRIO、VRM、PCM 等元件。
- Power Distribution Hub (PDH): REV 的電力分配模組，內含高電流與低電流通道，並支援 CAN / USB-C 遙測。
- Power Distribution Board (AMPD): AndyMark 的 24 埠電力分配板，支援 ATO / ATC 斷路器與簡潔布線。
- Voltage Regulator Module (VRM): CTRE 的電壓調節模組，提供穩壓 12V 和 5V 輸出，常用於相機與客製電子電路。
- 120A 主斷路器: 機器人電源的總開關與保護元件，連接電池與電力分配模組間的正極。

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

Power Distribution Details
~~~~~~~~~~~~~~~~~~~~~~~~~~

- CTRE Power Distribution Panel (PDP): 將 12VDC 電池電源分配給機器人各個元件，提供 8 組 40A 機械通道與 8 組 30A 通道，並具備 CAN 介面，可記錄電流、溫度與電池電壓。
- CTRE Power Distribution Panel 2.0 (PDP 2.0): 提供 24 個 40A 通道並支援 ATO 斷路器，適合需要更多驅動通道的機器人。注意：PDP 2.0 本身不具有內建電流日誌顯示。
- REV Power Distribution Hub (PDH): 提供 20 個高電流通道（40A）與 3 個低電流通道（15A），以及 1 個可切換的低電流通道。具備可拆式 WAGO 端子、LED 電壓顯示器，並可透過 CAN / USB-C 連接 REV Hardware Client 監控遙測資料。
- AndyMark Power Distribution Board (AMPD): 提供 24 個 40A 端口，支援 ATO / ATC 斷路器，並設計成便於整理布線的直角輸出。
- CTRE Voltage Regulator Module (VRM): 由 PDP 的專用連接器供電，提供穩壓 12V 與 5V 輸出，適合供電給相機與自訂電路。
- 120A Main Circuit Breaker: 機器人電源系統的總開關與保護元件，保護下游布線與電控裝置。
- Breakers: Snap Action 與 Rev ATO 斷路器常見於 PDP/PDH/PDP 2.0，用於分路保護。ATO 斷路器有 40A、30A、20A、10A 等規格。

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