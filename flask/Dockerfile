# 使用python 鏡像為基底
FROM python

# 設定環境變數<key> <value>
# ENV SECRET_KEY A_VERY_LONG_SECRET_KEY


# 設定工作目錄
WORKDIR /srv/flask
# 複製本地 -> container工作目錄
COPY . .

# pip更新與安裝相關套件
RUN pip install --upgrade pip \
&& pip install -r requirements.txt

# 開放3000連接至container
EXPOSE 3000

# 設定當run images自動執行命令
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:3000", "app:create_app('prod')"]