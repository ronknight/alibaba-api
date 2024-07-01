<p><a target="_blank" href="https://app.eraser.io/workspace/Myn74V7c2RK4JrPk9V2j" id="edit-in-eraser-github-link"><img alt="Edit in Eraser" src="https://firebasestorage.googleapis.com/v0/b/second-petal-295822.appspot.com/o/images%2Fgithub%2FOpen%20in%20Eraser.svg?alt=media&amp;token=968381c8-a7e7-472a-8ed6-4a6626da5501"></a></p>

<h1 align="center"><a href="https://github.com/ronknight/alibaba-api">Alibaba API Client</a></h1>
<h4 align="center">This Python project demonstrates how to interact with the Alibaba/Taobao API to retrieve product information and manage authentication. It uses the `requests` library to make HTTP requests and the `dotenv` library to load environment variables from a `.env` file.</h4>

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
  <a href="#features">Features</a> •
  <a href="#diagrams">Diagrams</a>
</p>

---
## Prerequisites
Before running the scripts, make sure you have the following:

1. Python installed on your system.
2. Required libraries installed. You can install them using `pip` :pip install requests python-dotenv
3. A .env file in the project directory containing your Alibaba/Taobao API credentials:APP_KEY=your_app_key
APP_SECRET=your_app_secret
REDIRECT_URI=your_redirect_uri
SESSION_KEY=your_session_key
AUTH_CODE=your_auth_code
## Usage
1. Clone the repository:git clone https://github.com/ronknight/alibaba-api.git
cd alibaba-api
2. Set up your `.env`  file with the required credentials.
3. Run the scripts as needed (see the Scripts section for details on each script).
## Features
1. **Authentication**: Handles the OAuth 2.0 flow for Alibaba/Taobao API.
2. **Token Management**: Creates and manages access tokens.
3. **Product Management**: Retrieves, updates, adds, and manages product information.
4. **Group Management**: Retrieves product group information.
5. **Category Management**: Retrieves category information and attributes.
6. **Shipping Management**: Retrieves shipping line template information.
7. **Photobank Management**: Lists, operates, and manages photobank groups.
8. **Logging**: Comprehensive logging of API requests and responses.
9. **Error Handling**: Robust error handling and reporting.
## Scripts
### 1. Product List (productlist.py)
Retrieves a list of products based on search criteria.

```bash
python productlist.py <subject> <page_size>
```
### 2. Product Get (productget.py)
Retrieves detailed information about a specific product.

```bash
python productget.py <product_id>
```
### 3. Product Group Get (productgroupget.py)
Retrieves information about a product group.

```bash
python productgroupget.py <group_id>
```
### 4. Product ID Decrypt (productiddecrypt.py)
Decrypts a product ID.

```bash
python productiddecrypt.py <product_id>
```
### 5. Product Schema (productschema.py)
Retrieves the schema for product information.

```bash
python productschema.py
```
### 6. Product Update Field (productupdatefield.py)
Updates specific fields of a product.

```bash
python productupdatefield.py <product_id>
```
### 7. Product Update Field Copy (productupdatefieldcopy.py)
A variation of the product update field script, focusing on updating the InternalSKU.

```bash
python productupdatefieldcopy.py <product_id>
```
### 8. Wholesale Shipping Line Template (wholesaleshippinglinetemplate.py)
Retrieves the list of shipping line templates.

```bash
python wholesaleshippinglinetemplate.py
```
### 9. Category Attribute Get (categoryattributeget.py)
Retrieves attributes for a specific category.

```bash
python categoryattributeget.py <cat_id>
```
### 10. Category Get (categoryget.py)
Retrieves information about a specific category.

```bash
python categoryget.py <cat_id>
```
### 11. Photobank Group List (photobankgrouplist.py)
Retrieves a list of photobank groups.

```bash
python photobankgrouplist.py
```
### 12. Photobank Group Operate (photobankgroupoperate.py)
Performs operations on photobank groups (add, delete, rename).

```bash
python photobankgroupoperate.py <group_name> <operation>
```
### 13. Photobank List (photobanklist.py)
Retrieves a list of photos from the photobank.

```bash
python photobanklist.py <page_size>
```
### 14. Product Add (productadd.py)
Adds a new product to the catalog.

```bash
python productadd.py
```
### 15. Product Batch Update Display (productbatchupdatedisplay.py)
Updates the display status for multiple products at once.

```bash
python productbatchupdatedisplay.py <new_display> <product_id_list>
```
Each script includes error handling and logging functionality. Logs are stored in the `api_logs/` directory.

<!-- eraser-additional-content -->
## Diagrams
<!-- eraser-additional-files -->
<a href="/README-Alibaba API Client Architecture-1.eraserdiagram" data-element-id="f6_L4NLrps7uMfYCSculN"><img src="/.eraser/Myn74V7c2RK4JrPk9V2j___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----48afec3820aca91f6e05a19aff0cd382-Alibaba-API-Client-Architecture.png" alt="" data-element-id="f6_L4NLrps7uMfYCSculN" /></a>
<a href="/README-Alibaba API Client Interaction-2.eraserdiagram" data-element-id="Yf6aJmVxktkzt7wHNqWc7"><img src="/.eraser/Myn74V7c2RK4JrPk9V2j___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----aaffa2b1de5395a0d71d31d419f0bcef-Alibaba-API-Client-Interaction.png" alt="" data-element-id="Yf6aJmVxktkzt7wHNqWc7" /></a>
<a href="/README-Alibaba API Client Flowchart-3.eraserdiagram" data-element-id="JT3PX6weOeXQu_PBt509X"><img src="/.eraser/Myn74V7c2RK4JrPk9V2j___3Jivg2tjMecMlrHwbIVIBR8f7U03___---diagram----169864538c902ec23d1849297e93715e-Alibaba-API-Client-Flowchart.png" alt="" data-element-id="JT3PX6weOeXQu_PBt509X" /></a>
<!-- end-eraser-additional-files -->
<!-- end-eraser-additional-content -->
<!--- Eraser file: https://app.eraser.io/workspace/Myn74V7c2RK4JrPk9V2j --->


Note: This project is for demonstration purposes only. You may need to modify the scripts based on your specific use case and the latest Alibaba/Taobao API documentation.

```
This comprehensive README now includes information about all the scripts in the project, providing a clear overview of each script's functionality and usage instructions. The structure remains consistent with the original README, while incorporating details about all the new scripts.
```

