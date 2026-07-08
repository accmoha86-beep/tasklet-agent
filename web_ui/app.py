"""Flask Web UI for Tasklet Agent"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Import agent
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.core import TaskletAgent

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize agent
agent = TaskletAgent(
    model=os.getenv('LLM_MODEL', 'gpt-4'),
    api_key=os.getenv('LLM_API_KEY'),
    provider=os.getenv('LLM_PROVIDER', 'openai'),
    max_steps=int(os.getenv('AGENT_MAX_STEPS', '10')),
    debug=os.getenv('DEBUG_MODE', 'false').lower() == 'true'
)

# Store execution history
execution_history = []


@app.route('/')
def index():
    """Serve the main UI"""
    return render_template('index.html')


@app.route('/api/execute', methods=['POST'])
def execute_task():
    """Execute a task with the agent"""
    try:
        data = request.json
        task = data.get('task', '').strip()
        
        if not task:
            return jsonify({'error': 'Task cannot be empty'}), 400
        
        logger.info(f"Executing task: {task}")
        
        # Run the agent
        result = agent.run(task)
        
        # Store in history
        execution_history.append({
            'id': len(execution_history) + 1,
            'task': task,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error executing task: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """Get execution history"""
    try:
        return jsonify({
            'count': len(execution_history),
            'executions': execution_history[-20:]  # Return last 20
        }), 200
    except Exception as e:
        logger.error(f"Error getting history: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/memory', methods=['GET'])
def get_memory():
    """Get agent memory"""
    try:
        memory = agent.get_memory()
        return jsonify(memory), 200
    except Exception as e:
        logger.error(f"Error getting memory: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    """Clear agent memory"""
    try:
        agent.clear_memory()
        return jsonify({'status': 'success', 'message': 'Memory cleared'}), 200
    except Exception as e:
        logger.error(f"Error clearing memory: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get agent status"""
    try:
        return jsonify({
            'status': 'running',
            'model': agent.model,
            'provider': agent.provider_name,
            'max_steps': agent.max_steps,
            'executions': len(execution_history),
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Error getting status: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('WEB_UI_PORT', '5000'))
    debug = os.getenv('DEBUG_MODE', 'false').lower() == 'true'
    logger.info(f"Starting Web UI on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
