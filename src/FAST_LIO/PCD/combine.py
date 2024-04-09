import cv2
import numpy as np

# 加载图像
img1 = cv2.imread('xu_0.65_inf.png', 0)  # 以灰度模式加载图像1
img2 = cv2.imread('xu_1.1_inf.png', 0)  # 以灰度模式加载图像2

# 获取图像的尺寸
height1, width1 = img1.shape
height2, width2 = img2.shape

# 确定分割线的位置
split_col1 = width1 // 2  # 图像1的分割线列坐标
split_col2 = width2 // 2  # 图像2的分割线列坐标

# 创建新的图像来保存合并结果
merged_img = np.zeros((max(height1, height2), split_col1 + (width2 - split_col2)), np.uint8)

# 将图像1的左侧复制到合并图像中
merged_img[:height1, :split_col1] = img1[:, :split_col1]

# 将图像2的右侧复制到合并图像中
merged_img[:height2, split_col1:] = img2[:, split_col2:]

# 显示合并后的图像
cv2.imwrite('final_occupancy_map.png', merged_img)
