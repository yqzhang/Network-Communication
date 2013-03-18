set terminal pngcairo enhanced font "arial,12" size 600, 400
set output 'failure_distribution.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set grid
set style data lines
set format y '%g %%'
set xlabel 'Number of failures occurred on a single link'
plot 'failure_distribution.dat' using 1:($2*100) title 'CDF'

