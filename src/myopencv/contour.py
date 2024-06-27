import cv2
import numpy as np

# 读取图像
image = cv2.imread('data/lena.jpg')

# 显示图像
# cv2.imshow('Original Image', image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# # 将图像转换为灰度
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('Gray Image', gray_image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# 边缘检测
edges = cv2.Canny(gray_image, 100, 200)
# cv2.imshow('Edges', edges)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


# 找到轮廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
contour_image = image.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)
cv2.imshow('Contours', contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# cv2.imwrite('processed_image.jpg', contour_image)
