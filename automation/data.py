"""
**Created on 2018-03-15 17:12:08**

***@author: Wai***

DATA module for automated testing exercise
"""

START_URL = "https://www.ebay.com.au/"
EBAY_DATA = {"Search top 5 brands of Electronics category": [
                                                    {"steps": ["//li[@class='hl-cat-nav__js-tab']//a[text()='Electronics']"]},      
                                                    {"check": {"Top Brand/Store 1: Bing Lee": "//li[1]/a[text()='Bing Lee']", 
                                                               "Top Brand/Store 2: Dell": "//li[2]/a[text()='Dell']",
                                                               "Top Brand/Store 3: EB Games": "//li[3]/a[text()='EB Games']",
                                                               "Top Brand/Store 4: Futu Online": "//li[4]/a[text()='Futu Online']",
                                                               "Top Brand/Store 5: KG Electronics": "//li[5]/a[text()='KG Electronics']"}}],
            "Add item to shopping cart & validate the navigation of pages": [
                                                    {"steps": ["//li[@class='hl-cat-nav__js-tab']//a[text()='Electronics']"]},    
                                                    {"check": {"Electronics Category Header": "//h1[text()='Electronics']"}},  
                                                    {"steps": ["//div[text()='Laptops & Tablets']",
                                                               "//div[text()='Apple Laptops']"]},   
                                                    {"check": {"Apple Laptops Category Header": "//h1/span[text()='Apple Laptops']"}},  
                                                    {"steps": ["//h3[contains(text(),'Apple Macbook Pro 13-Inch')]",
                                                               "//a[contains(text(),'Add to cart')]"]}, 
                                                    {"check": {"Your eBay Shopping Cart Header": "//h1[text()='Your eBay Shopping Cart']"}}, 
                                                    {"steps": ["//a[text()='Proceed to checkout']",
                                                               "//input[contains(@value,'Continue as')]"]},    
                                                    {"check": {"Confirm and Pay Button": "//button[text()='Confirm and pay']"}}],
                }
                                              
                                              