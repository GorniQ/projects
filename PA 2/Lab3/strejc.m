function[MSE] = strejc(wej)
syms s;
T = wej(1);
n = wej(2);
id = wej(3);
load pomiary_3out.mat;
y = pomiary_3out(:,id)-pomiary_3out(1,id);
k = (y(300,1)-y(1,1))/1.0;
czas = 1:1:300;
l = [k];
m = sym2poly((T*s+1).^n);
ym = step(l,m,czas);
MSE = sum((y-ym).^2);
plot(czas,y,czas,ym);
u = ones(size(y));
yexper = iddata(y,u,1);
ymodel = tf(l,m);
compare(yexper,ymodel,300);
grid;
end