from flask import Flask, render_template, request, url_for
import os, json, datetime, random
from dbconnect import connect
from dbRedisCache import r

app = Flask(__name__)
port = int(os.getenv("PORT", 5000))

@app.route("/", methods=["GET"])
def hello():
   return render_template('index.html')


@app.route('/prob1a', methods=["POST"])
def problem1a():
	start_mag = float(request.form["start_mag"])
	end_mag = float(request.form["end_mag"])

	if (start_mag < end_mag):
		return "start magnitude must be greater than end magnitude"
	start_time = datetime.datetime.now().timestamp()
	cursor = connect.cursor()
	sql = "SELECT qi.id, latitude, longitude from qm INNER JOIN qi ON qm.id=qi.id where qi.mag between ? and ?"
	cursor.execute(sql, (end_mag, start_mag))

	result = []
	for row in cursor.fetchall():
		result.append([row[0], row[1], row[2]])
	total_time = (datetime.datetime.now().timestamp() - start_time) * 1000
	return render_template('prob1a.html', execution_time= total_time, result=result)


@app.route('/prob2a', methods=["POST"])
def problem2b():
	query_count = int(request.form["query_count1"])

	start_mag1 = float(request.form["start_mag1"])
	end_mag1 = float(request.form["end_mag1"])

	result = []
#	i = 0
	tot_time = 0
	mag1 =start_mag1
	for _ in range(query_count):

		mag2 = start_mag1 + .1

		if (mag1 > mag2):
			start_latitude = mag1
			end_latitude = mag2
		else:
			start_latitude = mag2
			end_latitude = mag1

		# start
		start_time = datetime.datetime.now().timestamp()

		cursor = connect.cursor()
		sql = "SELECT qi.id, latitude, longitude from qm INNER JOIN qi ON qm.id=qi.id where qi.mag between ? and ?"
		cursor.execute(sql, (start_latitude, end_latitude))

		# end time
		total_time = (datetime.datetime.now().timestamp() - start_time)

		result.append({
			"numbers": str(end_latitude) + " to " + str(start_latitude),
			"count": str(len(cursor.fetchall())),
			"time": str(total_time * 1000)
			})
		tot_time = tot_time + total_time
	return render_template('prob2a.html', execution_time=tot_time*1000, result=result)


@app.route('/prob10', methods=["POST"])
def problem10():
	query_count = int(request.form["query_count1"])

	start_mag1 = float(request.form["start_mag1"])
	end_mag1 = float(request.form["end_mag1"])

	result = []
#	i = 0
	tot_time = 0
	mag1 = end_mag1
	for _ in range(query_count):
		mag2 = mag1 + .1
		if mag1 <= mag2:
			start_time = datetime.datetime.now().timestamp()
			key = 'imq3_lat_' + str(mag1) + str(mag2)
			output = []
			if r.exists(key):
				output = json.loads(r.get(key))
		# start
			else:
				cursor = connect.cursor()
				sql = "SELECT qi.id, latitude, longitude from qm INNER JOIN qi ON qm.id=qi.id where qi.mag between ? and ?"
				cursor.execute(sql, (mag1, mag2))
		# end time
			total_time = (datetime.datetime.now().timestamp() - start_time)

			result.append({
				"numbers": str(mag1) + " to " + str(mag2),
				"count": str(len(cursor.fetchall())),
				"time": str(total_time * 1000)
				})
			tot_time = tot_time + total_time
		mag1 = mag2
	return render_template('prob3a.html', execution_time=tot_time*1000, result=result)


@app.route('/prob11', methods=["POST"])
def problem11():
	start_mag = float(request.form["start_mag"])
	end_mag = float(request.form["end_mag"])
	start_lat = float(request.form["start_lat"])
	end_lat = float(request.form["end_lat"])
	start_long = float(request.form["start_long"])
	end_long = float(request.form["end_long"])

	if (start_mag < end_mag):
		return "start magnitude must be greater than end magnitude"
	start_time = datetime.datetime.now().timestamp()
	cursor = connect.cursor()
	sql = "SELECT qi.id, time, place, latitude, longitude from qm INNER JOIN qi ON qm.id=qi.id where qi.mag between ? and ?"
	cursor.execute(sql, (end_mag, start_mag))

	result = []
	for row in cursor.fetchall():
		result.append([row[0], row[1], row[2]])
	total_time = (datetime.datetime.now().timestamp() - start_time) * 1000
	return render_template('prob1a.html', execution_time= total_time, result=result)


@app.route('/prob3a', methods=["POST"])
def problem3a():
	start_mag = float(request.form["start_mag"])
	end_mag = float(request.form["end_mag"])

	if (start_mag < end_mag):
		return "start magnitude must be greater than end magnitude"

	result = []
	for _ in range(query_count):

		latitude1 = round(random.uniform(end_latitude1, start_latitude1), 1)
		latitude2 = round(random.uniform(end_latitude1, start_latitude1), 1)

		if (latitude1 > latitude2):
			start_latitude = latitude1
			end_latitude = latitude2
		else:
			start_latitude = latitude2
			end_latitude = latitude1

		# start
		start_time = datetime.datetime.now().timestamp()
		key = 'imq3_lat_' + str(end_latitude) + str(start_latitude)
		output = []
		if r.exists(key):
			output = json.loads(r.get(key))
		else:
			cursor = connect.cursor()
			sql = "SELECT time, place, mag from earthquakes where latitude between ? and ?"
			cursor.execute(sql, (end_latitude, start_latitude))
			output = []
			for row in cursor.fetchall():
				output.append([row[0], row[1], round(row[2], 2)])
			r.set(key, json.dumps(output))
		# end time
		total_time = (datetime.datetime.now().timestamp() - start_time)

		result.append({
			"numbers": str(end_latitude) + " to " + str(start_latitude),
			"count": str(len(output)),
			"time": str(total_time * 1000)
			})

	return render_template('prob3a.html', result=result)


@app.route('/prob4a', methods=["POST"])
def problem4a():
	query_count = int(request.form["query_count3"])

	start_latitude1 = float(request.form["start_latitude3"])
	end_latitude1 = float(request.form["end_latitude3"])
	use_cache = (request.form["use_cache"] == "True")
	result = []
	for _ in range(query_count):

		latitude1 = round(random.uniform(end_latitude1, start_latitude1), 1)
		latitude2 = round(random.uniform(end_latitude1, start_latitude1), 1)

		if (latitude1 > latitude2):
			start_latitude = latitude1
			end_latitude = latitude2
		else:
			start_latitude = latitude2
			end_latitude = latitude1

		# start
		start_time = datetime.datetime.now().timestamp()
		key = 'imq3_lat_' + str(end_latitude) + str(start_latitude)
		output = []
		if (use_cache and r.exists(key)):
			output = json.loads(r.get(key))
		else:
			cursor = connect.cursor()
			sql = "SELECT time, place, mag from earthquakes where latitude between ? and ?"
			cursor.execute(sql, (end_latitude, start_latitude))
			output = []
			for row in cursor.fetchall():
				output.append([row[0], row[1], round(row[2], 2)])
			r.set(key, json.dumps(output))
		# end time
		total_time = (datetime.datetime.now().timestamp() - start_time)

		result.append({
			"numbers": str(end_latitude) + " to " + str(start_latitude),
			"count": str(len(output)),
			"time": str(total_time * 1000)
			})

	return render_template('prob4a.html', result=result)


@app.route('/prob1', methods=["POST"])
def problem_1():

	query_count = int(request.form["query_count"])
	use_cache = (request.form["use_cache"] == "True")

	total_time = 0

	for _ in range(query_count):

		if (use_cache):
			# cache
			if r.exists("all"):
				# start time
				start_time = datetime.datetime.now().timestamp()

				result = json.loads(r.get("all"))

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
			else:

				# start time
				start_time = datetime.datetime.now().timestamp()

				sql = "SELECT place from earthquakes"
				cursor = connect.cursor()
				cursor.execute(sql)
				output = cursor.fetchall()

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

				result = []
				for row in output:
					result.append(row[0])

				r.set("all", json.dumps(result))
			
		else:
			# no cache

			# start time
			start_time = datetime.datetime.now().timestamp()

			cursor = connect.cursor()
			sql = "SELECT place from earthquakes"
			cursor.execute(sql)
			output = cursor.fetchall()

			# end time
			total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

			result = []
			for row in output:
				result.append(row[0])

	total_time = total_time * 1000
	return render_template('prob1.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)


@app.route('/prob2', methods=["POST"])
def problem_2():
	start_magnitude = int(request.form["start_magnitude"])
	end_magnitude = int(request.form["end_magnitude"])

	query_count = int(request.form["query_count"])
	use_cache = (request.form["use_cache"] == "True")

	total_time = 0

	for _ in range(query_count):
		magnitude = round(random.uniform(start_magnitude, end_magnitude), 1)

		if (use_cache):
			# cache
			if r.exists("mag=" + str(magnitude)):
				# start time
				start_time = datetime.datetime.now().timestamp()

				result = json.loads(r.get("mag=" + str(magnitude)))

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)
			else:

				# start time
				start_time = datetime.datetime.now().timestamp()

				sql = "SELECT place from earthquakes where mag = ?"
				cursor = connect.cursor()
				cursor.execute(sql, (magnitude))
				output = cursor.fetchall()

				# end time
				total_time = total_time + (datetime.datetime.now().timestamp() - start_time)

				result = []
				for row in output:
					result.append(row[0])

				r.set("mag=" + str(magnitude), json.dumps(result))
			
		else:
			# no cache

			# start time
			start_time = datetime.datetime.now().timestamp()

			cursor = connect.cursor()
			sql = "SELECT place from earthquakes where mag = ?"
			cursor.execute(sql, (magnitude))
			output = cursor.fetchall()

			# end time
			total_time + (datetime.datetime.now().timestamp() - start_time)

			result = []
			for row in output:
				result.append(row[0])

	total_time = total_time * 1000
	return render_template('prob2.html', query_count=query_count, use_cache=use_cache, execution_time=total_time)


# if __name__ == '__main__':
# 	app.run(host='0.0.0.0', port=port)