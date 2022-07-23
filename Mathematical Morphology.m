clc;
clear all;
close all;
img=imread('e:/1.jpg');
gray_img=rgb2gray(img);
bw_img=im2bw(gray_img);
bw_img1=~bw_img;
se=strel('rectangle',[3 1])
bw_erode=imerode(bw_img1,se);
g=~bw_erode;
imshow(g);
[L n]=bwlabel(bw_erode);
s= regionprops(L, 'BoundingBox');
s.BoundingBox
rectangle('Position',s(1).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(2).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(3).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(4).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(5).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(6).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(7).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(8).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(9).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(10).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(11).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(12).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(13).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(14).BoundingBox,'edgecolor','r','LineWidth',1.5);
rectangle('Position',s(15).BoundingBox,'edgecolor','r','LineWidth',1.5);