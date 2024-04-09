import cv2
import numpy as np

# 加载图像
img = cv2.imread('final_occupancy_map.png', 0)  # 以灰度模式加载

# 获取图像尺寸
rows, cols = img.shape

# 计算旋转矩阵
# 正值为逆时针旋转,负值为顺时针旋转
rotation_angle = -2.5  # 顺时针旋转10度
rotation_matrix = cv2.getRotationMatrix2D((cols / 2, rows / 2), rotation_angle, 1)

# 计算旋转后的图像边界
cos = np.abs(rotation_matrix[0, 0])
sin = np.abs(rotation_matrix[0, 1])
new_width = int((rows * sin) + (cols * cos))
new_height = int((rows * cos) + (cols * sin))

# 调整旋转矩阵,使图像保持在视图中心
rotation_matrix[0, 2] += (new_width / 2) - (cols / 2)
rotation_matrix[1, 2] += (new_height / 2) - (rows / 2)

# 进行旋转和填充
rotated_img = cv2.warpAffine(img, rotation_matrix, (new_width, new_height), borderValue=255)

# 裁剪图像到原始尺寸
x = new_width // 2 - cols // 2
y = new_height // 2 - rows // 2
rotated_img = rotated_img[y:y+rows, x:x+cols]

# 保存旋转后的图像
cv2.imwrite('rotated_occupancy_map.png', rotated_img)