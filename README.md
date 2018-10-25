# Resume-Filter
Extracting relevant information from resume using Deep Learning.

## Getting Started
### Requirements
Code successfully runs with:
```
python 3.6.5
numpy 1.13.3
pandas 0.23.0
keras 2.1.5
pdfminer
```
### Usage
1.Put the resume in ``` data/training_data``` folder. Currently only ```.pdf``` and ```.docx``` format supported.

2. Run ```utils/create_training_data.py```. A popup will be created. Annote the lines of resume in the same.
   
3.Run ```start_training.py```.

4.Trained model will be saved in ```trained_model``` folder.

5.Put the resume to parse in ```data/resume_to_parse``` folder. Only ```.pdf``` and ```.docx``` format supported.

6.Run ```predict.py```



