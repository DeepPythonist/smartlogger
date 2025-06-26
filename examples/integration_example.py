import logging
import smartlogger.auto

class DatabaseManager:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def connect(self):
        self.logger.info("Connecting to database...")
        self.logger.debug("Using connection string: localhost:5432")
        
    def query(self, sql):
        self.logger.debug(f"Executing query: {sql}")
        self.logger.warning("Query took longer than expected")
        
    def disconnect(self):
        self.logger.info("Database connection closed")

class APIServer:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db = DatabaseManager()
    
    def start(self):
        self.logger.info("Starting API server...")
        self.db.connect()
        
    def handle_request(self, request_id):
        self.logger.info(f"Processing request {request_id}")
        try:
            self.db.query("SELECT * FROM users")
            self.logger.info(f"Request {request_id} completed successfully")
        except Exception as e:
            self.logger.error(f"Request {request_id} failed: {e}")
            self.logger.critical("System may be unstable")

def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    server = APIServer()
    server.start()
    server.handle_request("REQ-001")
    server.handle_request("REQ-002")

if __name__ == "__main__":
    main() 