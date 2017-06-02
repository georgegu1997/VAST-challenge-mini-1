[X, map] = imread('Lekagul Roadways.bmp');
if ~isempty(map)
    img = ind2rgb(flipud(X),map);
end
image(img)
set(gca,'YDir','normal')

% 所要查找的点的r, g, b值
r_value = 1; 
g_value = 0;
b_value = 0;
% image 的r, g, b三个分量图像
r = img(:, :, 1);
g = img(:, :, 2);
b = img(:, :, 3);
% 标示出图像image中红色点的位置为1,其它点为0,结果存放在index中
index_r = (abs(r - r_value) < 0.01);
index_g = (abs(g - g_value) < 0.01);
index_b = (abs(b - b_value) < 0.01);
index = index_r & index_g & index_b;
% 最终的红色点位置(x, y)坐标
[y, x] = find(index == 1);
for i = 1: length(x)
    fprintf('%d\t%d\n',x(i),y(i))
end