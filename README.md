# Human Classifier

A simple Python app to classify GAN-generated images. There are two models to choose from: a high-quality (HQ) model with challenging images and a low-quality (LQ) model with relatively more straightforward digits. Each model has a total of nine classes, with each class containing 100 images.
## Installation

```bash
pip install pillow
```
## Usage

* Clone this repository
  ```bash
  git clone https://github.com/WafaAmr/Human-Classifier.git
  ```
* Uncomment one of the models in the code
  ```python
  5: # model = 'HQ'
  6: # model = 'LQ'
  ```
* Run the code
  ```bash
  python human_classifier.py
  ```
* Use the **the number keys** <kbd>1-9</kbd> or the GUI to classify the images. The <kbd>enter</kbd> key is mapped to the unknown class.

* The results will be saved in a TXT file named `<MODEL>-labels.txt`
