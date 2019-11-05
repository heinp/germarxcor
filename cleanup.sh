function clean {
	rm $1/*.htm*#*
	for elem in $1/*; do
		if [[ -d $elem ]]; then
			clean $elem;
		fi;
	done;
}

clean .
