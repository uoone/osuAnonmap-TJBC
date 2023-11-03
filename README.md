# osuAnonmap
Essentially the same tool as https://github.com/pishifat/contest-anonymization#readme but in Python

Requirements:
tqdm (just for visualized progress bars)

Assumed inputs:
In the same directory as the code, put maps.zip. This should be a Zip file containing all the .osz files you want to anonymize.
Create token.json with the following format:
```
{
  "token": "<your legacy osuAPI token>"
}
```

Your API key can be found under the settings on your profilepage.

To run:
Navigate to the folder you stored this code and run main.py with
```
python ./main.py
```

In the output folder you will find a zip file containing anonymized .osz files. The .csv file you will find in there will be in the exact same format as MPG requires to un-fuck the anonymization.
For contest integrity, do NOT share the mask.csv. Do also NOT share token.json as that holds your personal osu API token.
