# Winifier
A text classifier for wine reviews crawled from http://winemag.com.

### We have developed two algorithms you can train on:
  1: Bernoulli Naive Bayes
  2: Multinomial Naive Bayes

### Options:
  1: Cross Validation
  2: Percentage Split

### Steps to run:
  ```
  git clone https://github.com/nirbhayph/Winifier.git
  cd Winifier
  pip3 install -r requirements.txt
  ```
  Now that the requirements are satisfied you can use the following options to run the program:

  `process (whether "train"/"test")`

  `filePath for training (path to dataset, "txt file delimited with ~")`

  `modelFilePath for testing with custom dataset (path to dataset, "txt file delimited with ~")`

  `algorithm (whether "bernoulli"/"multinomial")`

  `type (whether "percentage_split"/"cross_validation")`

  `trainPercentage (if "percentage_split" selected)`

  `numberOfFolds (if "cross_validation" selected)`

  `datasetLimit (number of rows to select from dataset)`

  #### Commands to train on dataset and evaluate on remaining subset of data:

  ##### Command format:
  ```
  <python3 Winifier.py "train" "filePath" datasetLimit "algorithm" "type" "trainPercentage/numberOfFolds">
  ```
  ##### Sample commands to try out:
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
  ### Model Files are generated after each train command runs in the __model__/generated directory.

  #### Commands to custom test with a dataFile and modelFile:  
  #### This is under development, currently we have the option only to train and evaluate at run time! We plan to deliver this option through the next checkpoint
  ```
  <python3 Winifier.py "test" "filePath" datasetLimit "modelFilePath">
  ```
  ##### Sample commands to try out:
  ```
  python3 Winifier.py "test" "__data__/trainingV2.txt" 1110 "__model__/generated/multinomial__percentage_split__90.json"
  ```

  Link to repository: https://github.com/nirbhayph/Winifier.git
  You can visit this link to see updated ReadMe file if you wish to.
  
  @Authors (Team #5)
  `Khavya Seshadri`  `Dhiren Chandnani`  `Nirbhay Pherwani`
 
