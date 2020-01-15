CURRENT_DIR=$(pwd)
WORK_DIR="./cervix_dataset"
CERVIX_ROOT="${WORK_DIR}/dataset"
SEG_FOLDER="${CERVIX_ROOT}/SegmentationClass"
SEMANTIC_SEG_FOLDER="${CERVIX_ROOT}/SegmentationClassRaw"
# Build TFRecords of the dataset.
OUTPUT_DIR="${WORK_DIR}/tfrecord"
mkdir -p "${OUTPUT_DIR}"
IMAGE_FOLDER="${CERVIX_ROOT}/JPEGImages"
LIST_FOLDER="${CERVIX_ROOT}/ImageSets"
echo "Converting Cervix dataset..."
python3 ./build_new_pqr_data.py \
  --image_folder="${IMAGE_FOLDER}" \
  --semantic_segmentation_folder="${SEMANTIC_SEG_FOLDER}" \
  --list_folder="${LIST_FOLDER}" \
  --image_format="png" \
  --output_dir="${OUTPUT_DIR}"
