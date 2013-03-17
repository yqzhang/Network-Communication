set terminal pngcairo enhanced font "arial,8" size 600, 400
set output 'failure_plot.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set style data lines
set title 'Network Failure Distribution of CENIC 10/20/2012-02/09/2013'
set xdata time
set timefmt '%m-%d-%Y %H:%M:%S'
set format x '%m-%d-%Y'
plot 'failure_plot.dat' using 2:1 title ''
