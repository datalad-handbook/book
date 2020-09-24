Code from chapter: usecase_ml
-----------------------------

Code snippet 195::

   datalad create imagenette


Code snippet 196::

   cd imagenette
   # 0.12.2 <= datalad < 0.13.4  needs the configuration option -c datalad.runtime.use-patool=1 to handle .tgz
   datalad -c datalad.runtime.use-patool=1 download-url \
     --archive \
     --message "Download Imagenette dataset" \
     'https://s3.amazonaws.com/fast-ai-imageclas/imagenette2-160.tgz' \


Code snippet 197::

   cd ../
   datalad create -c text2git -c yoda ml-project


Code snippet 198::

   cd ml-project
   mkdir -p data
   # install the dataset into data/
   datalad clone -d . ../imagenette data/raw


Code snippet 199::

   # show the directory hierarchy
   tree -d


Code snippet 200::

   datalad containers-add software --url shub://adswa/python-ml:1


Code snippet 201::

   cat << EOT > code/prepare.py
   #!/usr/bin/env python3

   import pandas as pd
   from pathlib import Path

   FOLDERS_TO_LABELS = {"n03445777": "golf ball",
                        "n03888257": "parachute"}


   def get_files_and_labels(source_path):
       images = []
       labels = []
       for image_path in source_path.rglob("*/*.JPEG"):
           filename = image_path
           folder = image_path.parent.name
           if folder in FOLDERS_TO_LABELS:
               images.append(filename)
               label = FOLDERS_TO_LABELS[folder]
               labels.append(label)
       return images, labels


   def save_as_csv(filenames, labels, destination):
       data_dictionary = {"filename": filenames, "label": labels}
       data_frame = pd.DataFrame(data_dictionary)
       data_frame.to_csv(destination)


   def main(repo_path):
       data_path = repo_path / "data"
       train_path = data_path / "raw/imagenette2-160/train"
       test_path = data_path / "raw/imagenette2-160/val"
       train_files, train_labels = get_files_and_labels(train_path)
       test_files, test_labels = get_files_and_labels(test_path)
       save_as_csv(train_files, train_labels, data_path / "train.csv")
       save_as_csv(test_files, test_labels, data_path / "test.csv")


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT


Code snippet 202::

   datalad status


Code snippet 203::

   datalad save -m "Add script for data preparation for 2 categories" code/prepare.py


Code snippet 204::

   datalad containers-run -n software \
     -m "Prepare the data for categories golf balls and parachutes" \
     --input 'data/raw/imagenette2-160/train/n03445777' \
     --input 'data/raw/imagenette2-160/val/n03445777' \
     --input 'data/raw/imagenette2-160/train/n03888257' \
     --input 'data/raw/imagenette2-160/val/n03888257' \
     --output 'data/train.csv' \
     --output 'data/test.csv' \
     "python3 code/prepare.py"


Code snippet 205::

   cat << EOT > code/train.py
   #!/usr/bin/env python3

   from joblib import dump
   from pathlib import Path

   import numpy as np
   import pandas as pd
   from skimage.io import imread_collection
   from skimage.transform import resize
   from sklearn.linear_model import SGDClassifier


   def load_images(data_frame, column_name):
       filelist = data_frame[column_name].to_list()
       image_list = imread_collection(filelist)
       return image_list


   def load_labels(data_frame, column_name):
       label_list = data_frame[column_name].to_list()
       return label_list


   def preprocess(image):
       resized = resize(image, (100, 100, 3))
       reshaped = resized.reshape((1, 30000))
       return reshaped


   def load_data(data_path):
       df = pd.read_csv(data_path)
       labels = load_labels(data_frame=df, column_name="label")
       raw_images = load_images(data_frame=df, column_name="filename")
       processed_images = [preprocess(image) for image in raw_images]
       data = np.concatenate(processed_images, axis=0)
       return data, labels


   def main(repo_path):
       train_csv_path = repo_path / "data/train.csv"
       train_data, labels = load_data(train_csv_path)
       sgd = SGDClassifier(max_iter=10)
       trained_model = sgd.fit(train_data, labels)
       dump(trained_model, repo_path / "model.joblib")


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT


Code snippet 206::

   datalad save -m "Add SGD classification script" code/train.py


Code snippet 207::

   cat << EOT > code/evaluate.py

   #!/usr/bin/env python3

   from joblib import load
   import json
   from pathlib import Path

   from sklearn.metrics import accuracy_score

   from train import load_data


   def main(repo_path):
       test_csv_path = repo_path / "data/test.csv"
       test_data, labels = load_data(test_csv_path)
       model = load(repo_path / "model.joblib")
       predictions = model.predict(test_data)
       accuracy = accuracy_score(labels, predictions)
       metrics = {"accuracy": accuracy}
       print(metrics)
       accuracy_path = repo_path / "accuracy.json"
       accuracy_path.write_text(json.dumps(metrics))


   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT


Code snippet 208::

   datalad save -m "Add script to evaluate model performance" --version-tag "ready4analysis" code/evaluate.py


Code snippet 209::

   datalad containers-run -n software \
     -m "Train an SGD classifier on the data" \
     --input 'data/raw/imagenette2-160/train/*' \
     --output 'model.joblib' \
     "python3 code/train.py"


Code snippet 210::

   datalad containers-run -n software \
     -m "Evaluate SGD classifier on test data" \
     --input 'data/raw/imagenette2-160/val/*' \
     --output 'accuracy.json' \
     "python3 code/evaluate.py"


Code snippet 211::

   sed -i 's/SGDClassifier(max_iter=10)/SGDClassifier(max_iter=100)/g' code/train.py


Code snippet 212::

   git diff


Code snippet 213::

   datalad save -m "Increase the amount of iterations to 100" --version-tag "SGD-100" code/train.py


Code snippet 214::

   datalad rerun -m "Recompute classification with more iterations" ready4analysis..SGD-100


Code snippet 215::

   cat << EOT >| code/train.py
   #!/usr/bin/env python3

   from joblib import dump
   from pathlib import Path

   import numpy as np
   import pandas as pd
   from skimage.io import imread_collection
   from skimage.transform import resize
   from sklearn.ensemble import RandomForestClassifier

   def load_images(data_frame, column_name):
       filelist = data_frame[column_name].to_list()
       image_list = imread_collection(filelist)
       return image_list

   def load_labels(data_frame, column_name):
       label_list = data_frame[column_name].to_list()
       return label_list

   def preprocess(image):
       resized = resize(image, (100, 100, 3))
       reshaped = resized.reshape((1, 30000))
       return reshaped

   def load_data(data_path):
       df = pd.read_csv(data_path)
       labels = load_labels(data_frame=df, column_name="label")
       raw_images = load_images(data_frame=df, column_name="filename")
       processed_images = [preprocess(image) for image in raw_images]
       data = np.concatenate(processed_images, axis=0)
       return data, labels

   def main(repo_path):
       train_csv_path = repo_path / "data/train.csv"
       train_data, labels = load_data(train_csv_path)
       rf = RandomForestClassifier()
       trained_model = rf.fit(train_data, labels)
       dump(trained_model, repo_path / "model.joblib")

   if __name__ == "__main__":
       repo_path = Path(__file__).parent.parent
       main(repo_path)
   EOT


Code snippet 216::

   datalad save -m "Switch to random forest classification" --version-tag "random-forest" code/train.py


Code snippet 217::

   datalad rerun --branch="randomforest" -m "Recompute classification with random forest classifier" ready4analysis..SGD-100


Code snippet 218::

   git diff master -- accuracy.json


Code snippet 219::

   git checkout master
   cat accuracy.json


