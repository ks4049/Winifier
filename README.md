# Winifier
A text classifier for wine reviews crawled from http://winemag.com.

### We have developed two algorithms you can train on:
  1: Bernoulli Naive Bayes
  2: Multinomial Naive Bayes

### Training options:
  1: Cross Validation
  2: Percentage Split

### Steps to run: (If you are on a Unix / Mac System)
  ```
  git clone https://github.com/nirbhayph/Winifier.git
  cd Winifier
  pip3 install -r requirements.txt
  ```
  Now that the requirements are satisfied you can use the following options to run the program for training:

  `process (whether "train"/"test")``
  `filePath for training (path to dataset, "txt file delimited with ~")`
  `modelFilePath for testing with custom dataset (path to dataset, "txt file delimited with ~")`
  `algorithm (whether "bernoulli"/"multinomial")`
  `trainType (whether "percentage_split"/"cross_validation")`
  `trainPercentage (if "percentage_split" selected)`
  `numberOfFolds (if "cross_validation" selected)`
  `datasetLimit (number of rows to select from dataset)`

  #### Commands to train on dataset and evaluate on remaining subset of data:

  ##### Command Format:
  ```
  <python3 Winifier.py "train" "filePath" datasetLimit "algorithm" "trainType" "trainPercentage/numberOfFolds">
  ```

  ```
  python3 Winifier.py "train" "__data__/trainingV2.txt" 11110 "bernoulli" "percentage_split" 90
  ```

  ```
  python3 Winifier.py "train" "__data__/trainingV2.txt" 11110 "multinomial" "percentage_split" 90
  ```

  ```
  python3 Winifier.py "train" "__data__/trainingV2.txt" 11110 "bernoulli" "cross_validation" 10
  ```

  ```
  python3 Winifier.py "train" "__data__/trainingV2.txt" 11110 "multinomial" "cross_validation" 10
  ```

  #### Commands to custom test with a dataFile and modelFile:

  ```
  <python3 Winifier.py "test" "filePath" datasetLimit "modelFilePath">
  ```

  ```
  python3 Winifier.py "test" "__data__/trainingV2.txt" 1110 "__model__/generated/multinomial__percentage_split__90.json"
  ```
