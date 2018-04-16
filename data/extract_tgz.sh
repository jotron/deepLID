# copied from https://github.com/twerkmeister/iLID/tree/master/data/voxforge and edited
if [ $# -lt 2 ]; then
  echo "Usage: $0 <tgz file> <language>"
  exit 1
fi

ZIP=$1
LANG=$2
TEMP_DIR=$(dirname $ZIP)
FILE_NAME=$(basename $ZIP)
STRIPPED_FILE_NAME=${FILE_NAME%.tgz}
STRIPPED_FILE_NAME_WITHOUT=${STRIPPED_FILE_NAME#n}

tar -xf $ZIP -C $TEMP_DIR

UNZIPPED_FOLDER=$TEMP_DIR/$STRIPPED_FILE_NAME
UNZIPPED_FOLDER_WITHOUT=$TEMP_DIR/$STRIPPED_FILE_NAME_WITHOUT
WAVES=$UNZIPPED_FOLDER_WITHOUT/wav

if [ ! -d $LANG ]; then
  mkdir $LANG
fi

for WAVE in $(ls $WAVES)
do
  mv $WAVES/$WAVE $LANG/$STRIPPED_FILE_NAME-$WAVE
done

rm -f $ZIP
rm -rf $UNZIPPED_FOLDER_WITHOUT
