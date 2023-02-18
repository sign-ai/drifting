from drifting.drift_detection_server.label import LabelDriftDetectorCore


def test_label_detector():
    """Test if detector created."""
    detector = LabelDriftDetectorCore()
    assert detector.implementation_path == "label.LabelDriftDetector"
