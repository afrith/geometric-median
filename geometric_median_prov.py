#!/usr/bin/env python

import psycopg2, sys
conn = psycopg2.connect('dbname=popcent')
cur = conn.cursor()

prov = sys.argv[1]

cur.execute('SELECT SUM(pop*lat)/SUM(pop) AS lat, SUM(pop*lcf*lon)/SUM(pop*lcf) AS lon FROM sal WHERE prov = %s', (prov,))
(lat, lon) = cur.fetchone()

for i in range(0,100):
    cur.execute('SELECT SUM(lat*pop/dist)/SUM(pop/dist) AS lat, SUM(lon*pop/dist)/SUM(pop/dist) FROM (SELECT pop, lon, lat, ST_Distance(Geography(ST_SetSRID(ST_MakePoint(lon, lat), 4326)), Geography(ST_SetSRID(ST_MakePoint(%s, %s), 4326))) AS dist FROM sal WHERE prov = %s) c', (lon, lat, prov))
    (lat, lon) = cur.fetchone()
    print('%2d, %f, %f' % (i, lat, lon))

cur.execute("INSERT INTO popmedian (prov, geom) SELECT %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)", (prov, lon, lat))
conn.commit()

cur.close()
conn.close()
