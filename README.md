# Africa_corporate_irrigation
 Project exploring drivers of corporate irrigation expansion

## Instructions

1. Install [Conda](http://conda.io/)

2. Create environment and install requirements

```bash
conda create -n irrigation python=3.12 -y
conda activate irrigation
pip install -r requirements.txt
```

3. Add data

### Shapefile containing Center Pivots across the World

You can obtain the shp file containing the world's center pivots [here](https://github.com/DetectCPIS/global_cpis_shp). 

To extract the Center Pivots identified in 2021, download all files in [this folder](https://github.com/DetectCPIS/global_cpis_shp/tree/main/World_CPIS_2021) and run the following code in the terminal: 

```{bash}
cd ~/Downloads 
zip -s 0 World_CPIS_2021.zip --out World_CPIS_2021_together.zip
unzip World_CPIS_2021_together.zip
```
The data from 2000 can be obtained analogously. 

### Other data

All data is either created using the code in this repository or can be downloaded elsewhere. Refer to the `config.yaml` file for links to and descriptions of datasets. 

4. Run the files

Run the files in the order their numbered names suggest in order to recreate the entire project. 