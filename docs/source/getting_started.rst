Getting Started
===============

本章節說明如何為 FRC 程式建立開發環境，以及如何開始使用本專案。

Prerequisites
-------------

- Visual Studio Code
- WPILib extension for VSCode
- Java 17
- FRC Driver Station (部署時必要)

Install WPILib
--------------

1. 下載並安裝 WPILib：
   - 前往 https://wpilib.org 取得最新版本。
   - 遵循官方安裝步驟。
2. 在 VSCode 中安裝 WPILib 擴充套件。
3. 確認 Java 17 已安裝，並且 `java -version` 顯示正確版本。

Clone the repository
--------------------

使用 Git 將本專案複製到本機：

.. code-block:: bash

   git clone https://github.com/boring89/FRC-Program-Docs.git

打開專案：

- 在 VSCode 中選擇 `File -> Open Folder...`
- 選擇剛才複製的資料夾

Open the project in VSCode
--------------------------

1. 開啟 VSCode。
2. 打開專案資料夾。
3. 確認側邊欄中的 WPILib 工具已正確載入。
4. 如果出現相依性提示，請執行 `pip install -r docs/requirements.txt`（如果你要建立文件網站）。

Build and Run
-------------

若要編譯或部署機器人程式，請使用 WPILib 提供的命令或工具列選單。

1. 在 VSCode 中打開命令面板（Ctrl+Shift+P）。
2. 執行 `WPILib: Build Robot Code`。
3. 執行 `WPILib: Deploy Robot Code`。

Next steps
----------

- 前往 :doc:`/programming` 了解程式架構與控制流程。
- 前往 :doc:`/robot_setup` 了解機器人硬體與網路設定。
- 若要加入新功能，請先閱讀專案中的 `README` 或開發指南。
