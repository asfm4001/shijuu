# Shijuu 西啾

---
### Pages
- Home
- Products
  - 需有管理權限(is_admin)方可新增、修改、刪除商品
  - 一般使用者僅有加入購物車功能
- Categorys
  - 顯示不同種類商品
- About
- Sign In / Register
  - 登入與註冊
- CheckOut
  - 填寫收件相關資料，並儲存至訂單中
- Orders
  - 輸入訂單聯絡人電話可查詢訂單
### Tables
- User
- Cart
- Product
- Order
##### 中介表
- CartProduct
- OrderProduct
> User (1)->(1) Cart (1)->(n) CartProduct (1)->(n) Product
> User (1)->(n) Order (1)->(n) CartProduct (1)->(n) Product
### To Do List
- 修改：
  - [ ] 結帳時，輸入錯誤顯示提示訊息
  - [x] 限制僅管理權限可查詢所有訂單
  - [ ] 將購物車儲存至cookie中
  - [ ] 訂單編號輸出為hash
  - [x] 資料庫改為MySQL 113.11.28
  - [ ] Factory(工廠模式)
- 新增：
  - [x] 訂單查詢明細(各項商品數量) 113.12.02
  - [ ] 商品查詢頁籤
  - [ ] 訂單查詢頁籤
  - [x] 修改訂單出貨狀態、付款狀態 113.12.02
  - [ ] 首頁公告
  - [ ] 訂單查詢增加訂單編號
  - [ ] 忘記密碼、密碼更改
  - [ ] 404 page
  - [ ] 訂單查詢資料筆數篩選
  - [ ] 商品熱銷、折扣標籤
  - [ ] 結帳流程
  - [ ] 快速登錄、註冊(google, line)