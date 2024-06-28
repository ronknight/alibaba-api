import os
import sys
import requests
import hashlib
import time
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve variables from environment
app_key = os.getenv('APP_KEY')
app_secret = os.getenv('APP_SECRET')
session_key = os.getenv('SESSION_KEY')

# Define the log directory
LOG_DIR = 'api_logs/'  # Directory to store log files
os.makedirs(LOG_DIR, exist_ok=True)  # Create directory if it doesn't exist

# API endpoint and parameters
url = 'https://eco.taobao.com/router/rest'

# Check if product_id is provided as command-line argument
if len(sys.argv) < 2:
    print("Usage: python productupdate.py <product_id>")
    sys.exit(1)

product_id = sys.argv[1]  # Get product_id from command-line argument

# Example of request parameters for updating specific fields of a product
params = {
    'app_key': app_key,
    'format': 'json',
    'method': 'alibaba.icbu.product.update.field',
    'partner_id': 'apidoc',
    'session': session_key,
    'sign_method': 'md5',
    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S"),
    'v': '2.0',
    'language': 'ENGLISH',  # Set language to English
    'product_id': product_id,  # Product ID from command-line argument
    'attributes': json.dumps({
        'product_attribute': [
            {
                'attribute_id': 100004405,
                'value_id': 3346829,  # Updated value ID for 'Painting Paper Type' to 'Pencil'
            },
            {
                'attribute_id': 191288006,
                'value_id': 3623298,  # Updated value ID for 'Use' to 'Gift'
            },
            {
                'attribute_id': 191288065,
                'value_id': 3291889,  # Updated value ID for 'Cover Material' to 'Paper'
            },
            {
                'attribute_id': 1,
                'value_name': 'US',  # Updated value for 'Place of Origin' to 'US'
            },
            {
                'attribute_id': 3,
                'value_name': '54401',  # Updated value for 'Model Number' to '54401'
            }
        ]
    }),
    'category_id': 201460532,  # Updated category ID
    'description': "<div id=\"ali-anchor-AliPostDhMb-nrc2y\" class=\"mceSectionContainer\" style=\"padding-top: 8px;\" data-section=\"AliPostDhMb-nrc2y\" data-section-title=\"Product Description\">\n<div id=\"ali-title-AliPostDhMb-nrc2y\" style=\"padding: 8px 0; border-bottom: 1px solid #ddd;\"><span style=\"background-color: #ddd; color: #333; font-weight: bold; padding: 8px 10px; line-height: 12px;\">Product Description</span></div>\n<div style=\"padding: 10px 0;\">\n<p><span style=\"color: #000000; font-size: 14px; font-style: normal; font-weight: 400; text-align: left;\">Aladdin coloring and activity book is perfect for children to color and complete fun activities that feature Disney characters from the popular Aladdin film. It comes in two assortments. Great buy products like these are perfect for your book section.<br /><br />Make big sales and stock up on this Aladdin coloring and activity book. It's ideal for dollar stores, discount stores, book stores and many other businesses.</span></p>\n</div>\n</div>\n<div id=\"ali-anchor-AliPostDhMb-ou0l5\" class=\"mceSectionContainer\" style=\"padding-top: 8px;\" data-section=\"AliPostDhMb-ou0l5\" data-section-title=\"Packaging &amp; Shipping\">\n<div id=\"ali-title-AliPostDhMb-ou0l5\" style=\"padding: 8px 0; border-bottom: 1px solid #ddd;\"><span style=\"background-color: #ddd; color: #333; font-weight: bold; padding: 8px 10px; line-height: 12px;\">Packaging &amp; Shipping</span></div>\n<div style=\"padding: 10px 0;\">\n<p>Case Pack:&nbsp;36 Case Pack<br />Piece Price: $0.65 Each<br />Case Price: $23.4 per Case Pack<br />Country of Origin: CHINA<br />Case Cube (cu. ft.):&nbsp;0.48<br />Case Weight (lbs.):10.35<br />Casepack Dimension: 16.2L x 11.3W x 4.5H<br />UPC Number :810051460445<br />Product Color:&nbsp;MILTICOLOR<br />Pallet Qty: 90<br />SKU:&nbsp;54401</p>\n</div>\n</div>\n<div id=\"ali-anchor-AliPostDhMb-2tgir\" class=\"mceSectionContainer\" style=\"padding-top: 8px;\" data-section=\"AliPostDhMb-2tgir\" data-section-title=\"Company Information\">\n<div id=\"ali-title-AliPostDhMb-2tgir\" style=\"padding: 8px 0; border-bottom: 1px solid #ddd;\"><span style=\"background-color: #ddd; color: #333; font-weight: bold; padding: 8px 10px; line-height: 12px;\">Company Information</span></div>\n<div style=\"padding: 10px 0;\">\n<p><span style=\"font-size: 12px;\">&nbsp;</span></p>\n<p><span style=\"font-size: 12px;\">4SGM Whosale Online Store - <a href=\"https://us1344727002uqin.trustpass.alibaba.com/?spm=a2700.shop_pl.88.13\" target=\"_blank\" rel=\"noopener noreferrer\">https://4sgm.com</a></span></p>\n</div>\n</div>\n<div id=\"ali-anchor-AliPostDhMb-uvth3\" class=\"mceSectionContainer\" style=\"padding-top: 8px;\" data-section=\"AliPostDhMb-uvth3\" data-section-title=\"FAQ\">\n<div id=\"ali-title-AliPostDhMb-uvth3\" style=\"padding: 8px 0; border-bottom: 1px solid #ddd;\"><span style=\"background-color: #ddd; color: #333; font-weight: bold; padding: 8px 10px; line-height: 12px;\">FAQ</span></div>\n<div style=\"padding: 10px 0;\">\n<p><span style=\"font-size: 12px;\"><strong>Q: What is the minimum order amount?</strong></span><br /><span style=\"font-size: 12px;\">A:The minimum order amount is $1,000. We don't process orders under $1000. Please mix and match with our other inventory to meet the minimum.</span></p>\n<p style=\"border: 0px solid #e3e3e3; box-sizing: border-box; margin: 1.25em 0px; color: #0d0d0d; font-family: sans-serif,Arial; font-size: 16px; font-style: normal; font-weight: 400; background-color: #ffffff;\"><span style=\"font-size: 12px;\"><strong>Q: Can I place my order through Alibaba?</strong></span><br /><span style=\"font-size: 12px;\">A: Yes, you can place your order through Alibaba. However, please note that orders placed through Alibaba will serve as price quotes only.</span></p>\n<p style=\"border: 0px solid #e3e3e3; box-sizing: border-box; margin: 1.25em 0px; color: #0d0d0d; font-family: sans-serif,Arial; font-size: 16px; font-style: normal; font-weight: 400; background-color: #ffffff;\"><span style=\"font-size: 12px;\"><strong>Q: Can I mix and match different products in my order?</strong></span><br /><span style=\"font-size: 12px;\">A: Yes, you are welcome to mix and match different products in your order.</span></p>\n<p style=\"border: 0px solid #e3e3e3; box-sizing: border-box; margin: 1.25em 0px; color: #0d0d0d; font-family: sans-serif,Arial; font-size: 16px; font-style: normal; font-weight: 400; background-color: #ffffff;\"><span style=\"font-size: 12px;\"><strong>Q: How do I get a shipping quote?</strong></span><br /><span style=\"font-size: 12px;\">A: Shipping quotes will be provided when you contact us directly.</span></p>\n</div>\n</div>\n<p>&nbsp;</p>\n<p><img src=\"//sc04.alicdn.com/kf/A7723b558ebd246ba94ee2457123819e31/963255098/A7723b558ebd246ba94ee2457123819e31.jpg\" alt=\"//sc04.alicdn.com/kf/A7723b558ebd246ba94ee2457123819e31/963255098/A7723b558ebd246ba94ee2457123819e31.jpg_100x100\" ori-width=\"1800\" ori-height=\"1800\" /></p>",
    'display': 'N',  # Set display status
    'gmt_modified': '2024-06-26 07:09:40',  # Set modification time
    'group_id': 901946552,  # Updated group ID
    'is_smart_edit': False,  # Set smart edit status
    'keywords': json.dumps({
        'string': [
            'coloring book 2-assorted activity book set 80-page activity book Coloring book for kids themed book Alladin'
        ]
    }),  # Updated keywords
    'main_image': json.dumps({
        'images': {
            'string': [
                'https://sc04.alicdn.com/kf/A9a990c20ec0f4b09858faffc4dffc45ab.jpg'
            ]
        }
    }),  # Updated main image URL
    'owner_member': 1622870364,  # Updated owner member ID
    'owner_member_display_name': 'Ron Audona',  # Updated owner member display name
    'pc_detail_url': 'https://www.alibaba.com/product-detail/Alladin-80pg-Coloring-and-Activity-Book_11000016069005.html',  # Updated product detail URL
    'price_type': 'fob_price',  # Set price type
    'product_sku': json.dumps({
        'sku_attributes': {
            'sku_attribute': [
                {
                    'attribute_id': 100001401,
                    'attribute_name': 'Size',
                    'values': {
                        'sku_attribute_value': [
                            {
                                'system_value_name': '1 Case Pack - min. $1000. Mix & match to meet min.',
                                'value_id': -2
                            },
                            {
                                'system_value_name': '43 Case Packs',
                                'value_id': -3
                            },
                            {
                                'system_value_name': '1 Pallet - 90 Case Packs',
                                'value_id': -4
                            }
                        ]
                    }
                }
            ]
        },
        'skus': {
            'sku_definition': [
                {
                    'attr2_value': '{100001401:-2}',
                    'bulk_discount_prices': {
                        'bulk_discount_price': [
                            {
                                'price': '23.4',
                                'start_quantity': -1
                            }
                        ]
                    },
                    'sku_id': 11000546715493
                },
                {
                    'attr2_value': '{100001401:-3}',
                    'bulk_discount_prices': {
                        'bulk_discount_price': [
                            {
                                'price': '1006.2',
                                'start_quantity': -1
                            }
                        ]
                    },
                    'sku_id': 11000546715494
                },
                {
                    'attr2_value': '{100001401:-4}',
                    'bulk_discount_prices': {
                        'bulk_discount_price': [
                            {
                                'price': '2106.0',
                                'start_quantity': -1
                            }
                        ]
                    },
                    'sku_id': 11000546715495
                }
            ]
        }
    }),  # Updated product SKU information
    'product_type': 'sourcing',  # Set product type
    'rts': False,  # Set real-time status
    'sourcing_trade': json.dumps({
        'deliver_periods': {
            'deliver_period': [
                {
                    'process_period': 30,
                    'quantity': 12
                }
            ]
        },
        'fob_currency': 'USD',  # Updated FOB currency
        'fob_max_price': '2106.0',  # Updated FOB max price
        'fob_min_price': '23.4',  # Updated FOB min price
        'fob_unit_type': 'Case',  # Set FOB unit type
        'min_order_quantity': '2.0',  # Set minimum order quantity
        'min_order_unit_type': 'Case',  # Set minimum order unit type
        'payment_methods': json.dumps({
            'string': [
                'Bank Transfer'
            ]
        })  # Set payment methods
    }),  # Updated sourcing trade information
    'status': 'tbd',  # Set status
    'subject': 'EPA Polo White Non-Medical Mask',  # Updated subject
    'wholesale_trade': {}  # Set wholesale trade information
}

# Function to calculate sign
def calculate_sign(params, secret):
    sorted_params = sorted(params.items())
    sign_string = secret + ''.join([f'{k}{v}' for k, v in sorted_params]) + secret
    return hashlib.md5(sign_string.encode('utf-8')).hexdigest().upper()

# Add sign to parameters
params['sign'] = calculate_sign(params, app_secret)

# Remove sensitive information for logging
def remove_sensitive_info(params):
    safe_params = params.copy()
    safe_params.pop('app_key', None)
    safe_params.pop('session', None)
    safe_params.pop('sign', None)
    return safe_params

# Log file names
log_file = f"{LOG_DIR}productupdatefield_logs_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"
error_log_file = f"{LOG_DIR}productupdatefield_error_{time.strftime('%Y-%m-%d_%H-%M-%S')}.json"

try:
    # Make the API request
    product_update_field_request = requests.post(url, params=params)
    product_update_field_response = product_update_field_request.json()

    # Log API request
    with open(log_file, 'w') as f:
        json.dump({
            'request_params': remove_sensitive_info(params),
            'response': product_update_field_response,
        }, f, indent=4)

    # Example of handling the response data
    if product_update_field_response.get('error_response'):
        with open(error_log_file, 'w') as f:
            json.dump({
                'request_params': remove_sensitive_info(params),
                'response': product_update_field_response,
            }, f, indent=4)
        print(f"Error: {product_update_field_response['error_response']['msg']}")
    else:
        print("Product update field API call successful.")
        # Process your response data as needed

except requests.exceptions.RequestException as e:
    with open(error_log_file, 'w') as f:
        json.dump({
            'request_params': remove_sensitive_info(params),
            'error_message': str(e),
        }, f, indent=4)
    print(f"Request failed: {e}")
