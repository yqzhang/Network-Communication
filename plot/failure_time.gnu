set terminal pngcairo enhanced font "arial,12" size 600, 400
set output 'failure_time.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set grid
set style data lines
set format y '%g %%'
set xlabel 'Recovery time in seconds'
plot 'failure_time.dat' using 1:($2*100) title 'CDF'

