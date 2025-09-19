from flask import Blueprint, request, jsonify
from src.data_collectors.file_ingestion_collector import FileIngestionCollector

file_ingestion_bp = Blueprint('file_ingestion', __name__)

@file_ingestion_bp.route('/api/ingest/files', methods=['POST'])
def ingest_files():
    """Ingest data from existing JSON files into the database"""
    try:
        data = request.get_json()
        data_type = data.get('data_type', 'all')
        
        collector = FileIngestionCollector()
        result = collector.collect_data(data_type=data_type)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Data ingestion completed successfully',
                'results': result
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Data ingestion completed with errors',
                'results': result
            }), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@file_ingestion_bp.route('/api/ingest/status', methods=['GET'])
def get_ingestion_status():
    """Get status of file ingestion"""
    try:
        # This would return the status of the ingestion process
        # For now, we'll return a simple status
        return jsonify({
            'success': True,
            'status': 'ready',
            'message': 'File ingestion service is ready'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500