If executing the code below returns an exit code of 9009, there may be no ``python3`` -- instead, it is called just ``python``.
Please run the following instead (adjusted for line breaks, you should be able to copy-paste this as a whole):

.. code-block:: console

  > datalad run -m "analyze iris data with classification analysis" ^
   --input "input/iris.csv" ^
   --output "pairwise_relationships.png" ^
   --output "prediction_report.csv" ^
   "python code/script.py {inputs} {outputs}"
