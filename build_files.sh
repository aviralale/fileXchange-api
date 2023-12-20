echo " BUILD START"
python3.11.7 -m pip install -r requirements.txt
python3.11.7 manage.py collectstatic --noinput --clear
echo " BUILD END" 
