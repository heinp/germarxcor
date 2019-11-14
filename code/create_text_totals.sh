for dir in ../txt/*; do
    if [[ -d $dir ]]; then
        cat $dir/*/* > $dir/$(basename $dir)_total.txt
    fi
done
cat ../txt/*/*_total.txt > ../txt/total.txt
