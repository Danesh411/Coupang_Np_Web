import os
import time
import json
import hashlib
import urllib.parse
import pandas as pd
from pathlib import Path
from parsel import Selector
from datetime import datetime
from curl_cffi import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

results_list = []

MAX_THREADS = 30
scrape_date = datetime.now().strftime("%d-%m-%Y")
export_date = datetime.now().strftime("%d_%m_%Y")

#TODO:: Pagesave conection path
try:
    PAGESAVE_PATH = Path(f"D:/Danesh/coupang/product_page_data/{export_date}")
    PAGESAVE_PATH.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(e)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    'cookie': 'visitor_id=668cc970-0baa-4ea5-8470-304c0532181a; nloc=en-ae; visitorId=12c027bc-403d-4b18-8aca-0a1e6fd100f7; ZLD887450000000002180avuid=69fdb243-3025-470d-a32c-ffdbbf28d0fc; x-whoami-headers=eyJ4LWxhdCI6IjI1MTk5ODQ5NSIsIngtbG5nIjoiNTUyNzE1OTg1IiwieC1hYnkiOiJ7XCJwb192Mi5lbmFibGVkXCI6MSxcImlwbF9lbnRyeXBvaW50LmVuYWJsZWRcIjoxLFwid2ViX3BscF9wZHBfcmV2YW1wLmVuYWJsZWRcIjoxLFwiY2F0ZWdvcnlfYmVzdF9zZWxsZXIuZW5hYmxlZFwiOjF9IiwieC1lY29tLXpvbmVjb2RlIjoiQUVfRFhCLVM1IiwieC1hYi10ZXN0IjpbNjEsOTAxLDk0MSw5NjEsMTAzMSwxMDkwLDExMDEsMTIxMSwxMjUwLDEzMDAsMTMzMSwxMzQyLDEzNzEsMTQxMywxNDIwLDE0NzAsMTUwMiwxNTQxLDE1ODAsMTYyMSwxNjUwLDE2ODFdLCJ4LXJvY2tldC16b25lY29kZSI6IlcwMDA2ODc2NUEiLCJ4LXJvY2tldC1lbmFibGVkIjp0cnVlLCJ4LWJvcmRlci1lbmFibGVkIjp0cnVlfQ%3D%3D; _gcl_au=1.1.330145660.1752672992; _uetsid=e320d670624911f09c581bb6872f63c4; _uetvid=e320eee0624911f0b2b81bd0bf06f6af; _fbp=fb.1.1752672993755.971521475232449673; _tt_enable_cookie=1; _ttp=01K09Q721G54Q8YJ8MHQN1GAR7_.tt.1; _pin_unauth=dWlkPU5UUTJZVEV4TTJVdFpqSm1ZUzAwWmpVMUxUbGxNVFV0TVRRME56azVaVGt4TldFNA; nguestv2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJraWQiOiJhNjczMTdhZjM0OGE0Zjk0ODYzZTU4MTU1MjQwNTYwYyIsImlhdCI6MTc1MjcyOTk2NSwiZXhwIjoxNzUyNzMwMjY1fQ.cjZph3XziPtsa1nzZnxkzpHCpGvHqZWNOmlO_s6qkrw; AKA_A2=A; _etc=ozSGPBN4GBWBXPcH; nguestv2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJraWQiOiJjYWZiOTQ3ZGZiNzc0NjUyYjhiY2IyNGI4NDFiN2Y0NSIsImlhdCI6MTc1MjcyOTk2OCwiZXhwIjoxNzUyNzMwMjY4fQ.e7I3FSRCTStkds4qlLAtIG6PtGjZpfyEurI-T6FIyzs; ak_bmsc=40E224BD368E6788C3C6EC90A5F66DBE~000000000000000000000000000000~YAAQC4R7XEc4LhSYAQAA2eHYFhzcRdzeJtSpPSiHDObR+Ak9NFwRA0OXdPOaWpo3T93SMREgp1a45bqwrMg2CK2klTR7KsVR/ZW1yCEqPFvd9/nNAgAEJyF836sTYlyI4oqsaIcqpaGQIQEDnAVhDXRG1QhDNXwfBOpOMQmD5gmdYWDscuOr3HNUt+arXINBHGG49cot0LL0ZCdcdoPCCleUwauf04ip2dkG5LHRwCe74rEHpwyMd6F3zJK7KCJ+/hGHaFk/sq/k24IUQ7KOEibZycL/KIeviD8rKZcofYJdRpGskCI6Iz9ckHlNEZ9p1ijKCZopqQrO0WQobMRXB/+Y9U1hwn1u43QdM9FvdJL2oxzXIU7GBu6xbcTaC4JxgVXjBuH8bLIzXwTL0XAjekfJ/ubQAcpCaq/VavSXkGpyvTLT5aN/0ejGTYhXFMCxolAINILj3RvQ3g==; bm_sv=20629C43B2D7670213D918F0A868F802~YAAQC4R7XFg4LhSYAQAAQOLYFhx3bpMR5oeemgSeY0hrJJunBhdBuYgUXJNGz3zl+9mu4ihv0h9sVv/C6S8zLr/gAvyEn/Nu1PfYoZjrixMy2FPOz2jeaG+MKqX+gPg0RQsplScNvdtSXpUmImRB/6IpTWAvvExiQXGNbG5IdgsFl3BuIVcr3ceYq2GD6Sb4TmXqTkcUnDJ6H99LpkdD+sDD1GgSVVVtULkhWc3mn7RfoMwAkQ5dPely61et6A==~1; _scid=bCO-z0yS-pKdmAyW73S9SEc4ek9vqCJU; _scid_r=bCO-z0yS-pKdmAyW73S9SEc4ek9vqCJU; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22oiaVDcBgjYZ6mfhdhwPS%22%2C%22expiryDate%22%3A%222026-07-17T05%3A26%3A10.126Z%22%7D; _ym_uid=1752729970999757519; _ym_d=1752729970; _ScCbts=%5B%22626%3Bchrome.2%3A2%3A5%22%5D; _clck=1y044rt%7C2%7Cfxo%7C0%7C2023; ttcsid_CFED02JC77U7HEM9PC8G=1752729969995::VXdv-m5DYxUkT1QGuwGw.2.1752730015740; ttcsid=1752729969996::lEAuvrJgHlhE8DVfg7vh.2.1752730015740; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3Anull%2C%22expiryDate%22%3A%222026-07-17T05%3A26%3A55.861Z%22%7D; _clsk=utc9ss%7C1752730016601%7C2%7C0%7Cl.clarity.ms%2Fcollect; noonengr-_zldp=dbw5UOFoeCyNLdmkfp51cZotnya0NgRNiFBrtjtE8RRqDZa%252ByjYyd5lOiDEkvBCmmKwM1K1ctjo%253D; ZLDsiq663f5c2580454f7ed6b7bbe12e575c5570eb9b21832ce32b902ca6cbca6ffc2bavuid=69fdb243-3025-470d-a32c-ffdbbf28d0fc; ZLDsiq3b3ce696144e42ab351af48092266ce3dda2b3c7b2ad6e09ba5d18504de03180tabowner=undefined; RT="z=1&dm=noon.com&si=qy91nidj7ei&ss=md6y5zn5&sl=1&tt=hbu&ld=hbx&nu=2400f1297a27ce661c35940f7ba1d940&cl=121n&ul=2jwd"',
}

def pagesave_portion(join_path, fetch_Product_URL):
    try:
        attempts = 0
        max_attempts = 3
        my_selector = ''

        while attempts < max_attempts and not my_selector:
            try:
                url = fetch_Product_URL
                scrape_do_token = ""
                proxy_url = f"https://api.scrape.do?token={scrape_do_token}&url={urllib.parse.quote(url)}&super=true"
                response = requests.get(url=proxy_url,
                                        headers=headers,
                                        )

                if response.status_code == 200 and ("product-title" in response.text and "price-amount" in response.text):
                    try:
                        with open(join_path, "w", encoding="utf-8") as file:
                            file.write(response.text)
                        my_selector = response.text
                    except Exception as e:
                        print(f"File write error: {e}")
            except Exception as e:
                print(f"Request error: {e}")
            attempts += 1
            if not my_selector:
                time.sleep(2)
        return my_selector
    except Exception as e:
        return ""

def process_item(url):
    Product_hashed_id = hashlib.sha256(url.encode()).hexdigest()
    page_name = f"{Product_hashed_id}.html"
    join_path = PAGESAVE_PATH / page_name

    if os.path.exists(join_path):
        my_selector = open(join_path, "r", encoding="utf-8").read()
    else:
        my_selector = pagesave_portion(join_path, url)

    if my_selector:
        my_content = Selector(text=my_selector)

        try:
            common_json_contain = my_content.xpath('//script[(contains(text(),"optionalBeacons"))]/text()').get()
            common_json_contain1 = common_json_contain.encode('utf-8').decode('unicode_escape')
            final_common_json_contain_test = common_json_contain.split('push(')[-1].strip('()')
            final_common_json_contain = final_common_json_contain_test.split("[1,")[-1].strip("[]")
            json_loading_content_check = json.loads(final_common_json_contain)
            av = (str(json_loading_content_check)).replace("18:", "")
            json_loading_content_check = json.loads(av)
        except:
            json_loading_content_check = ''

        item = {}

        split_id_url = url.split("products/")[-1].split("?itemId=")[0]
        item['product_id'] = split_id_url
        item['product_url'] = url

        # breadcrumbs
        try:
            breadcrumbs_list = my_content.xpath('//ul[contains(@class,"breadcrumb")]/li/a/text()').getall()
            breadcrumbs = "|".join(breadcrumbs_list) if breadcrumbs_list else "N/A"
            item['breadcrumbs'] = breadcrumbs
        except:...

        # Product Name
        try:
            product_name_check = my_content.xpath('//h1[contains(@class,"product-title")]//text()').get()
            item['product_name'] = product_name_check.strip() if product_name_check else "N/A"
        except:
            ...

        # Product Image url
        try:
            all_img_contain = my_content.xpath('//div[contains(@class,"product-image")]//img/@src').getall()
            item['product_image_url'] = "|".join(f"https:{img}" for img in all_img_contain) if all_img_contain else "N/A"
        except:
            ...

        #Expected arrival
        try:
            Expected_arrival = my_content.xpath('//em[@class="prod-txt-onyx prod-txt-font-14"]//text()').get()
            if not Expected_arrival:
                Expected_arrival = my_content.xpath('//em[@class="prod-txt-onyx prod-txt-green-2"]//text()').get()
                if not Expected_arrival:
                    Expected_arrival = my_content.xpath('//em[@class="prod-txt-onyx prod-txt-green-normal"]//text()').get()
            item['expected_arrival'] = Expected_arrival.strip() if Expected_arrival else "N/A"
        except:...

        # mrp // Price // Discounted Price
        try:
            mrp = my_content.xpath('//div[contains(@class,"original-price")]//div[contains(@class,"price-amount")]//text()').get(default="N/A")
            Price = my_content.xpath('//div[contains(@class,"sales-price")]//div[contains(@class,"price-amount")]//text()').get(default="N/A")
            discount_Price = my_content.xpath('//div[contains(@class,"final-price")]//div[contains(@class,"price-amount")]//text()').get(default="N/A")

            if mrp != "N/A" and Price != "N/A" and discount_Price != "N/A":
                item['mrp'] = mrp.replace("원", "")
                item['price'] = Price.replace("원", "")
                item['discounted_price'] = discount_Price.replace("원", "")

            elif mrp == "N/A" and Price == "N/A" and discount_Price != "N/A":
                item['mrp'] = discount_Price.replace("원", "")
                item['price'] = discount_Price.replace("원", "")
                item['discounted_price'] = 'N/A'

            elif mrp == "N/A" and Price != "N/A" and discount_Price != "N/A":
                item['mrp'] = discount_Price.replace("원", "")
                item['price'] = Price.replace("원", "")
                item['discounted_price'] = 'N/A'

            elif mrp != "N/A" and Price == "N/A" and discount_Price != "N/A":
                item['mrp'] = mrp.replace("원", "")
                item['price'] = mrp.replace("원", "")
                item['discounted_price'] = discount_Price.replace("원", "")

            else:
                item['mrp'] = mrp.replace("원", "")
                item['price'] = Price.replace("원", "")
                item['discounted_price'] = discount_Price.replace("원", "")
        except:
            ...

        # Discount Percentage
        try:
            discount_percentage = my_content.xpath('//div[contains(@class,"original-price")]/div/div/text()').getall()
            item['discount_percentage'] = "".join(discount_percentage) if discount_percentage else "N/A"
        except:
            ...

        # description
        try:
            description_list = my_content.xpath("//div[contains(@class,'product-description')]//li/text()").getall()
            description = " #||# ".join(description_list) if description_list else "N/A"
            item['description'] = description
        except:...

        # product information
        try:
            product_information_list = []
            if json_loading_content_check:
                product_information_check = json_loading_content_check[3]['children'][2][3]['children'][1][3]['btfData']['essentials']
                for product_information_ls in product_information_check:
                    product_information_dict = {}
                    product_information_key = product_information_ls.get('title')
                    product_information_value = product_information_ls.get('description')
                    product_information_dict['key'] = product_information_key.strip()
                    product_information_dict['value'] = product_information_value.strip()
                    product_information_list.append(product_information_dict)
            item['product_information'] = product_information_list if product_information_list else "N/A"
        except:
            item['product_information'] = "N/A"

        # variations
        try:
            variant_list = []
            if json_loading_content_check:
                variant_list_check = json_loading_content_check[3]['children'][2][3]['children'][1][3]['atfData']['options']['attributeVendorItemMap']
                for variant_key, variant_value in variant_list_check.items():
                    variant_dict = {}
                    variant_itemId = variant_value.get('itemId')
                    variant_url = f"https://www.coupang.com/vp/products/{split_id_url}?itemId={variant_itemId}"
                    variant_name = variant_value.get('itemName')
                    variant_price = variant_value.get('quantityBase')[0].get('price').get('finalPrice')

                    variant_dict['url'] = variant_url
                    variant_dict['itemId'] = variant_itemId
                    variant_dict['name'] = variant_name
                    variant_dict['price'] = variant_price
                    variant_list.append(variant_dict)
            item['variant'] = variant_list if variant_list else "N/A"
        except:
            item['variant'] = "N/A"

        #rating & review json
        try:
            rat_rev_json_check = my_content.xpath('//script[@type="application/ld+json"][@src="product"]//text()').get()
            rat_rev_json = json.loads(rat_rev_json_check)
            rating = rat_rev_json.get("aggregateRating").get("ratingValue")
            review = rat_rev_json.get("aggregateRating").get("ratingCount")

            item['rating'] = rating if rating else "N/A"
            item['review'] = review if review else "N/A"
        except:
            item['rating'] = "N/A"
            item['review'] = "N/A"

        #Seller Name
        try:
            # seller_name = my_content.xpath('//div[contains(text(),"판매자:")]/a/text()').get()
            seller_name = my_content.xpath('//th/div[contains(text(),"상호/대표자")]/../following-sibling::td/text()').get()
            if not seller_name:
                seller_name_check = my_content.xpath('//th[contains(text(),"판매자")]/following-sibling::td//text()').getall()
                seller_name = "".join(seller_name_check) if seller_name_check else "N/A"
            item['seller_name'] = seller_name.strip() if seller_name else "N/A"
        except:...

        # Seller rating
        try:
            seller_rating = my_content.xpath('//span[contains(text(),"판매자 평가")]/following-sibling::span/text()').get()
            item['seller_rating'] = seller_rating if seller_rating else "N/A"
        except:
            ...

        #delivery_company
        try:
            delivery_company = my_content.xpath('//div[contains(text(),"배송사: ")]/span/text()').get()
            item['delivery_company'] = delivery_company.strip() if delivery_company else "N/A"
        except:...

        #scrape_date
        item['scrape_date'] = scrape_date
        results_list.append(item)
        print("Appended ......")

def main():

    # urls = ["https://www.coupang.com/vp/products/7152343694?itemId=17983734258&vendorItemId=85140476054&sourceType=CATEGORY&categoryId=176430"]
    
    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        list(executor.map(process_item, set(urls)))
    print("All tasks completed.")

if __name__ == '__main__':
    main()
    # Export to Excel
    df = pd.DataFrame(results_list)
    output_path = f"Coupang_Sample_{export_date}.xlsx"
    df.to_excel(output_path, index=False)
    print(f"Excel file saved to {output_path}")
