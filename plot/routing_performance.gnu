set terminal pngcairo enhanced font "arial,12" size 600, 400
set output 'routing_performance.png'
set key inside right top vertical Right noreverse noenhanced autotitles
set style data boxes
set style fill solid border
set xrange [0:52500]
set xlabel 'Traceroute'
set ylabel 'Sum of Path Weights'
plot 'routing_performance.dat' using 2:xtic(1000) ti col fc rgb 'green',\
	 'routing_performance.dat' using 3 ti col fc rgb 'red'

