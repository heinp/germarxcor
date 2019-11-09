for path_to_html in ../html/$1/*/*; do
    echo $path_to_html
    python3 transform_to_tei.py $path_to_html
done;

