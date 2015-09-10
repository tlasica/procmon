src_filename = argv(){1};
png_filename = argv(){2};


warning("off", "all");

data = dlmread(src_filename);
time = data(:,1);
usr = data(:,4);
sys = data(:,5);
total = data(:,7);

for i=1:length(time)
    ts = strptime(num2str(time(i), "%06d"), "%H%M%S");
    tt = ts.hour*3600+ts.min*60+ts.sec;
    time(i)=tt;
end

diff = time(3)-time(2)
for i=2:length(time)
    time(i) = (i-1) * diff;
end

plot(time, usr, "b", time, sys, "r", time, total, "g");

title(["total CPU (usr/sys/total)" " for " src_filename]);

legend("usr","sys","total");
xlabel("[sec] since start")
ylabel("[%] of cpu");

print(png_filename);


