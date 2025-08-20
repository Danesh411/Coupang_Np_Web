import pandas as pd
import os, json, pymongo, threading, time, hashlib
import datetime
import urllib.parse
from curl_cffi import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from parsel import Selector

results_list = []


#TODO:: Pagesave conection path
try:
    PAGESAVE_PATH = Path("D:/Danesh/Coupang NP Web feasibility/product_page_data/25_07_2025")
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

        item = {}
        split_id_url = url.split("products/")[-1].split("?itemId=")[0]
        item['product_id'] = split_id_url
        item['product_url'] = url

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

            if discount_Price != "N/A" and Price != "N/A":
                if discount_Price == Price:
                    discount_Price = "N/A"

            if discount_Price == "N/A":
                mrp = Price


            item['mrp'] = mrp.replace("원","")
            item['price'] = Price.replace("원","")
            item['discounted_price'] = discount_Price.replace("원","")
        except:
            ...

        # Discount Percentage
        try:
            discount_percentage = my_content.xpath('//div[contains(@class,"original-price")]/div/div/text()').getall()
            item['discount_percentage'] = "".join(discount_percentage) if discount_percentage else "N/A"
        except:
            ...

        #rating & review json
        try:
            rat_rev_json_check = my_content.xpath('//script[@type="application/ld+json"][@src="product"]//text()').get()
            rat_rev_json = json.loads(rat_rev_json_check)
            rating = rat_rev_json.get("aggregateRating").get("ratingValue")
            review = rat_rev_json.get("aggregateRating").get("ratingCount")

            item['rating'] = rating if rating else "N/A"
            item['review'] = review if review else "N/A"
        except:...


        #Seller Name
        try:
            # seller_name = my_content.xpath('//div[contains(text(),"판매자:")]/a/text()').get()
            seller_name = my_content.xpath('//th/div[contains(text(),"상호/대표자")]/../following-sibling::td/text()').get()
            item['seller_name'] = seller_name.strip() if seller_name else "N/A"
        except:...

        # Seller rating
        try:
            seller_rating = my_content.xpath('//span[contains(text(),"판매자 평가")]/following-sibling::span/text()').get()
            item['seller_rating'] = seller_rating if seller_rating else "N/A"
        except:
            ...
        #
        # #shipping_company
        # try:
        #     shipping_company = my_content.xpath('//div[contains(text(),"배송사: ")]/span/text()').get()
        #     item['shipping_company'] = shipping_company if shipping_company else "N/A"
        # except:...

        #delivery_company
        try:
            delivery_company = my_content.xpath('//div[contains(text(),"배송사: ")]/span/text()').get()
            item['delivery_company'] = delivery_company.strip() if delivery_company else "N/A"
        except:...

        #scrape_date
        try:
            scrape_date = "25-07-2025"
            item['scrape_date'] = scrape_date
        except:...

        results_list.append(item)
        # print("Appended ......")



MAX_THREADS = 1
def main():
    urls = [
"https://www.coupang.com/vp/products/8917646692?itemId=26057112298&vendorItemId=92811635700&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8618125627?itemId=25001855405&vendorItemId=92006999039&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8642228912?itemId=25080829295&vendorItemId=92084738027&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8660236732?itemId=25136119888&vendorItemId=92135144181&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8643834050?itemId=25087451209&vendorItemId=92091219443&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8787731451?itemId=25574568483&vendorItemId=92565624182&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8586703997?itemId=24893505255&vendorItemId=92315964876&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8593308905?itemId=24916173774&vendorItemId=91922540144&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8010739062?itemId=22348633736&vendorItemId=91266374716&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670813398?itemId=25170667745&vendorItemId=92409070156&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634111907?itemId=25050737399&vendorItemId=92055186465&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8007155804?itemId=22321998304&vendorItemId=92142537839&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312662&vendorItemId=91088074492&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8776709775?itemId=25534277872&vendorItemId=92525940734&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670815406?itemId=25170675361&vendorItemId=92574505045&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24925567976&vendorItemId=92555804541&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312141&vendorItemId=91088073981&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7059056549?itemId=3849414261&vendorItemId=93118943113&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7410157624?itemId=25591302172&vendorItemId=92879570435&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8825839897?itemId=25718160323&vendorItemId=92706963482&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24580285353&vendorItemId=91592064801&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=21567136745&vendorItemId=92932882360&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401502057?itemId=24285969748&vendorItemId=91302226528&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24580285066&vendorItemId=91592064516&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634103395?itemId=25050703945&vendorItemId=92055153789&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8628848724?itemId=25036079815&vendorItemId=92316291877&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8641430788?itemId=25078107698&vendorItemId=92082076572&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827135?itemId=20799858024&vendorItemId=92648277928&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8595783695?itemId=24923790739&vendorItemId=91930048713&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8825839897?itemId=25718160331&vendorItemId=92706963514&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8380052384?itemId=24215834080&vendorItemId=91233179966&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8887830055?itemId=25948635045&vendorItemId=92779581906&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790571200?itemId=15997178736&vendorItemId=92768257228&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8352414439?itemId=24131743938&vendorItemId=91150732757&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7655076552?itemId=24730130016&vendorItemId=92778786258&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8489404146?itemId=24570943868&vendorItemId=91582929646&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670809560?itemId=25170653084&vendorItemId=92574477109&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8352414439?itemId=24131743937&vendorItemId=91150732743&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634113313?itemId=25050742262&vendorItemId=92055190658&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8721969902?itemId=25335711905&vendorItemId=92330453429&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7276697564?itemId=18569839307&vendorItemId=88042486601&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8137556672?itemId=26015038850&vendorItemId=92996864637&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6396531908?itemId=25238889949&vendorItemId=92234985958&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634097247?itemId=25050677235&vendorItemId=92055127601&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8137556672?itemId=26015038848&vendorItemId=92996864618&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8886151906?itemId=25940712109&vendorItemId=92641795472&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8597521793?itemId=24929346205&vendorItemId=91935526618&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24875536724&vendorItemId=91592064494&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8515632450?itemId=24652397241&vendorItemId=91662975788&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8486186136?itemId=24559505643&vendorItemId=91533243370&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634103395?itemId=25050703946&vendorItemId=92055153797&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888734?itemId=20252601032&vendorItemId=93032090372&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670813398?itemId=25170667738&vendorItemId=92409070162&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009412420?itemId=11356857107&vendorItemId=93125741158&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8489404146?itemId=24570943871&vendorItemId=91582929654&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8866714659?itemId=25860425232&vendorItemId=92846736598&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615645731?itemId=24992389157&vendorItemId=91997709608&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888734?itemId=20252600964&vendorItemId=93032090361&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=22949290180&vendorItemId=92637198778&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401785735?itemId=24286978884&vendorItemId=93063041314&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24580285075&vendorItemId=91592064522&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7826078289?itemId=21271373594&vendorItemId=92732421875&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536740&vendorItemId=91592064750&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401473692?itemId=24285892087&vendorItemId=91302150139&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8700877880?itemId=25266314991&vendorItemId=90567011261&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/131924531?itemId=388049960&vendorItemId=70379805688&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634096784?itemId=25050675353&vendorItemId=92055124347&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670809560?itemId=25170653086&vendorItemId=92409049731&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8628848762?itemId=25036079976&vendorItemId=92135744399&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8817171110?itemId=25691522783&vendorItemId=92680692072&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8822010177?itemId=25709725433&vendorItemId=89136805034&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8628848724?itemId=25036079814&vendorItemId=92135870502&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8642206997?itemId=25080740279&vendorItemId=92084644890&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009412420?itemId=24694931533&vendorItemId=93125741170&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8648217866?itemId=25101146348&vendorItemId=92135880106&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8717772920?itemId=25321016167&vendorItemId=92315973479&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8590880364?itemId=24908679837&vendorItemId=92082032092&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6321694223?itemId=23009024546&vendorItemId=91996866593&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401785735?itemId=24286978882&vendorItemId=93063041332&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748753?itemId=24580285122&vendorItemId=91592064560&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=22681361540&vendorItemId=93004099285&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8891328996?itemId=25956447441&vendorItemId=92939244455&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/311125458?itemId=981884656&vendorItemId=92227013391&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827135?itemId=20799858065&vendorItemId=92648277938&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8140767326?itemId=23133399087&vendorItemId=92644441856&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24580285348&vendorItemId=91592064777&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8700877880?itemId=25266314992&vendorItemId=90567011242&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401785735?itemId=24286978885&vendorItemId=93063041345&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8658338036?itemId=25129369399&vendorItemId=92128525171&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8886151906?itemId=25940712112&vendorItemId=92641795443&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615645701?itemId=24992389008&vendorItemId=91997709425&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8628848724?itemId=25036079813&vendorItemId=92135870484&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670815406?itemId=25170675364&vendorItemId=92574505070&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8648217866?itemId=25101146346&vendorItemId=92135880101&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847090907?itemId=25787777476&vendorItemId=92775603588&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009412420?itemId=11356857104&vendorItemId=93125741178&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8161274337?itemId=23268683518&vendorItemId=92966672762&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827135?itemId=20799857727&vendorItemId=92602739260&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893691&vendorItemId=92680155548&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312135&vendorItemId=91088073942&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24875536730&vendorItemId=91592064490&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8891785697?itemId=25958188611&vendorItemId=92940957220&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8591230625?itemId=24909898769&vendorItemId=92082059530&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401473753?itemId=24285892226&vendorItemId=91302150237&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8489404146?itemId=24570943869&vendorItemId=91582940892&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6155868999?itemId=24661571925&vendorItemId=92084757608&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827059?itemId=20799858025&vendorItemId=92558455489&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8101727531?itemId=25581255955&vendorItemId=92585866233&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009412420?itemId=11356856853&vendorItemId=92813526758&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8717783677?itemId=25321057989&vendorItemId=92316014458&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8825839897?itemId=25718160328&vendorItemId=92706963497&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8745097048?itemId=25417338840&vendorItemId=5256421411&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8040345729?itemId=24995790966&vendorItemId=93061247900&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827059?itemId=21476836268&vendorItemId=87868951093&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8352414439?itemId=24131743943&vendorItemId=91150732787&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132877?itemId=23156170354&vendorItemId=90188980802&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312665&vendorItemId=91088074520&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7276727876?itemId=25248270956&vendorItemId=93052835439&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8608393400?itemId=24966144968&vendorItemId=91971812723&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132881?itemId=24126728494&vendorItemId=93064007139&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8591348719?itemId=24910275328&vendorItemId=92135336920&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8887830055?itemId=25948635041&vendorItemId=92779581945&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312669&vendorItemId=91088074576&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=20799857756&vendorItemId=92932671857&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615468071?itemId=25004767485&vendorItemId=92009842332&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670815941?itemId=25170677359&vendorItemId=92574515234&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199461?itemId=22179251516&vendorItemId=92820032670&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8591230625?itemId=24909898761&vendorItemId=92082059520&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312495&vendorItemId=91088074310&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24580285065&vendorItemId=91592064510&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847090907?itemId=25787777484&vendorItemId=92775603625&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8351420670?itemId=24603611602&vendorItemId=93051665466&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=23934383072&vendorItemId=92718627291&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8933220103?itemId=23423236991&vendorItemId=92910350381&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8371447702?itemId=24191077936&vendorItemId=93039127070&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7728777508?itemId=20573290580&vendorItemId=91962793545&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199461?itemId=11356886299&vendorItemId=92820032676&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8744995745?itemId=25416766553&vendorItemId=92410046259&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=21293982066&vendorItemId=93051533795&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199381?itemId=11356856629&vendorItemId=92816338689&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312487&vendorItemId=91088074265&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8659817124?itemId=25135089326&vendorItemId=92135099455&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401484120?itemId=24285920317&vendorItemId=91302177861&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888680?itemId=20252600516&vendorItemId=87340557451&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8835122273?itemId=25746120707&vendorItemId=92734469558&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=25561188493&vendorItemId=92637198807&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790571200?itemId=15997173162&vendorItemId=92768257126&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312675&vendorItemId=91088074657&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8344425715?itemId=25367783200&vendorItemId=92715460543&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8658338036?itemId=25129369398&vendorItemId=92128525165&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8648252369?itemId=25101206805&vendorItemId=92135892507&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634096784?itemId=25050675352&vendorItemId=92055124339&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8513454505?itemId=24644788501&vendorItemId=92788210064&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7688572954?itemId=20554945007&vendorItemId=87630955510&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=24882563682&vendorItemId=92637198736&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536731&vendorItemId=91592064768&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8918753038?itemId=26060854641&vendorItemId=93042148870&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312520&vendorItemId=91088074405&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8885832263?itemId=25939099091&vendorItemId=92923413621&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8891328996?itemId=25956447439&vendorItemId=92939244442&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8628848762?itemId=25036079974&vendorItemId=92135744383&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24875536723&vendorItemId=91592064505&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827059?itemId=21476835412&vendorItemId=87868950964&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312488&vendorItemId=91088074282&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8773565060?itemId=25522007604&vendorItemId=92513855150&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7755655021?itemId=3849412609&vendorItemId=92820490386&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=23786866903&vendorItemId=92637199158&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7742626742?itemId=20835311788&vendorItemId=93053448861&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8725529525?itemId=25348103418&vendorItemId=92290359027&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401473692?itemId=24285892090&vendorItemId=91302150146&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7834159285?itemId=25169504362&vendorItemId=92777722300&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7405190397?itemId=19175222797&vendorItemId=93071354479&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8624472376?itemId=25022459208&vendorItemId=92027230057&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009412420?itemId=11356856856&vendorItemId=92813526806&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8571845762?itemId=24835019856&vendorItemId=91842246908&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132877?itemId=25431703591&vendorItemId=93127626657&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847090907?itemId=25787777482&vendorItemId=92775603612&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893682&vendorItemId=92220237702&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8663136900?itemId=25143438439&vendorItemId=92142349808&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132881?itemId=23156170379&vendorItemId=90188980904&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8593125271?itemId=24915524744&vendorItemId=91921900614&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312667&vendorItemId=91088074547&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8597619402?itemId=24929608519&vendorItemId=91935906633&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615021245?itemId=24990287292&vendorItemId=92524302405&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316504953?itemId=24001383515&vendorItemId=92635387709&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199349?itemId=11356856617&vendorItemId=92816315173&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8608393400?itemId=24966144967&vendorItemId=91971812714&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25281984198&vendorItemId=92526160249&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8628848822?itemId=25036080240&vendorItemId=92084644902&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132877?itemId=23156170358&vendorItemId=90188980839&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132881?itemId=23156170394&vendorItemId=90188980994&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159130&vendorItemId=90044609383&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8035149412?itemId=24420571955&vendorItemId=92084189980&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24580285351&vendorItemId=91592064790&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25052246067&vendorItemId=93059878660&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8457735882?itemId=24464415297&vendorItemId=91812870952&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7837008464?itemId=22682171213&vendorItemId=93054038956&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8134872744?itemId=23106636861&vendorItemId=90139928103&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7719635109?itemId=24655645727&vendorItemId=92097519069&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8599880726?itemId=24936290906&vendorItemId=91942359436&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24580285067&vendorItemId=91592064521&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8249884714?itemId=24536208864&vendorItemId=93130651105&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132877?itemId=23156170373&vendorItemId=90188980983&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7755655021?itemId=3849412604&vendorItemId=92820490313&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893685&vendorItemId=92680155468&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8665570383?itemId=25150893644&vendorItemId=92149372629&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8728715872?itemId=25360224457&vendorItemId=92354912281&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8645383787?itemId=25093147687&vendorItemId=92725913500&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8206400000?itemId=23540784546&vendorItemId=90781271164&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24580285080&vendorItemId=91592064530&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8593653673?itemId=24917238765&vendorItemId=91923580005&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536727&vendorItemId=91592064762&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8294992236?itemId=23924490871&vendorItemId=90946705098&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7719635109?itemId=24655645730&vendorItemId=92057241235&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748753?itemId=24580285134&vendorItemId=91592064589&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24898683192&vendorItemId=93059878279&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790571200?itemId=15997176157&vendorItemId=92768257164&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199372?itemId=11356856713&vendorItemId=92816374914&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615645791?itemId=24992389345&vendorItemId=91997709943&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827059?itemId=20799857840&vendorItemId=92558455500&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199461?itemId=13660506398&vendorItemId=92820032742&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199372?itemId=11356856872&vendorItemId=92816374815&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312133&vendorItemId=91088073925&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24875536728&vendorItemId=91592064497&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7665226060?itemId=24962986498&vendorItemId=92717359346&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8918775731?itemId=26060872172&vendorItemId=93042166504&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=20799857760&vendorItemId=92932671850&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670820911?itemId=25170694738&vendorItemId=92316327494&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8310298956?itemId=24420542700&vendorItemId=92717020312&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893688&vendorItemId=92680155456&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8670815941?itemId=25170677360&vendorItemId=92574515230&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8854560522?itemId=25815836511&vendorItemId=91520963691&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8593308905?itemId=24916173773&vendorItemId=91922540136&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759451265?itemId=24380751754&vendorItemId=92369669945&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24580285074&vendorItemId=91592064517&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8721969902?itemId=25335711907&vendorItemId=92330453442&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634112756?itemId=25050740800&vendorItemId=92055189146&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25647082631&vendorItemId=93006442547&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600655&vendorItemId=87340557638&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827135?itemId=25736238566&vendorItemId=93074136266&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8048973487?itemId=22567363063&vendorItemId=92182881508&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8554020367?itemId=24769377953&vendorItemId=92799142801&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8200576723?itemId=23505039556&vendorItemId=91274157045&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7720012513?itemId=22683280809&vendorItemId=93064000000&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8352414439?itemId=24131743940&vendorItemId=91150732771&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8012114557?itemId=22354579105&vendorItemId=92283812352&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8540019824?itemId=24724662598&vendorItemId=91733824991&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8118595680?itemId=23020184318&vendorItemId=93061111032&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312670&vendorItemId=91088074593&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25158180639&vendorItemId=93059878719&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634115939?itemId=25050750892&vendorItemId=92055199401&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25120551823&vendorItemId=93130677572&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=23934383071&vendorItemId=92718627300&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132881?itemId=24126800812&vendorItemId=93051959933&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=25191864405&vendorItemId=92317271994&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8369680515?itemId=24185106474&vendorItemId=92371307854&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=25149243603&vendorItemId=93119100895&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312511&vendorItemId=91088074353&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8790650665?itemId=25585814759&vendorItemId=92576683075&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6319323194?itemId=24596963171&vendorItemId=92612328547&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6396531908?itemId=13660508306&vendorItemId=92813877454&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7478935820?itemId=19531275339&vendorItemId=86639708593&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199349?itemId=11356858961&vendorItemId=92816315290&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24580285349&vendorItemId=91592064783&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24580285068&vendorItemId=91592064526&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8419601789?itemId=24351065861&vendorItemId=91366487105&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634111907?itemId=25050737394&vendorItemId=92055186453&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7658254957?itemId=21679140541&vendorItemId=92759095159&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748753?itemId=24580285125&vendorItemId=91592064567&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8886151906?itemId=25940712111&vendorItemId=92641795464&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312518&vendorItemId=91088074397&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827059?itemId=20799857956&vendorItemId=92628933798&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8771559279?itemId=25515077187&vendorItemId=91966553979&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8853177314?itemId=25810781754&vendorItemId=92797977098&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7679945044?itemId=19685263257&vendorItemId=93061497790&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=25001662785&vendorItemId=93117886586&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8734896542?itemId=25384082700&vendorItemId=92377975290&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8034468149?itemId=24974456373&vendorItemId=93108926838&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8457735882?itemId=24464415271&vendorItemId=91812870910&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159142&vendorItemId=90044609357&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8885832263?itemId=25939099092&vendorItemId=92923413581&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199349?itemId=11356856620&vendorItemId=92816315222&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24655662614&vendorItemId=93008535795&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=17845105692&vendorItemId=92526160189&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790571200?itemId=15997175967&vendorItemId=92768257108&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199461?itemId=24513336687&vendorItemId=92820032764&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847090907?itemId=25787777471&vendorItemId=92775603568&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8101727531?itemId=24425362413&vendorItemId=92088259045&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748753?itemId=24580285124&vendorItemId=91592064563&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8073129456?itemId=22731436465&vendorItemId=92789078051&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199372?itemId=11356856709&vendorItemId=92816374903&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8794150481?itemId=25599770429&vendorItemId=92590441192&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8021863197?itemId=22416310397&vendorItemId=93073082998&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748753?itemId=24580285132&vendorItemId=91592064584&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159152&vendorItemId=90044609262&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8075129542?itemId=22745621689&vendorItemId=92321169020&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827135?itemId=25540847063&vendorItemId=93074223718&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7728777508?itemId=20573290544&vendorItemId=93008315212&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8658338036?itemId=25129369396&vendorItemId=92128525156&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8698830385?itemId=25259265585&vendorItemId=92644397600&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24875536726&vendorItemId=91592064492&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8034468149?itemId=25190152236&vendorItemId=92239713483&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8073128873?itemId=22731434182&vendorItemId=92750014395&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25211233470&vendorItemId=93056020341&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=22903628671&vendorItemId=92709410766&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7728777508?itemId=20573290558&vendorItemId=92787667511&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8690523972?itemId=25231510956&vendorItemId=92227708897&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6530596347?itemId=23239910468&vendorItemId=92577237604&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8027176629?itemId=22436382055&vendorItemId=92376302173&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8442931162?itemId=24422486153&vendorItemId=92643990095&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24925567978&vendorItemId=92555804534&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8037230169?itemId=22491200542&vendorItemId=92845743885&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252601157&vendorItemId=87340558032&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24948251270&vendorItemId=92715148187&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159153&vendorItemId=90044609268&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313126&vendorItemId=91088074938&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312131&vendorItemId=91088073913&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=21476814229&vendorItemId=92933459011&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634113313?itemId=25050742267&vendorItemId=92055190667&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7495250071?itemId=25153364500&vendorItemId=93050931642&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8233190921?itemId=23698165938&vendorItemId=93052872129&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8369807414?itemId=24185576191&vendorItemId=93119826683&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8606916814?itemId=24960728820&vendorItemId=91966467458&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=21476817529&vendorItemId=92933459027&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8844025306?itemId=25777239372&vendorItemId=92765335486&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6321694223?itemId=25192134369&vendorItemId=92812373482&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8026904222?itemId=22901010530&vendorItemId=92911702702&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8301079303?itemId=23947371080&vendorItemId=91996327019&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8233190921?itemId=24502752177&vendorItemId=93052781675&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8007155804?itemId=25265725509&vendorItemId=92525940890&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199461?itemId=24513336688&vendorItemId=92768455707&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8419601789?itemId=24351065873&vendorItemId=91366487158&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790570817?itemId=15997178746&vendorItemId=83202425025&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835154&vendorItemId=92777611569&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615645611?itemId=25179706259&vendorItemId=92476678762&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312524&vendorItemId=91088074424&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24948251277&vendorItemId=92021328324&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6823442318?itemId=16179267652&vendorItemId=92848868600&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24496771971&vendorItemId=92715148348&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6437398194?itemId=13920011301&vendorItemId=81169449238&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25249141121&vendorItemId=93135783495&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7276727876?itemId=23038447370&vendorItemId=93052835212&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8284568344?itemId=23887340987&vendorItemId=93002508925&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25249141114&vendorItemId=93135783539&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8608393400?itemId=24966144970&vendorItemId=91971812743&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8606916814?itemId=24960728841&vendorItemId=91966467564&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6999755659?itemId=22521865872&vendorItemId=93052158857&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8778354630?itemId=25539886653&vendorItemId=92085394846&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=22681361535&vendorItemId=93070067298&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8040345729?itemId=23195889870&vendorItemId=90228493391&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24898474427&vendorItemId=93135505259&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6323293075?itemId=13189671892&vendorItemId=92249017471&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8034468149?itemId=25190152235&vendorItemId=93108927029&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7650887485?itemId=20356830277&vendorItemId=92316309182&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=24882563687&vendorItemId=92673716120&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790570817?itemId=15997175950&vendorItemId=83202422283&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8665664621?itemId=25441068070&vendorItemId=92775470460&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8933220103?itemId=23091816573&vendorItemId=92095487920&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8457735882?itemId=24464415291&vendorItemId=91937898420&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600954&vendorItemId=87340557859&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7054572004?itemId=25209466915&vendorItemId=92205995644&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25153264694&vendorItemId=93056020576&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8438585578?itemId=24407670123&vendorItemId=93063302863&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8544777654?itemId=24740695209&vendorItemId=91749389231&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7912967159?itemId=21718069556&vendorItemId=93073727250&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5574519945?itemId=11573622069&vendorItemId=92002255410&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6988625765?itemId=17097021020&vendorItemId=93126174193&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5895627360?itemId=10380171899&vendorItemId=90117236401&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8743370446?itemId=25410428146&vendorItemId=92403829142&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888636?itemId=20252601168&vendorItemId=87340558036&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=25424550113&vendorItemId=92417666615&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24898683188&vendorItemId=93059878759&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6515706092?itemId=24030465927&vendorItemId=92565988074&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8540019824?itemId=24724662600&vendorItemId=91733825007&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8721969902?itemId=25335711909&vendorItemId=92330453457&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7054572004?itemId=24565098607&vendorItemId=92612287152&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615468071?itemId=25004767482&vendorItemId=92009842321&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7674621253?itemId=20482695669&vendorItemId=93081979623&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7650887485?itemId=20356830275&vendorItemId=92316309207&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8737222203?itemId=23723200564&vendorItemId=92375939031&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=25149243606&vendorItemId=92583998446&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8744961877?itemId=25416602108&vendorItemId=91239763424&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759451265?itemId=24542908169&vendorItemId=91892116777&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8751021972?itemId=25440177299&vendorItemId=92433065340&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8627175047?itemId=25031688957&vendorItemId=92036347092&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8522633157?itemId=24674245701&vendorItemId=91684436093&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=21567136752&vendorItemId=92129936462&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25120551832&vendorItemId=93130677566&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600264&vendorItemId=87340557100&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8632040518?itemId=24949859665&vendorItemId=91954127477&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827135?itemId=25540847062&vendorItemId=93074223733&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=25498576372&vendorItemId=92637198839&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313130&vendorItemId=91088074955&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7720012513?itemId=21287021473&vendorItemId=93064641582&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615646113?itemId=25441223857&vendorItemId=92524335497&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7054572004?itemId=25209466908&vendorItemId=93073173438&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8522633157?itemId=24674245702&vendorItemId=91684436096&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8401473753?itemId=24285892222&vendorItemId=91302150222&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7728777508?itemId=20573290645&vendorItemId=93008315205&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790571200?itemId=15997175946&vendorItemId=92768257198&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8273061636?itemId=23844991048&vendorItemId=91975406667&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159140&vendorItemId=90044609285&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7719635109?itemId=25190138542&vendorItemId=92418901789&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24898474446&vendorItemId=93130020273&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759454620?itemId=22634885682&vendorItemId=91892582068&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7276727876?itemId=25248270951&vendorItemId=93052835101&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24284340614&vendorItemId=92526105359&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=22903628688&vendorItemId=91618453620&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8608393400?itemId=24966144969&vendorItemId=91971812734&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=21567136744&vendorItemId=93051535137&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159132&vendorItemId=90044609371&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8008675298?itemId=24425306443&vendorItemId=93073832888&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759451265?itemId=22352426299&vendorItemId=92924402231&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8310298956?itemId=24420542683&vendorItemId=92717058854&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893683&vendorItemId=92715148121&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7567553190?itemId=22683063959&vendorItemId=92911395165&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6999755659?itemId=25585218295&vendorItemId=93052158177&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=25001662783&vendorItemId=93117886611&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7472297829?itemId=3849414395&vendorItemId=92820676238&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8159835017?itemId=24286255180&vendorItemId=93101044757&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25153264695&vendorItemId=93056020354&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312492&vendorItemId=91088074296&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8728887005?itemId=25360797162&vendorItemId=92767706306&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8354220547?itemId=24138067609&vendorItemId=91836655445&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=25189926195&vendorItemId=93117886631&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7495250071?itemId=24543374690&vendorItemId=91555811888&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312486&vendorItemId=91088074242&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159125&vendorItemId=90044609252&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8496332233?itemId=24590700645&vendorItemId=92719199317&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7219639358?itemId=24484916673&vendorItemId=93052256187&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8755569605?itemId=25455147347&vendorItemId=92967376612&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7358399326?itemId=22893931414&vendorItemId=92471940446&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536744&vendorItemId=91592064835&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8034468149?itemId=25613261155&vendorItemId=93108927014&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312515&vendorItemId=91088074378&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8347868204?itemId=24113853448&vendorItemId=92331232389&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8233190921?itemId=24558981430&vendorItemId=93052782283&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8596770300?itemId=24926646088&vendorItemId=92981250268&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615468071?itemId=24991719945&vendorItemId=91997052493&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8011369583?itemId=22351701798&vendorItemId=92516744352&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=17845105686&vendorItemId=92526160538&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8194779139?itemId=23466156225&vendorItemId=93051581044&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8244827636?itemId=25282347837&vendorItemId=93062606017&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313128&vendorItemId=91088074948&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/4945187498?itemId=24541742043&vendorItemId=92878820893&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7405190397?itemId=21437660316&vendorItemId=92315976230&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536737&vendorItemId=91592064756&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159136&vendorItemId=90044609266&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7358399326?itemId=22893931415&vendorItemId=92471940459&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8035149412?itemId=24420571976&vendorItemId=92084189962&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8554020367?itemId=24769377952&vendorItemId=91777545496&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=24541809669&vendorItemId=93061718338&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316504953?itemId=24001383520&vendorItemId=92635387793&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/4945187498?itemId=23251068179&vendorItemId=92735483126&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=25424550106&vendorItemId=92931462565&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847090907?itemId=25787777468&vendorItemId=92939311426&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7834159285?itemId=23114949348&vendorItemId=92361681181&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8249884714?itemId=25343923841&vendorItemId=93130619283&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313119&vendorItemId=91088074905&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7912789806?itemId=22138114385&vendorItemId=91974393148&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8634102664?itemId=25050700782&vendorItemId=92055150420&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6155868999?itemId=22683598405&vendorItemId=92054618217&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=25639098176&vendorItemId=93063182273&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893684&vendorItemId=93072379797&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8039909783?itemId=25643087234&vendorItemId=93073420325&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615021245?itemId=24990287303&vendorItemId=92524302370&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7720012513?itemId=21287021477&vendorItemId=91996880750&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25036204446&vendorItemId=93059878814&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7719635109?itemId=24666241088&vendorItemId=92146305305&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748728?itemId=24875536734&vendorItemId=91592064499&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7054572004?itemId=17475090995&vendorItemId=93000072540&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8915762774?itemId=15997173956&vendorItemId=92768284132&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7742626742?itemId=20835311790&vendorItemId=92377192073&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=21476815808&vendorItemId=92931191807&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8101727531?itemId=23251927945&vendorItemId=93014064395&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7709097178?itemId=20659990555&vendorItemId=93009125225&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8007155804?itemId=25265725508&vendorItemId=93133275052&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=25561188502&vendorItemId=92637198963&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7674621253?itemId=20482695665&vendorItemId=93081979611&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25454003733&vendorItemId=92526105081&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=21293982067&vendorItemId=93051535211&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8347868204?itemId=24113853446&vendorItemId=92331232217&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009006213?itemId=24627029197&vendorItemId=92786690027&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8665664621?itemId=25151270311&vendorItemId=92775470613&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24655662604&vendorItemId=93008535809&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7276727876?itemId=24379553677&vendorItemId=92820216218&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312140&vendorItemId=91088073973&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7970258723?itemId=22071318354&vendorItemId=92987692013&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7405190397?itemId=19175222826&vendorItemId=91973054367&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8454289958?itemId=25727683858&vendorItemId=92796893059&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790570817?itemId=15997177440&vendorItemId=83202423670&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8841419721?itemId=25791850906&vendorItemId=92931071614&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159128&vendorItemId=90044609377&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/1299315622?itemId=25057493104&vendorItemId=92083922800&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7674621253?itemId=24984470203&vendorItemId=93111901742&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316873869?itemId=24002976542&vendorItemId=91975391386&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536722&vendorItemId=91592064806&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24875536729&vendorItemId=91592064504&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8419601789?itemId=24351065882&vendorItemId=91366487183&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7495250071?itemId=24543374694&vendorItemId=93050932087&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7219639358?itemId=18291865961&vendorItemId=92977924385&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8008675298?itemId=23423834240&vendorItemId=91592077340&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25036204441&vendorItemId=93059878028&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312506&vendorItemId=91088074335&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759451265?itemId=24380751752&vendorItemId=92716096719&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8596313555?itemId=24925027823&vendorItemId=93033825434&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/4945187498?itemId=24326794322&vendorItemId=92789042194&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24898683189&vendorItemId=93059877558&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8215371059?itemId=23596299324&vendorItemId=92812734907&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8558735297?itemId=24784254882&vendorItemId=91792174410&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827110?itemId=21476818583&vendorItemId=93032547919&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8354220547?itemId=24138067611&vendorItemId=92418178521&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8381887654?itemId=24222626345&vendorItemId=92404884040&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=25149243594&vendorItemId=92583998386&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25094729673&vendorItemId=92525051526&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6823442318?itemId=16179267658&vendorItemId=92594807958&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759454620?itemId=22634885683&vendorItemId=91892581977&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8381666557?itemId=24221864220&vendorItemId=91278851574&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553625?itemId=25789834103&vendorItemId=92777610854&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748753?itemId=24580285130&vendorItemId=91592064579&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25647082625&vendorItemId=92636984489&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/4791919213?itemId=24168359216&vendorItemId=93071820925&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8039909783?itemId=25643072535&vendorItemId=93073420334&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8608393400?itemId=24966144971&vendorItemId=91971812749&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8371447702?itemId=25353984927&vendorItemId=92496384681&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8513454505?itemId=24644788500&vendorItemId=93044362595&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600657&vendorItemId=87340557635&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312527&vendorItemId=91088074446&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8505517152?itemId=24618285153&vendorItemId=93053607876&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7759441810?itemId=24536745397&vendorItemId=91892636231&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8350854955?itemId=24125579043&vendorItemId=91935656242&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25281984195&vendorItemId=92277548307&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8803794559?itemId=25638121410&vendorItemId=92628197841&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7658254957?itemId=24514012547&vendorItemId=92778361777&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7194239438?itemId=18170734059&vendorItemId=92932907008&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24898683183&vendorItemId=93059877527&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790570817?itemId=15997178194&vendorItemId=83202424427&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009006213?itemId=24627029201&vendorItemId=92786690058&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7768190938?itemId=24478736715&vendorItemId=92856270316&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8933220099?itemId=23408680101&vendorItemId=92525503515&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8027176629?itemId=22436382060&vendorItemId=92376302158&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8082824900?itemId=22798824674&vendorItemId=92777572228&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=22407402882&vendorItemId=92531494437&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888636?itemId=20252600428&vendorItemId=87340557211&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6515706092?itemId=24030465775&vendorItemId=92789947057&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8522633157?itemId=24674245695&vendorItemId=91684436077&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313124&vendorItemId=91088074925&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8255678398?itemId=23774605866&vendorItemId=93035189454&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=25191864406&vendorItemId=93117886622&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5381062413?itemId=23379106623&vendorItemId=92736046389&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/4612396545?itemId=23629857894&vendorItemId=91020946616&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7970258723?itemId=24496747527&vendorItemId=92726513974&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8347871059?itemId=24928936152&vendorItemId=92271622896&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8717341255?itemId=24736214672&vendorItemId=92418958592&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8457735882?itemId=24674221395&vendorItemId=92675765468&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8388749968?itemId=25192013141&vendorItemId=92188741362&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615645611?itemId=25179706287&vendorItemId=92785438411&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8496332594?itemId=24590702355&vendorItemId=93070211161&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6155868999?itemId=23934079266&vendorItemId=92577102506&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8597694917?itemId=24929810347&vendorItemId=92502424807&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6988423390?itemId=24666412014&vendorItemId=92727071001&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8909840291?itemId=26026497179&vendorItemId=93008134693&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312500&vendorItemId=91088074324&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8021863197?itemId=22416310374&vendorItemId=93073083012&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8453200536?itemId=24457911406&vendorItemId=93062487149&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=23934383070&vendorItemId=92718627282&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600653&vendorItemId=87340557636&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8034468149?itemId=24593812729&vendorItemId=93108926863&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7655076552?itemId=23388241798&vendorItemId=92024140595&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132881?itemId=25985795689&vendorItemId=93129766336&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6155868999?itemId=24661571929&vendorItemId=92084757598&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7719635109?itemId=24666241095&vendorItemId=92621038000&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24496771964&vendorItemId=92714987488&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8159835017?itemId=24637525998&vendorItemId=93133353508&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312127&vendorItemId=91088073889&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6321011350?itemId=22681215200&vendorItemId=90711824645&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8419601789?itemId=24351065868&vendorItemId=91366487133&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8194779139?itemId=24570524486&vendorItemId=93051878807&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6790571431?itemId=15997176880&vendorItemId=92768340652&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8037230169?itemId=24882607625&vendorItemId=92484781730&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7881775314?itemId=21556872065&vendorItemId=91652857857&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8755569605?itemId=25455147329&vendorItemId=92682012939&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8007155804?itemId=22321998325&vendorItemId=92142537810&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5381062413?itemId=7992531468&vendorItemId=91801006622&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6999755659?itemId=6343508428&vendorItemId=93052158838&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600276&vendorItemId=87340557110&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536742&vendorItemId=91592064825&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6321694223?itemId=23978391398&vendorItemId=91996866579&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009006213?itemId=24627029198&vendorItemId=92786690050&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8347871059?itemId=24113866402&vendorItemId=92566011488&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7219639358?itemId=24930967617&vendorItemId=92075565302&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7665226060?itemId=23642899094&vendorItemId=93052024507&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8039909783?itemId=25507951322&vendorItemId=93073420345&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8007155804?itemId=25265706401&vendorItemId=92261509214&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8034468149?itemId=24593812732&vendorItemId=93055097268&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6515706092?itemId=24030465837&vendorItemId=92508099706&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8419601789?itemId=24351065871&vendorItemId=92838305550&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8755569605?itemId=25455147335&vendorItemId=92682001364&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=24541809671&vendorItemId=91554287339&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748833?itemId=24875536741&vendorItemId=91592064817&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7970258723?itemId=25210140698&vendorItemId=92340916894&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600267&vendorItemId=87340557103&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25052246070&vendorItemId=93059879150&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25153264696&vendorItemId=93056020606&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7958495982?itemId=24666508615&vendorItemId=91676858643&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=25993489592&vendorItemId=93120409922&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312485&vendorItemId=91088074228&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7059056549?itemId=3849414266&vendorItemId=93118943088&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7549464894?itemId=25645209336&vendorItemId=92635142668&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24760507221&vendorItemId=93059878301&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8933220099?itemId=24279964131&vendorItemId=92176780408&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600487&vendorItemId=87340557355&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553625?itemId=25789834106&vendorItemId=92777610880&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7358399326?itemId=24563739631&vendorItemId=93108784050&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8665570383?itemId=25150893660&vendorItemId=92149372672&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8347871059?itemId=24113866427&vendorItemId=92292245983&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7495250071?itemId=24543374688&vendorItemId=91555811879&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8056509310?itemId=24381908458&vendorItemId=93054845687&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7234871047?itemId=25186285785&vendorItemId=92637198823&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24536379121&vendorItemId=93102017218&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8909840291?itemId=26026497175&vendorItemId=93008134680&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8533841909?itemId=24703067467&vendorItemId=91712661733&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7405190397?itemId=19175222809&vendorItemId=92878152012&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7276727876?itemId=25246547696&vendorItemId=92820199335&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8560049227?itemId=25321470818&vendorItemId=92316419267&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8755569605?itemId=25455147336&vendorItemId=92967376599&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25158180640&vendorItemId=93059878669&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313125&vendorItemId=91088074932&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8390506241?itemId=24253589651&vendorItemId=91315899879&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=22489329378&vendorItemId=93051533738&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=24885449741&vendorItemId=92715460319&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=21121578360&vendorItemId=92380655410&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=25247093637&vendorItemId=93044546766&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615021245?itemId=24990287290&vendorItemId=92524302451&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25120551828&vendorItemId=92526105354&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8591230625?itemId=24909898780&vendorItemId=91916338953&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8454289958?itemId=25727683869&vendorItemId=92796893202&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8026844340?itemId=24366985333&vendorItemId=92486515467&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8438585578?itemId=24407670118&vendorItemId=92148656781&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25281984197&vendorItemId=92526160310&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8117663564?itemId=23016675372&vendorItemId=93057396421&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24875536732&vendorItemId=91592064511&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6091199349?itemId=11356857201&vendorItemId=92816315183&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7834159285?itemId=25042764800&vendorItemId=92777722285&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8449734807?itemId=24445472227&vendorItemId=92460748980&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615468071?itemId=24991719950&vendorItemId=92458897691&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8351420670?itemId=24596205685&vendorItemId=93051665454&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7728777508?itemId=20573290494&vendorItemId=93008315195&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8215371059?itemId=25280714776&vendorItemId=92743487043&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7655076552?itemId=22609758122&vendorItemId=92826347228&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8438585578?itemId=24407670116&vendorItemId=93063303147&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25052246072&vendorItemId=93059878269&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8118595680?itemId=24536427212&vendorItemId=93061083359&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24535242210&vendorItemId=93135783617&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=23934383073&vendorItemId=92718627311&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7655076552?itemId=22187676227&vendorItemId=92826371149&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7996658881?itemId=22247232519&vendorItemId=93060865730&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25249141113&vendorItemId=93135783564&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8515252454?itemId=24651104533&vendorItemId=92315441250&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8856795554?itemId=25823123282&vendorItemId=92759867218&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8369827873?itemId=24185663184&vendorItemId=92518689911&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8438585578?itemId=24407670115&vendorItemId=92602747855&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316873869?itemId=24002976547&vendorItemId=93044833213&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8371447702?itemId=25353984915&vendorItemId=92496384697&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7799776622?itemId=25191864404&vendorItemId=92735422900&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8630364624?itemId=25038413552&vendorItemId=92767726953&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8009006213?itemId=24627029200&vendorItemId=92004001875&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8755569605?itemId=25455147340&vendorItemId=92682012972&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312136&vendorItemId=91088073955&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8233190921?itemId=24558981448&vendorItemId=93052783011&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312130&vendorItemId=91088073904&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7665226060?itemId=22315225951&vendorItemId=93052024905&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8338145551?itemId=24077731972&vendorItemId=92508673792&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6802464494?itemId=16061336798&vendorItemId=92687233984&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5574519945?itemId=8889485175&vendorItemId=92378897341&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8059785906?itemId=22636159148&vendorItemId=90044609363&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888636?itemId=20252601040&vendorItemId=87340557937&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7925889780?itemId=25158180644&vendorItemId=93059879082&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25102669525&vendorItemId=93130241498&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7984128326?itemId=22168571735&vendorItemId=92242055251&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8560049227?itemId=24788534901&vendorItemId=93053698691&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25249141119&vendorItemId=92959550387&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8273061636?itemId=23844991054&vendorItemId=91975406659&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615646113?itemId=25441223853&vendorItemId=92524335490&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312668&vendorItemId=91088074560&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8496332594?itemId=24590702325&vendorItemId=93054237089&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25211233472&vendorItemId=92526160379&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8493748732?itemId=24580285078&vendorItemId=91592064527&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8449734807?itemId=25169584179&vendorItemId=92189757903&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8616588621?itemId=24995924180&vendorItemId=92636004160&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434837?itemId=24068312526&vendorItemId=91088074436&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/4368556884?itemId=3849413191&vendorItemId=92820676231&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8540019824?itemId=24724662687&vendorItemId=91733825073&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8037230169?itemId=24882607620&vendorItemId=92602370161&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7565826275?itemId=24711893690&vendorItemId=92680155493&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8909820958?itemId=26026389094&vendorItemId=93008027607&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8145132877?itemId=23156170361&vendorItemId=90783613441&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7124226770?itemId=25190201031&vendorItemId=93056020452&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7958602013?itemId=25248455257&vendorItemId=92244404219&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7792577965?itemId=25057797392&vendorItemId=92880431904&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8496332233?itemId=24590700646&vendorItemId=92719199264&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7405190397?itemId=21256208085&vendorItemId=92871149878&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8388749968?itemId=24247618087&vendorItemId=92237269995&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/6164137813?itemId=11982788649&vendorItemId=92375683401&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8584991581?itemId=24887314255&vendorItemId=92411579702&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8548075156?itemId=24753234104&vendorItemId=92924441259&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=24557907986&vendorItemId=92526104860&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8249884714?itemId=23749264047&vendorItemId=93130651124&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8513454505?itemId=24644788498&vendorItemId=92621048573&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7735827059?itemId=21575519156&vendorItemId=88766655152&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5570041486?itemId=22602317977&vendorItemId=92239150341&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7495250071?itemId=25153364505&vendorItemId=92525190979&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8388749968?itemId=25592532863&vendorItemId=92583291059&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8297773342?itemId=25249141116&vendorItemId=93135783671&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316504953?itemId=25176722422&vendorItemId=92602709141&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8449734807?itemId=24445472204&vendorItemId=92189757911&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8233190921?itemId=24711957602&vendorItemId=93052782392&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7665226060?itemId=22683849279&vendorItemId=92130128395&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8239560769?itemId=24590517152&vendorItemId=91732964779&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7655076552?itemId=24652563814&vendorItemId=92237047063&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8073129456?itemId=22731436464&vendorItemId=92789078007&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8554491680?itemId=24771065097&vendorItemId=91849758079&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434673?itemId=24068312134&vendorItemId=91088073935&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7701364844?itemId=22489318057&vendorItemId=92001580848&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7655076552?itemId=24930475329&vendorItemId=92826371106&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8533841909?itemId=24703067462&vendorItemId=91712661725&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8159835017?itemId=23258217562&vendorItemId=92093771615&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316504953?itemId=25176722420&vendorItemId=93063085068&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8533841909?itemId=24703067469&vendorItemId=91712661740&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8923461613?itemId=26078422474&vendorItemId=93059391150&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835166&vendorItemId=92777611770&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8351420670?itemId=24127647226&vendorItemId=93051646583&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615646113?itemId=25585144819&vendorItemId=93118000252&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434891?itemId=24068312671&vendorItemId=91088074607&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8007155804?itemId=25265725507&vendorItemId=92261527614&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8027176629?itemId=25259839136&vendorItemId=93111979229&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553627?itemId=25789834132&vendorItemId=92777610922&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8909820958?itemId=26026389089&vendorItemId=93008027594&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8316504953?itemId=24001383518&vendorItemId=92635387736&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835171&vendorItemId=92777611883&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8558735297?itemId=25647015050&vendorItemId=92636917991&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8249884714?itemId=24899215695&vendorItemId=92559749898&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835165&vendorItemId=92777611740&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8118595680?itemId=24662611651&vendorItemId=93097334581&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8615646113?itemId=25585145485&vendorItemId=93129785311&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553625?itemId=25789834112&vendorItemId=92777610919&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553627?itemId=25789834136&vendorItemId=92777610938&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8616745358?itemId=24996471945&vendorItemId=92717410305&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/5570041486?itemId=22729848809&vendorItemId=91655636879&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8116588203?itemId=24034738367&vendorItemId=92526339971&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553625?itemId=25789834104&vendorItemId=92777610865&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835170&vendorItemId=92777611860&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835150&vendorItemId=92777611549&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8909820958?itemId=26026389092&vendorItemId=93008027599&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8233190921?itemId=25178366218&vendorItemId=93060889346&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8883215099?itemId=25927624238&vendorItemId=92913006932&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553625?itemId=25789834120&vendorItemId=92777610951&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8728887005?itemId=25360797159&vendorItemId=92767706296&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600911&vendorItemId=87340557834&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835167&vendorItemId=92777611794&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553625?itemId=25789834115&vendorItemId=92777610933&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/7630888717?itemId=20252600455&vendorItemId=87340557298&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8335434969?itemId=24068313113&vendorItemId=91088074875&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8847553844?itemId=25789835156&vendorItemId=92777611584&sourceType=CATEGORY&categoryId=497144",
"https://www.coupang.com/vp/products/8497209411?itemId=24593741615&vendorItemId=91605357868&sourceType=CATEGORY&categoryId=497144",
]

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        results = list(executor.map(process_item, set(urls)))

    print("All tasks completed.")

if __name__ == '__main__':
    main()

print(results_list)
df = pd.DataFrame(results_list)

# Export to Excel
output_path = "Coupang_Sample_25_07_2025.xlsx"
df.to_excel(output_path, index=False)

print(f"Excel file saved to {output_path}")



