Code from chapter: 10_yoda
--------------------------

Code snippet 126::

   # inside of DataLad-101
   datalad create -c yoda --dataset . midterm_project


Code snippet 127::

   cd midterm_project
   # we are in midterm_project, thus -d . points to the root of it.
   datalad clone -d . https://github.com/datalad-handbook/iris_data.git input/


Code snippet 128::

   cd ../
   tree -d
   cd midterm_project


Code snippet 129::

   cat << EOT > code/script.py

   import pandas as pd
   import seaborn as sns
   import datalad.api as dl
   from sklearn import model_selection
   from sklearn.neighbors import KNeighborsClassifier
   from sklearn.metrics import classification_report

   data = "input/iris.csv"

   # make sure that the data are obtained (get will also install linked sub-ds!):
   dl.get(data)

   # prepare the data as a pandas dataframe
   df = pd.read_csv(data)
   attributes = ["sepal_length", "sepal_width", "petal_length","petal_width", "class"]
   df.columns = attributes

   # create a pairplot to plot pairwise relationships in the dataset
   plot = sns.pairplot(df, hue='class', palette='muted')
   plot.savefig('pairwise_relationships.png')

   # perform a K-nearest-neighbours classification with scikit-learn
   # Step 1: split data in test and training dataset (20:80)
   array = df.values
   X = array[:,0:4]
   Y = array[:,4]
   test_size = 0.20
   seed = 7
   X_train, X_test, Y_train, Y_test = model_selection.train_test_split(X, Y,
                                                                       test_size=test_size,
                                                                       random_state=seed)
   # Step 2: Fit the model and make predictions on the test dataset
   knn = KNeighborsClassifier()
   knn.fit(X_train, Y_train)
   predictions = knn.predict(X_test)

   # Step 3: Save the classification report
   report = classification_report(Y_test, predictions, output_dict=True)
   df_report = pd.DataFrame(report).transpose().to_csv('prediction_report.csv')

   EOT


Code snippet 130::

   datalad status


Code snippet 131::

   datalad save -m "add script for kNN classification and plotting" --version-tag ready4analysis code/script.py


Code snippet 132::

   datalad run -m "analyze iris data with classification analysis" \
     --input "input/iris.csv" \
     --output "prediction_report.csv" \
     --output "pairwise_relationships.png" \
     "python3 code/script.py"


Code snippet 133::

   git log --oneline


Code snippet 134::

   # with the >| redirection we are replacing existing contents in the file
   cat << EOT >| README.md

   # Midterm YODA Data Analysis Project

   ## Dataset structure

   - All inputs (i.e. building blocks from other sources) are located in input/.
   - All custom code is located in code/.
   - All results (i.e., generated files) are located in the root of the dataset:
     - "prediction_report.csv" contains the main classification metrics.
     - "output/pairwise_relationships.png" is a plot of the relations between features.

   EOT


Code snippet 135::

   datalad status


Code snippet 136::

   datalad save -m "Provide project description" README.md


Code snippet 137::

   # we are in the midterm_project subdataset
   datalad containers-add midterm-software --url shub://adswa/resources:1


Code snippet 138::

   git log -n 1 -p


Code snippet 139::

   datalad containers-run -m "rerun analysis in container" \
     --container-name midterm-software \
     --input "input/iris.csv" \
     --output "prediction_report.csv" \
     --output "pairwise_relationships.png" \
     "python3 code/script.py"


Code snippet 140::

   git log -p -n 1


Code snippet 141::

   cd ../
   datalad status


Code snippet 142::

   datalad save -d . -m "add container and execute analysis within container" midterm_project
