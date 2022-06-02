function [MSE] = kup2rz(wej)

load pomiary_3out.mat;

T1 = wej(1);
T2 = wej(2);
tau = wej(3);
nrpom = wej(4);
y = pomiary_3out(:,nrpom) - pomiary_3out(1,nrpom);
k = (y(300,1)-y(1,1))/1.0;
[ld, md] = pade(tau,10);
[l, m] = series (ld,md,[k], [T1*T2,T1+T2, 1]);
czas = 1:1:300;
ym = step(l,m,czas);
MSE = sum((y-ym).^2);

plot(czas,y,czas,ym);
u = ones(size(y));
yexper = iddata(y,u,1);
ymodel = tf(l,m);
compare(yexper,ymodel,300);
grid;
end