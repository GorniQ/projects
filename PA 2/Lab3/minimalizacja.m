function[MSE] = minimalizacja(Tz,Tm,tau,r)

load pomiary_3out.mat

pom = pomiary_3out
y2 = pom(:,2)-pom(1,2);

k2 = (y2(300,1)-y2(1,1))/1.0;

[ld,md]=pade(tau,r);
[l, m] = series(ld,md,[k2], [Tm*Tz,Tm+Tz, 1]);

czas=1:1:300;

ym2 = step(l,m,czas);

MSE= sum((y2-ym2).^2)

u=ones(size(y2));

y2exper=iddata(y2,u,1);
y2m=tf(l,m);

compare(y2exper,y2m,300);
grid
end
