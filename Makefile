
reset-db : 
	! test -f results.db || rm results.db
	$(MAKE) results.db

results.db:
	sqlite3 results.db < results-schema.sql

run-check:
	./site_health/check.py

serve:
	FLASK_APP=site_health/server.py python -m flask run
