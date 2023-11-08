import gunicorn
import logging
from flask import Flask, request, jsonify
from data_procession import generate_report  

app = Flask(__name__)

@app.route('/api/report/<report_name>', methods=['POST'])
def generate_report_endpoint(report_name):
    data = request.get_json()

    if 'metrics' not in data or 'users' not in data:
        app.logger.error("Metrics and users are required.")
        return jsonify({"error": "Metrics and users are required."}), 400

    metrics = data['metrics']
    users = data['users']

    if not metrics or not users:
        app.logger.error("Invalid metrics or users.")
        return jsonify({"error": "Invalid metrics or users."}), 400

    try:
        generate_report(report_name, metrics, users)
        app.logger.info(f"Report '{report_name}' successfully created.")
        return jsonify({"message": f"Report '{report_name}' successfully created."}), 200
    except ValueError as ve:
        app.logger.error(f"Invalid value: {str(ve)}")
        return jsonify({"error": f"Invalid value: {str(ve)}"}), 400
    except PermissionError as pe:
        app.logger.error(f"Permission denied: {str(pe)}")
        return jsonify({"error": f"Permission denied: {str(pe)}"}), 403
    except FileNotFoundError as fnf:
        app.logger.error(f"File not found: {str(fnf)}")
        return jsonify({"error": f"File not found: {str(fnf)}"}), 404
    except Exception as e:
        app.logger.error(f"Error generating report: {str(e)}")
        return jsonify({"error": f"Error generating report: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=False)