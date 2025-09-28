import re
import cv2
import torch
import difflib
import numpy as np
from PIL import Image
from collections import deque
from django.core.management.base import BaseCommand
from ultralytics import YOLO
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from API.tasks import add_vehicle_entry

# ========== CONFIGURATION ==========
YOLO_MODEL_PATH = "Utils/best.pt"  # Path to your YOLO model
VIDEO_SOURCE = "http://192.168.0.128:8080/video"  # Your video stream or file path
# VIDEO_SOURCE = "../sample/sample5.mp4"

CAMERA_ID = 1
CONFIDENCE_THRESHOLD = 0.80
OCR_BACKEND = "paddle"  # Options: "trocr", "paddle", "easyocr"
TROCR_MODEL = "microsoft/trocr-small-printed"

# Deduplication settings
USE_FUZZY_MATCHING = True
RECENTLY_DETECTED_PLATES = deque(maxlen=50)

VALID_STATES = {
    "AP", "AR", "AS", "BR", "CH", "CT", "DN", "DD", "DL", "GA", "GJ", "HR", "HP",
    "JH", "JK", "KA", "KL", "LA", "LD", "MH", "ML", "MN", "MP", "MZ", "NL", "OD",
    "PB", "PY", "RJ", "SK", "TN", "TR", "TS", "UK", "UP", "WB"
}

device = "cuda" if torch.cuda.is_available() else "cpu"


# ========== OCR WRAPPER ==========
class OCRRecognizer:
    def __init__(self, backend="trocr"):
        self.backend = backend.lower()
        print(f"[INFO] Initializing OCR backend: {self.backend}")

        if self.backend == "trocr":
            self.processor = TrOCRProcessor.from_pretrained(TROCR_MODEL)
            self.model = VisionEncoderDecoderModel.from_pretrained(TROCR_MODEL).to(device)
        elif self.backend == "paddle":
            from paddleocr import PaddleOCR
            self.model = PaddleOCR(
                use_textline_orientation=False,
                use_doc_orientation_classify=False,
                use_doc_unwarping=False,
            )
        elif self.backend == "easyocr":
            import easyocr
            self.model = easyocr.Reader(["en"], gpu=(device == "cuda"))
        else:
            raise ValueError(f"OCR backend '{self.backend}' is not supported.")
        print("[INFO] OCR backend loaded successfully.")

    def recognize(self, image):
        text = ""
        try:
            if self.backend == "trocr":
                pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
                inputs = self.processor(images=pil_img, return_tensors="pt").pixel_values.to(device)
                with torch.no_grad():
                    output_ids = self.model.generate(inputs)
                text = self.processor.batch_decode(output_ids, skip_special_tokens=True)[0]
            elif self.backend == "paddle":
                result = self.model.predict(image)
                if result and len(result) > 0:
                    rec_texts = result[0].get("rec_texts", [])
                    rec_scores = result[0].get("rec_scores", [])
                    if rec_texts:
                        best_idx = int(np.argmax(rec_scores)) if rec_scores else 0
                        text = rec_texts[best_idx]
            elif self.backend == "easyocr":
                result = self.model.readtext(image)
                if result:
                    text = result[0][1]
        except Exception as e:
            print(f"[WARNING] OCR recognition failed: {e}")
            return None

        return self.clean_plate(text)

    @staticmethod
    def clean_plate(text):
        if not text:
            return None
        text = re.sub(r"[^A-Z0-9]", "", text.upper())
        match = re.fullmatch(r"([A-Z]{2})(\d{2})([A-Z]{1,3})(\d{4})", text)
        if match and match.group(1) in VALID_STATES:
            return "".join(match.groups())
        return None


def is_similar(a, b, threshold=0.85):
    return difflib.SequenceMatcher(None, a, b).ratio() >= threshold


# ========== DJANGO COMMAND ==========
class Command(BaseCommand):
    help = "Run ANPR (Automatic Number Plate Recognition) pipeline"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS(f"[INFO] Using device: {device}"))
        self.run_anpr()

    def run_anpr(self):
        self.stdout.write(f"[INFO] Starting video source: {VIDEO_SOURCE}")
        cap = cv2.VideoCapture(VIDEO_SOURCE)
        if not cap.isOpened():
            self.stderr.write(self.style.ERROR("[ERROR] Failed to open video source."))
            return

        detector = YOLO(YOLO_MODEL_PATH)
        ocr = OCRRecognizer(backend=OCR_BACKEND)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                self.stdout.write("[INFO] End of video stream.")
                break

            results = detector(frame, stream=True, verbose=False)

            for result in results:
                for box in result.boxes:
                    if box.conf[0] < CONFIDENCE_THRESHOLD:
                        continue

                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cropped_plate = frame[y1:y2, x1:x2]

                    plate_text = ocr.recognize(cropped_plate)

                    if plate_text:
                        is_duplicate = False
                        if USE_FUZZY_MATCHING:
                            if any(is_similar(plate_text, p) for p in RECENTLY_DETECTED_PLATES):
                                is_duplicate = True
                        elif plate_text in RECENTLY_DETECTED_PLATES:
                            is_duplicate = True

                        if not is_duplicate:
                            self.stdout.write(self.style.SUCCESS(
                                f"[INFO] New plate detected: {plate_text}. Sending to DB..."
                            ))
                            RECENTLY_DETECTED_PLATES.append(plate_text)
                            add_vehicle_entry.delay(car_number=plate_text, camera_id=CAMERA_ID)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()
        self.stdout.write(self.style.SUCCESS("[INFO] ANPR process finished."))
