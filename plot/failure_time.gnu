set terminal pngcairo enhanced font "arial,10" size 500, 350 
set output 'failure_time.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set style data points
set title 'Recovery time of the ISIS failures'
plot 'failure_time.dat' using 2:1 title 'failure last time (in second)'
