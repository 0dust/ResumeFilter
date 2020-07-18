# Resume-Filter
Extracting relevant information from resume using Deep Learning.

## Getting Started
### Installation

Steps:
It is recommended to do the installation in anaconda virtual environment to avoid issues with dependencies.
You can skip creating conda virtual environment(at your own risk!)
1. Run ``` conda create --name resumefilter python=3.7.6 ```
2. ``` conda activate resumefilter ```
3. ``` git clone https://github.com/0dust/ResumeFilter.git ```
4. ``` cd ResumeFilter ```
5. ``` pip install -U setuptools ```
6. ``` pip install -e . ```

## Usage
### Data Preparation

Getting training data is most challenging part due to lack of publicaly available dataset of resume. Currently, to create 
training data you will have to manually label the lines of resume.

1.Put the resume in ``` data/training_data``` folder. Currently only ```.pdf``` and ```.docx``` format supported.

2.Run ```utils/create_training_data.py```. A popup will be created. Annote the lines of resume in the same.

### Training   
3.Run ```start_training.py```.

4.Trained model will be saved in ```trained_model``` folder.
### Ready to use!
5.Put the resume to parse in ```data/resume_to_parse``` folder. Only ```.pdf``` and ```.docx``` format supported.

6.Run ```predict.py```



