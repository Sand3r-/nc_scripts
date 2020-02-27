if [ $# -eq 0 ]
  then
    echo "Please run as source $0 path_to_release"
fi

GLTF_FILE="$1"/../Final.gltf
FILES=output/*
for f in $FILES
do
  name=$(basename -- $f)
  no_ext=$(basename $name ".rgb8a1.ktx")
  name_ktx=${no_ext}.ktx
  if test -f "$1"/"$name_ktx"; then
    echo "Changing name from $name_ktx to $name in file $GLTF_FILE"
    sed -i "s/$name_ktx/$name/g" "$GLTF_FILE"
    echo "Copying file $f as it exists there"
    cp $f "$1"/"$name"
    echo "Removing file $name_ktx"
    rm "$1"/"$name_ktx"
  fi
done


