PhotonVision 視覺辨識與定位
==========================

`PhotonVision` 與 `AutoAlign` 組合可支援目標對齊功能。
這個專案在 `RobotContainer` 中建立了視覺事件與狀態觸發器。

PhotonVision 的主要功能：

- 使用 PhotonVision 程式庫進行 AprilTag 檢測
- 支援多相機配置和姿態估計
- 實現視覺里程計融合到 Swerve 驅動系統
- 提供姿態重置功能用於初始化

程式碼輔助
~~~~~~~~~~

以下是 PhotonVision.java 的關鍵程式碼片段：

.. code-block:: java

   public class PhotonVision extends SubsystemBase {

     private final List<CamWrapper> cams = new ArrayList<>();

     public PhotonVision(CommandSwerveDrivetrain drive, Map<String, Transform3d> cameraTransforms) {
       AprilTagFieldLayout fieldLayout = AprilTagFieldLayout.loadField(AprilTagFields.kDefaultField);

       cameraTransforms.forEach((name, transform) -> {
         PhotonCamera cam = new PhotonCamera(name);
         PhotonPoseEstimator estimator = new PhotonPoseEstimator(
             fieldLayout,
             PoseStrategy.MULTI_TAG_PNP_ON_COPROCESSOR,
             transform);
         estimator.setMultiTagFallbackStrategy(PoseStrategy.LOWEST_AMBIGUITY);
         cams.add(new CamWrapper(name, cam, estimator));
       });
     }

     private void updateVision() {
       for (CamWrapper cw : cams) {
         for (PhotonPipelineResult result : cw.cam.getAllUnreadResults()) {
           Optional<EstimatedRobotPose> poseOpt = cw.estimator.update(result);
           if (poseOpt.isPresent()) {
             EstimatedRobotPose est = poseOpt.get();
             Pose3d cameraRobotPose3d = est.estimatedPose;

             // 過濾和驗證邏輯
             int numTags = est.targetsUsed.size();
             double avgDist = calculateAverageDistance(est.targetsUsed);

             Vector<N3> stdDevs = calculateStandardDeviations(numTags, avgDist, this.NeedResetPose);
             drivetrain.addVisionMeasurement(
                 cameraRobotPose3d.toPose2d(),
                 est.timestampSeconds,
                 stdDevs);
           }
         }
       }
     }

     public boolean resetPoseToVision() {
       // 尋找最佳姿態進行重置
       Pose2d bestPose = findBestPoseFromCameras();
       if (bestPose != null) {
         drivetrain.resetPose(bestPose);
         return true;
       }
       return false;
     }

   }

這個類別展示了先進的視覺處理和姿態估計技術在 FRC 中的應用。