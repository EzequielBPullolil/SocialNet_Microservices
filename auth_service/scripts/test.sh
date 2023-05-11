export PYTHONPATH='.'

export DATABASE_URI='postgresql://usertestservices:testuser@localhost/authservice_db_test' 

clear
pytest -s -vvvv $1 $2
