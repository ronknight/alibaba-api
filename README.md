<p><a target="_blank" href="https://app.eraser.io/workspace/Myn74V7c2RK4JrPk9V2j" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

<h1 align="center"><a href="https://github.com/ronknight/alibaba-api">Alibaba API Client</a></h1>
<h4 align="center">This Python script demonstrates how to interact with the Taobao API to retrieve product information. It uses the `requests` library to make HTTP POST requests and the `dotenv` library to load environment variables from a `.env` file.</h4>

<p align="center">
<a href="https://twitter.com/PinoyITSolution"><img src="https://img.shields.io/twitter/follow/PinoyITSolution?style=social"></a>
<a href="https://github.com/ronknight?tab=followers"><img src="https://img.shields.io/github/followers/ronknight?style=social"></a>
<a href="https://github.com/ronknight/ronknight/stargazers"><img src="https://img.shields.io/github/stars/BEPb/BEPb.svg?logo=github"></a>
<a href="https://github.com/ronknight/ronknight/network/members"><img src="https://img.shields.io/github/forks/BEPb/BEPb.svg?color=blue&logo=github"></a>
  <a href="https://youtube.com/@PinoyITSolution"><img src="https://img.shields.io/youtube/channel/subscribers/UCeoETAlg3skyMcQPqr97omg"></a>
<a href="https://github.com/ronknight/alibaba-api/issues"><img src="https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat"></a>
<a href="https://github.com/ronknight/alibaba-api/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg"></a>
<a href="#"><img src="https://img.shields.io/badge/Made%20with-Python-1f425f.svg"></a>
<a href="https://github.com/ronknight"><img src="https://img.shields.io/badge/Made%20with%20%F0%9F%A4%8D%20by%20-%20Ronknight%20-%20red"></a>
</p>

<p align="center">
  <a href="#prerequisites">Prerequisites</a> •
  <a href="#usage">Usage</a> •
  <a href="#magic">Magic</a> •
  <a href="#diagrams">Diagrams</a> •
</p>

---

## Prerequisites
Before running the script, make sure you have the following:

1. Python installed on your system.
2. `requests`  and `python-dotenv`  libraries installed. You can install them using `pip` :
```bash
pip install requests python-dotenv
```
1. A `.env`  file in the same directory as the script, containing your Taobao API credentials. The format should be:
```bash
APP_KEY=your_app_key
APP_SECRET=your_app_secret
ACCESS_TOKEN=your_access_token
```
Replace `your_app_key`, `your_app_secret`, and `your_access_token` with your actual API credentials.

## Usage
1. Save the `main.py`  script in a directory of your choice.
2. Create a `.env`  file in the same directory and add your API credentials as mentioned above.
3. Open a terminal or command prompt, navigate to the directory containing the script, and run the following command:
```bash
python main.py
```
The script will make a POST request to the Taobao API, and the response will be printed to the console.

## Magic
1. The script loads the environment variables from the `.env`  file using the `load_dotenv`  function from the `dotenv`  library.
2. It constructs the URL and payload for the POST request using the API credentials and other required parameters.
3. The payload parameters are sorted alphabetically, concatenated, and combined with the `APP_SECRET`  to create a string to sign.
4. The string to sign is hashed using the MD5 algorithm, and the resulting hash is converted to uppercase to generate the signature.
5. The signature is added to the payload, and a POST request is made to the Taobao API endpoint using the `requests.post`  function.
6. The API response is printed to the console.
Note: This script is for demonstration purposes only. You may need to modify the API endpoint and parameters based on your specific use case and the Taobao API documentation.


<!-- eraser-additional-content -->
## Diagrams
<!-- eraser-additional-files -->
<a href="/README-Alibaba API Client Interaction-1.eraserdiagram" data-element-id="AEL4JksdF87F6dg5VG1m0"><img src="/.eraser/Myn74V7c2RK4JrPk9V2j___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----dd95c05bc6f05a6355ed26be6e907103-Alibaba-API-Client-Interaction.png" alt="" data-element-id="AEL4JksdF87F6dg5VG1m0" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/Myn74V7c2RK4JrPk9V2j --->