- To scrape sub sectors from https://www.amazon.ae/

|       Field        | Description  |
|:------------------:|:------------:|
|         id         |              |
|   category_name    |              |
|     parent_id      | id of parent |
|        url         |              |
|  all_child_parsed  |              |
|     timestamp      |              |
|        asin        |              |
|        name        |              |
| technical_details  |              |
|       price        |              |
|       stock        |              |
|       stars        |              |
| number_of_reviews  |              |
|   product_images   |              |
| shipping_cost_info |              |


- images saved in tree folder
- product normally has 1 main product and a couple of image as gallery
- 1 main product image
- and an image gallery
- product row will have
- main_image, image_gallery_paths main_image is text
- image_gallery_paths is json array , ['xxxx/image1.jpg', 'xxxx/image2.jpg', '', ]where xxxx, is first 4 chars of md5(product asin)
- per prodct we save the images and image gallery
- around 5 to 7 images depends on product