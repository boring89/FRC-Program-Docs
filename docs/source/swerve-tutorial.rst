Swerve 驅動程式編寫教程
====================

本教程基於 `2024-CloneBot` 專案，逐步教你從零開始編寫一個完整的 Swerve 驅動控制程式。這個專案使用了 REV Robotics 的 Spark 馬達控制器和 CTRE 的 CANcoder 絕對編碼器，是 FRC 中常見的硬體配置。

專案概覽
--------

GitHub 連結：https://github.com/FRC-Team-10114/2024-CloneBot

這個專案實現了一個完整的 Swerve 驅動系統，包含：

- 4 個 Swerve 模組（前左、前右、後左、後右）
- 場地相對座標控制
- 速度限制與平滑控制
- PathPlanner 自動路徑支援
- 視覺定位整合

教程內容
--------

本教程分為以下幾個部分：

.. toctree::
   :maxdepth: 2

   swerve-constants
   swerve-module
   swerve-drivetrain
   swerve-commands
   swerve-integration

開始之前
--------

在開始編寫程式之前，請確保你已經：

1. 安裝了 WPILib 開發環境
2. 建立了新的 Java Command-Based 專案
3. 熟悉基本的 Java 程式設計概念
4. 了解 FRC 機器人的基本結構

讓我們開始建立你的第一個 Swerve 驅動系統吧！

