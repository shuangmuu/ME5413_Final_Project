import pcl
import numpy as np
import cv2

# 加载PCD文件
# filename = "xu"
# cloud = pcl.load(f"{filename}_scans.pcd")

cloud = pcl.load("aloam.pcd")

# 创建一个PassThrough过滤器,只保留Z轴上一定范围内的点
passthrough = cloud.make_passthrough_filter()
passthrough.set_filter_field_name('z')
z_min = 0.2
z_max = np.inf  # 调整z_max的值以适应你的场景
passthrough.set_filter_limits(z_min, z_max)
cloud_filtered = passthrough.filter()

# 获取点云的x,y范围
max_x = np.max(cloud_filtered.to_array()[:, 0])
min_x = np.min(cloud_filtered.to_array()[:, 0])
max_y = np.max(cloud_filtered.to_array()[:, 1]) 
min_y = np.min(cloud_filtered.to_array()[:, 1])

# # xu
# max_x =19.41440773010254; min_x = -1.7952392101287842
# max_y = 5.5600481033325195; min_y = -16.34099578857422
# max_z = 5.189615726470947; min_z = -0.21556983888149261

# ye
# max_x =18.953990936279297; min_x = -1.6434186697006226
# max_y = 4.950534343719482; min_y = -15.496820449829102

# print(f"{max_x}\n")
# print(f"{min_x}\n")
# print(f"{max_y}\n")
# print(f"{min_y}\n")

grid_resolution = 0.04  # 米

# 创建一个空的占用网格
width = int((max_x - min_x) / grid_resolution) + 1
height = int((max_y - min_y) / grid_resolution) + 1
occupancy_grid = np.full((height, width), 255, np.uint8)  # 255表示未占用

# 将点云投影到2D占用网格
points = cloud_filtered.to_array()
for point in points:
    x, y = point[0], point[1]
    cell_x = int((x - min_x) // grid_resolution)
    cell_y = int((y - min_y) // grid_resolution)
    occupancy_grid[height - cell_y - 1, cell_x] = 0  # 0表示占用

# 应用形态学操作去除噪点
# kernel = np.ones((2, 2), np.uint8)
# occupancy_grid = cv2.morphologyEx(occupancy_grid, cv2.MORPH_OPEN, kernel)
# occupancy_grid = cv2.morphologyEx(occupancy_grid, cv2.MORPH_CLOSE, kernel)

# edges = cv2.Canny(occupancy_grid, 50, 150, apertureSize=3)
# lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
# angles = []
# for theta in lines[0]:
#     angle = theta * 180 / np.pi
#     if angle < 0:
#         angle += 180
#     angles.append(angle)

# average_angle = np.mean(angles) - 90

# height, width = occupancy_grid.shape
# M = cv2.getRotationMatrix2D((width/2, height/2), average_angle, 1)
# occupancy_map_corrected = cv2.warpAffine(occupancy_grid, M, (width, height), borderValue=255)


# 保存PNG图像
# cv2.imwrite(f'{filename}_{z_min}_{z_max}.png', occupancy_map_corrected)
# print("PNG image generated successfully!")

# 保存PNG图像
cv2.imwrite(f'{z_min}_{z_max}.png', occupancy_grid)
print("PNG image generated successfully!")