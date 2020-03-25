# Install python dependencies
pip install -r requirements.txt

# Download & configure Google object_detection API
git clone https://github.com/tensorflow/models.git
cd models/research
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim
python setup.py build
python setup.py install


python detection_utils\generate_csv.py xml data\Annotations\ data\annotation.csv
python detection_utils\generate_pbtxt.py csv data\annotation.csv data\labelmap.pbtxt
python detection_utils\generate_train_eval.py data\annotation.csv -f 0.95
