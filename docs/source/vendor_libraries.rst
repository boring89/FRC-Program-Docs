第三方函式庫與 Vendor 依賴
=========================

當你的 FRC 機器人使用 CTRE、REV 或其他高級設備時，通常需要安裝「廠商函式庫」，這些函式庫稱為 vendor dependency。

什麼是 vendor dependency？
--------------------------

Vendor dependency 是廠商提供給機器人的軟體套件，讓你的程式可以控制他們的硬體設備。舉例來說：

- CTRE Phoenix 用來控制 Talon SRX、Talon FX、Victor SPX 等馬達控制器
- REV 的驅動程式用來控制 Spark MAX、CANSparkMax、PDH 等硬體

這些函式庫讓你能夠使用 CAN 或其他通訊協定，取得更完整的功能，而不是只使用基本的 PWM 控制。

為什麼要使用 vendor dependency？
-------------------------------

使用 vendor dependency 的好處：

- 可以使用高階功能，例如編碼器回傳、位置控制、PID 自動調整
- 支援更多型號的馬達控制器與感測器
- 可以透過廠商提供的官方工具進行設定、診斷與韌體更新

管理 vendor dependency
------------------------

在 WPILib 專案中，vendor dependency 是「每個專案獨立安裝」的。常見方式有兩種：

- 線上安裝：透過網路下載函式庫，適合有網路時使用
- 離線安裝：使用廠商提供的安裝程式，一次安裝所有必要元件

線上安裝有一個重要提醒：如果你使用線上模式，請每 30 天重新連網並重新建立專案，否則下載快取可能會清除，已安裝的函式庫可能會消失。

使用 VS Code 的 Vendor Dependency 管理器
-------------------------------------

在 VS Code 中安裝 WPILib 擴充後，你可以看到 Dependency Manager：

- 點選側邊欄中的 WPILib 圖示
- 進入 Vendor Dependency 管理頁面
- 點選你要安裝的函式庫旁的 Install
- 如果要更新，點選 To Latest 或 Update All
- 如果要移除，點選垃圾桶圖示

安裝後，對應的 JSON 檔案會儲存在專案的 `vendordeps` 資料夾中，這樣專案就知道要包含這些外部函式庫。

第三方函式庫示例
----------------

常見的 FRC 第三方函式庫：

- CTRE Phoenix: 讓你控制 Talon 系列與 Victor 系列馬達控制器
- REV Lib: 讓你控制 Spark MAX、CANSparkMax、PDH、Pneumatic Hub 等
- 其他廠商感測器套件：例如 LiDAR、Vision、IMU 等

如果你使用 Java，這些函式庫會自動被加入 Gradle 專案，讓你在程式中直接 `import` 對應的類別。

小結
----

對於剛接觸 FRC 的隊伍，建議先從 WPILib 內建的控制器與感測器開始，待熟悉後再加入 vendor dependency。若你必須使用廠商硬體，優先選擇離線安裝，因為它更穩定，也更不會因為網路變動而影響開發環境。