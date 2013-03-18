set terminal pngcairo enhanced font "arial,12" size 600, 400
set output 'accessibility.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set grid
set style data lines
set format y '%g %%'
set format x '%g %%'
set yrange [0:100]
set xlabel 'Percentage of accessable traceroutes during the failure'
plot 'accessibility.dat' using ($1/100):($2*100) title 'CDF'

