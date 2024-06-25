import cv2
from tqdm import tqdm
from ultralytics import YOLO
import supervision as sv
import numpy as np
from collections import defaultdict, deque

def vehicle_detect():
    # 配置
    MODEL = 'static/model/best.pt'
    MODEL_RESOLUTION = 1280
    SOURCE_VIDEO_PATH = 'tests/minivehicles.mp4'
    TARGET_VIDEO_PATH = 'tests/minivehicles-result.mp4'
    CONFIDENCE_THRESHOLD = 0.3
    IOU_THRESHOLD = 0.5
    SOURCE = np.array([
        [1252, 787],
        [2298, 803],
        [5039, 2159],
        [-550, 2159]
    ])
    TARGET_WIDTH = 25
    TARGET_HEIGHT = 250
    TARGET = np.array([
        [0, 0],
        [TARGET_WIDTH - 1, 0],
        [TARGET_WIDTH - 1, TARGET_HEIGHT - 1],
        [0, TARGET_HEIGHT - 1],
    ])

    # 矩阵变换
    class ViewTransformer:

        def __init__(self, source: np.ndarray, target: np.ndarray) -> None:
            source = source.astype(np.float32)
            target = target.astype(np.float32)
            self.m = cv2.getPerspectiveTransform(source, target)

        def transform_points(self, points: np.ndarray) -> np.ndarray:
            if points.size == 0:
                return points

            reshaped_points = points.reshape(-1, 1, 2).astype(np.float32)
            transform_points = cv2.perspectiveTransform(reshaped_points, self.m)
            return transform_points.reshape(-1, 2)


    # 初始化
    model = YOLO(MODEL)
    video_info = sv.VideoInfo.from_video_path(SOURCE_VIDEO_PATH)
    view_transformer = ViewTransformer(SOURCE, TARGET)
    frame_generator = sv.get_video_frames_generator(SOURCE_VIDEO_PATH)
    frame_iterator = iter(frame_generator)
    frame = next(frame_iterator)

    byte_track = sv.ByteTrack(
        frame_rate=video_info.fps,
        track_activation_threshold=CONFIDENCE_THRESHOLD,
    )

    thickness = sv.calculate_optimal_line_thickness(
        resolution_wh=video_info.resolution_wh
    )
    text_scale = sv.calculate_optimal_text_scale(
        resolution_wh=video_info.resolution_wh
    )
    bounding_box_annotator = sv.BoundingBoxAnnotator(
        thickness=thickness
    )
    label_annotator = sv.LabelAnnotator(
        text_scale=text_scale,
        text_thickness=thickness,
        text_position=sv.Position.BOTTOM_CENTER
    )
    trace_annotator = sv.TraceAnnotator(
        thickness=thickness,
        trace_length=video_info.fps * 2,
        position=sv.Position.BOTTOM_CENTER
    )

    polygon_zone = sv.PolygonZone(
        polygon=SOURCE,
        frame_resolution_wh=video_info.resolution_wh
    )

    coordinates = defaultdict(lambda: deque(maxlen=video_info.fps))

    # 开始
    with sv.VideoSink(TARGET_VIDEO_PATH, video_info) as sink:

        # 遍历每帧
        for frame in tqdm(frame_generator, total=video_info.total_frames):

            result = model(frame, imgsz=MODEL_RESOLUTION, verbose=False)[0]
            detections = sv.Detections.from_ultralytics(result)

            # 过滤标签
            detections = detections[detections.confidence > CONFIDENCE_THRESHOLD]
            detections = detections[detections.class_id == 0]

            # 过滤区域
            detections = detections[polygon_zone.trigger(detections)]

            detections = detections.with_nms(IOU_THRESHOLD)

            detections = byte_track.update_with_detections(detections)

            points = detections.get_anchors_coordinates(
                anchor=sv.Position.BOTTOM_CENTER
            )

            points = view_transformer.transform_points(points).astype(int)

            for tracker_id, [_, y] in zip(detections.tracker_id, points):
                coordinates[tracker_id].append(y)

            # 格式化
            labels = []

            for tracker_id in detections.tracker_id:
                if len(coordinates[tracker_id]) < video_info.fps / 2:
                    labels.append(f"#{tracker_id}")
                else:
                    # 估算速度
                    coordinates_start = coordinates[tracker_id][-1]
                    coordinates_end = coordinates[tracker_id][0]
                    distance = abs(coordinates_start - coordinates_end)
                    time = len(coordinates[tracker_id]) / video_info.fps
                    speed = distance / time * 3.6
                    labels.append(f"#{tracker_id} {int(speed)} km/h")

            # 标注
            annotated_frame = frame.copy()
            annotated_frame = trace_annotator.annotate(
                scene=annotated_frame,
                detections=detections
            )
            annotated_frame = bounding_box_annotator.annotate(
                scene=annotated_frame,
                detections=detections
            )
            annotated_frame = label_annotator.annotate(
                scene=annotated_frame,
                detections=detections,
                labels=labels
            )

            # sv.plot_image(annotated_frame)

            # 保存
            sink.write_frame(annotated_frame)