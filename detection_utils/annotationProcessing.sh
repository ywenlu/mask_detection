# Install python dependencies
pip install -r requirements.txt

# Download & configure Google object_detection API
git clone https://github.com/tensorflow/models.git
cd models/research
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
python setup.py build
python setup.py install


python detection_utils\generate_csv.py xml mergedData\Annotations\ mergedData\annotation.csv
python detection_utils\generate_pbtxt.py csv mergedData\annotation.csv mergedData\labelmap.pbtxt
python detection_utils\generate_train_eval.py mergedData\annotation.csv -f 0.95
python detection_utils\generate_tfrecord.py mergedData\annotation_train.csv mergedData\labelmap.pbtxt mergedData\JPEGImages\ mergedData\train.record
python detection_utils\generate_tfrecord.py mergedData\annotation_eval.csv mergedData\labelmap.pbtxt mergedData\JPEGImages\ mergedData\eval.record

