[X, map] = imread('Lekagul Roadways.bmp');
if ~isempty(map)
    img = ind2rgb(flipud(X),map);
end
image(img)
set(gca,'YDir','normal')

% ��Ҫ���ҵĵ��r, g, bֵ
r_value = 1; 
g_value = 0;
b_value = 0;
% image ��r, g, b��������ͼ��
r = img(:, :, 1);
g = img(:, :, 2);
b = img(:, :, 3);
% ��ʾ��ͼ��image�к�ɫ���λ��Ϊ1,������Ϊ0,��������index��
index_r = (abs(r - r_value) < 0.01);
index_g = (abs(g - g_value) < 0.01);
index_b = (abs(b - b_value) < 0.01);
index = index_r & index_g & index_b;
% ���յĺ�ɫ��λ��(x, y)����
[y, x] = find(index == 1);
for i = 1: length(x)
    fprintf('%d\t%d\n',x(i),y(i))
end