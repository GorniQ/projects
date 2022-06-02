T = 45;
tau = 22;
h1 = [0.05,0.1, 0.2];
SP = 0.5;


figure;
for h=[0.05 0.1 0.2]
    out = sim('Lab4');
    y = out.y;
    u = out.u;
    l = append("h=", string(h));
    plot(u.time,u.signals.values,'DisplayName',l)
    grid
    xlabel('czas[s]')
    ylabel('u(t)')
    axis([0,300,0,1])
    legend;
    hold on
end

figure;
for h=[0.05 0.1 0.2]
    out = sim('Lab4');
    y = out.y;
    u = out.u;
    l = append("h=", string(h));
    plot(y.time,y.signals.values,'DisplayName',l)
    grid
    xlabel('czas[s]')
    ylabel('y(t)')
    axis([0,300,-0.1,1.2])
    legend;
    hold on
end


