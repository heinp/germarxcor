function clean {
	rm $1/*.htm*#*
	rm $1/index.htm*
	for elem in $1/*; do
		if [[ -d $elem ]]; then
			clean $elem;
		fi;
	done;
}

clean .
