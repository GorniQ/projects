function [MSE] = kup1rz(wej)
load pomiary_3out.mat;
y = pomiary_3out(:,nrpom) - pomiary_3out(1,nrpom);

T = wej(1);
tau = wej(2);
nrpom = wej(3);
k = (y(300,1)-y(1,1))/1.0;
[ld, md] = pade(tau,10);
[l, m] = series([k],[T 1],ld,md);
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

