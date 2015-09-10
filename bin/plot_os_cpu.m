warning("off", "all");
data = dlmread('os_cpu.log.tmp');
time = data(:,1);
usr = data(:,2);
sys = data(:,4);
idle = data(:,11);

for i=1:length(time)
    ts = strptime(num2str(time(i), "%06d"), "%H%M%S");
    tt = ts.hour*3600+ts.min*60+ts.sec;
    time(i)=tt;
end

diff = time(3)-time(2)
for i=2:length(time)
    time(i) = (i-1) * diff;
end

plot(time, usr, "b", time, sys, "r", time, idle, "g");

title('total CPU (usr/sys/idle)');

legend('usr','sys','idle');
xlabel('[sec] since start')
ylabel('[%] of cpu');

print('os_cpu.png');


