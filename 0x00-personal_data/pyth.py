#!/usr/bin/env python3

import requests

url = "https://s3.amazonaws.com/alx-intranet.hbtn.io/uploads/misc/2019/11/a2e00974ce6b41460425.csv?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARDDGGGOUSBVO6H7D%2F20240208%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240208T141520Z&X-Amz-Expires=86400&X-Amz-SignedHeaders=host&X-Amz-Signature=96b810d8a0cc21584ba05f88a4e4c96480593bc41912cc0a1422ac06ab509a1c"

response = requests.get(url)

if response.status_code == 200:
    with open("user_data.csv", "wb") as file:
        file.write(response.content)
        print("CSV file downloaded successfully.")
else:
    print("Failed to download CSV file:", response.status_code)
