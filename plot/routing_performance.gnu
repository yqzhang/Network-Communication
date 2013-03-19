set terminal pngcairo enhanced font "arial,12" size 600, 400
set output 'routing_performance.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set grid
set style data boxes
set xtic scale 0
#set format y '%g %%'
#set format x '%g %%'
#set yrange [0:100]
#set xlabel 'Percentage of accessable traceroutes during the failure'
plot 'routing_performance.dat' using 2:xtic(1) ti col fc rgb 'green',\
	 'routing_performance.dat' using 3 ti col fc rgb 'red'

