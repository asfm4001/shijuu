# Shijuu 西啾 
一個簡易的購物網站，管理者可新增商品並管理訂單。使用者可將商品加入購物車，最後結帳可使用電話查詢訂單。

## Overview

## 💡 Features 
* 新增、修改、刪除商品且可分類展示
* 註冊、登入、登出
* 使用者可將商品加入購物車，結帳後自動成立訂單，同時清空原始購物車
* 管理者可查看所有訂單，同時可修改、刪除

**Pages**
* Home
* Products
  * 需有管理權限(is_admin)方可新增、修改、刪除商品
  * 一般使用者僅有加入購物車功能
* Categorys
  * 顯示不同種類商品
* About
* Sign In / Register
  * 登入與註冊
* CheckOut
  * 填寫收件相關資料，並儲存至訂單中
* Orders
  * 輸入訂單聯絡人電話可查詢訂單
<detalis>
  <summary>Feature Features</summary>
  
  - 修改：
    - [x] 限制僅管理權限可查詢所有訂單 113.11.28
    - [x] 資料庫改為MySQL 113.11.28
    - [ ] 結帳時，輸入錯誤顯示提示訊息
    - [ ] 將購物車儲存至cookie中
    - [ ] 訂單編號輸出為hash
    - [ ] Factory(工廠模式)
  - 新增：
    - [x] 訂單查詢明細(各項商品數量) 113.12.02
    - [x] 修改訂單出貨狀態、付款狀態 113.12.02
    - [ ] 商品查詢頁籤
    - [ ] 訂單查詢頁籤
    - [ ] 首頁公告
    - [ ] 訂單查詢增加訂單編號
    - [ ] 忘記密碼、密碼更改
    - [ ] 404 page
    - [ ] 訂單查詢資料筆數篩選
    - [ ] 商品熱銷、折扣標籤
    - [ ] 結帳流程
    - [ ] 快速登錄、註冊(google, line)
</detalils>

## 流程概念 
管理者新增商品 > 使用者加入購物車 > 使用者結帳(新增訂單與清空購物車) > 管理者確認款項入帳(更改訂單狀態) > 製作商品 > 管理者出貨(更改訂單狀態)。

## 🔧 Related Work 
* 原Flask-Bootstrap因版本過舊不支援Bootstrap 4 & 5，改使用Bootstrap-Flask
* SQLAlchemy 可使用MySQL(docker)
* Bcrypt 避免儲存user真實密碼
* Flask-Login 使用sission儲存user狀態
* Database Tables(1 to 1, 1 to n, n to n)
  * User
  * Cart
  * Product
  * Order
  * CartProduct(中介表)
  * OrderProduct(中介表)
  > User (1)->(1) Cart (1)->(n) CartProduct (1)->(n) Product
  > User (1)->(n) Order (1)->(n) CartProduct (1)->(n) Product

## 🚀 Run Locally 
1. Clone至本地端
  ``` git clone https://github.com/asfm4001/shijuu.git ```
2. 部署虛擬環境並進入
  ``` 
  python3 -m venv .venv
  source /bin/activate
  ```
3. install models
  ``` pip install -r requirements.txt ```
4. 執行flask
  ``` flask run ```
5. 在[這裡](http://localhost:5000/)可訪問Shijuu 西啾
6. 測試用帳號密碼、data
   * 調整```__init__.py  ```為測試設定檔```app.config.from_object(config["test"])```
      > devp/開發; test/測試, prod/正式(DB為MySQL)
   * user/password: test123/test123
   * admin/password: superadmin/superadmin
   * 訂單查詢/聯絡電話: 0800000123
1. 關閉flask server
  <kdb>ctrl</kdb> + <kdb>c</kdb>
1. 退出虛擬環境
  ``` deactivate ```

## 🗂️ File Structure 
```
.
├── README.md
├── config.py
├── requirements.txt
├── run.py
├── instance
│   └── test-data.sqlite
└── app
    ├── __init__.py
    ├── forms.py
    ├── models.py
    ├── routes.py
    ├── static
    │   ├── assets
    │   ├── logo
    │   └── product
    │       ├── default.png
    │       └── items
    └── templates
        ├── about.html
        ├── base.html
        ├── footer.html
        ├── index.html
        ├── navbar.html
        ├── shopping_cart.html
        ├── checkout
        │   ├── details.html
        │   └── payment.html
        ├── order
        │   ├── order_delete.html
        │   ├── order_edit.html
        │   ├── order_page.html
        │   └── order_query.html
        ├── product
        │   ├── add_product.html
        │   ├── delete_product.html
        │   ├── product.html
        │   ├── product_page.html
        │   └── update_product.html
        └── user
            ├── register.html
            ├── sign-in.html
            └── user_menu.html
```