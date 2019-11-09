for path_to_html in ../html/marx_engels/*/*; do
    echo $path_to_html
    folder="$(dirname $path_to_html)"
    folder="$(basename $folder)"
    path_to_tei=../tei/marx_engels/$folder/$(basename "$path_to_html" .htm).xml 
    python3 transform_to_tei.py $path_to_html $path_to_tei
done;

