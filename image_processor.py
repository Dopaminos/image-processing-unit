import cv2
import numpy as np
from skimage.filters import threshold_otsu, roberts, sobel
from skimage.morphology import dilation, erosion, closing, opening, skeletonize

class ImageProcessor:
    def __init__(self, image_path=None):
        self.current_image = None
        self.processed_image = None
        if image_path:
            self.load_image(image_path)

    def load_image(self, image_path):
        self.current_image = cv2.imread(image_path)

    def apply_negative(self):
        self.processed_image = cv2.bitwise_not(self.current_image)

    def apply_power_transform(self, gamma):
        self.processed_image = np.array(255 * (self.current_image / 255) ** gamma, dtype='uint8')

    def apply_brightness_cut(self, lower, upper):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        mask = cv2.inRange(gray, lower, upper)
        self.processed_image = cv2.bitwise_and(self.current_image, self.current_image, mask=mask)

    def apply_smoothing_filter(self, kernel_size):
        self.processed_image = cv2.blur(self.current_image, (kernel_size, kernel_size))

    def apply_median_filter(self, kernel_size):
        self.processed_image = cv2.medianBlur(self.current_image, kernel_size)

    def apply_roberts(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        edge_roberts = roberts(gray)
        self.processed_image = (edge_roberts * 255).astype(np.uint8)

    def apply_sobel(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        edge_sobel = sobel(gray)
        self.processed_image = (edge_sobel * 255).astype(np.uint8)

    def apply_laplacian(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        self.processed_image = np.uint8(np.absolute(laplacian))

    def apply_histogram(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_img = np.zeros((300, 256, 3), dtype=np.uint8)
        cv2.normalize(hist, hist, 0, 300, cv2.NORM_MINMAX)
        for x, y in enumerate(hist):
            cv2.line(hist_img, (x, 300), (x, 300 - int(y)), (255, 255, 255))
        self.processed_image = hist_img

    def apply_hist_equalization(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        equ = cv2.equalizeHist(gray)
        self.processed_image = cv2.cvtColor(equ, cv2.COLOR_GRAY2BGR)

    def apply_threshold_global(self, threshold):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)
        self.processed_image = cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

    def apply_threshold_otsu(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        thresh = threshold_otsu(gray)
        _, otsu = cv2.threshold(gray, thresh, 255, cv2.THRESH_BINARY)
        self.processed_image = cv2.cvtColor(otsu, cv2.COLOR_GRAY2BGR)

    def apply_dilation(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        dilated = dilation(gray)
        self.processed_image = cv2.cvtColor((dilated * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def apply_erosion(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        eroded = erosion(gray)
        self.processed_image = cv2.cvtColor((eroded * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def apply_closing(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        closed = closing(gray)
        self.processed_image = cv2.cvtColor((closed * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def apply_opening(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        opened = opening(gray)
        self.processed_image = cv2.cvtColor((opened * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def apply_boundary_extraction(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        boundary = gray - erosion(gray)
        self.processed_image = cv2.cvtColor((boundary * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)

    def apply_skeletonization(self):
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        skeleton = skeletonize(gray / 255)
        self.processed_image = cv2.cvtColor((skeleton * 255).astype(np.uint8), cv2.COLOR_GRAY2BGR)
