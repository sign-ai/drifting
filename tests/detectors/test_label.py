from drifting.detectors.label import LabelDriftDetectorCore


def test_label_detector():
    """Test if detector created."""
    detector = LabelDriftDetectorCore()
    assert detector.implementation_path == "label.LabelDriftDetector"
