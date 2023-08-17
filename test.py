import subprocess
import os 

# commmand = "cat metrics.yaml | yq '.s'"
# output = subprocess.check_output(commmand, shell=True, text=True).splitlines()
# value = output[0]

# if value == 'null':
#     print("No metrics")
b = f"""
yq -i '
  .cfr = "25%" |
  .total_releases = "4" |
  .total_features = "13" |
  .total_bugs = "6" |
  .total_hotfixes = "6" |
  .release_1.features = "4" |
  .release_1.bugs = "0" |
  .release_1.hotfixes = "1" |
  .release_1.deployments = "5" |
  .release_2.features = "5" |
  .release_2.bugs = "2" |
  .release_2.hotfixes = "0" |
  .release_2.deployments = "0" 
' metrics.yaml
"""

res = subprocess.getoutput(b)
print(res)