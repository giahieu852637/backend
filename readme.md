# lưu ý
OAUTH2_PROVIDER = {
    'OAUTH2_BACKEND_CLASS': 'oauth2_provider.oauth2_backends.JSONOAuthLibCore'
}
Khi chạy với postman thì comment dòng này lại



# Cách chạy cho máy mới
Goi thu vien
pip install django-cors-headers
pip install djoser
pip install pillow
pip install stripe
pip install django
pip install djangorestframework
pip install django-rest-knox
pip install markdown       # Markdown support for the browsable API.
pip install django-filter  # Filtering support
pip install django-cors-headers
pip install djoser
pip install psycopg2-binary
pip install pydrive

https://thigiacmaytinh.com/upload-file-len-google-drive-bang-python/
sudo apt install libpq-dev python3-dev


<!-- Nếu ko có django-x509 -->
pip install django-x509
pip install https://github.com/openwisp/django-x509/tarball/master
pip install -e git+git://github.com/openwisp/django-x509#egg=django-x509


<!-- pip install django-phonenumber-field -->
pip freeze > requirements

<!-- Các bước lưu ý tránh lỗi -->
sudo apt update
sudo apt install python3-pip
sudo apt install -y postgresql postgresql-contrib

<!-- Truy cap vap postgres -->
sudo -i -u postgres
psql
CREATE USER pnthanh WITH PASSWORD 'pnthanh2001';
CREATE DATABASE chinhquyendt OWNER pnthanh;

<!-- Cách xóa database -->
DROP DATABASE chinhquyendt;
SELECT
	pg_terminate_backend (pg_stat_activity.pid)
FROM
	pg_stat_activity
WHERE
	pg_stat_activity.datname = 'chinhquyendt';


\q
exit
sudo su - user


<!-- cấu hình postgresql -->
'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'spacedbv3',
        'USER': 'dangnguyen',
        'PASSWORD': 'poilkj09',
        'HOST': 'localhost',
        'PORT': '5432',


<!-- Chạy project -->
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver


<!-- Tạo user đăng nhập djangoadmin -->
python3 manage.py createsuperuser
<!-- admin -->
<!-- admin -->





<!-- Tạo project -->
create project
django-admin startproject chinhquyendtPKI_django
python3 manage.py startapp hoso



# Lỗi CROS
"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=~/chromeTemp














<!-- Tiều liệu tham khảo -->

Login Regieter
https://studygyaan.com/django/django-rest-framework-tutorial-register-login-logout
https://www.youtube.com/watch?v=Cw_jSc1NGdo
https://www.youtube.com/watch?v=DCRNavrlS8s&list=PLlVHoHHccp2_kuKovosZTK_Ftu6XwgFyH
https://app.creately.com/diagram/4qBlCNBx4tj/edit

 
