#!/usr/bin/env python3

import logging
import smartlogger.auto

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger('demo')

def main():
    print("SmartLogger Demo - Colorful Logging")
    print("=" * 40)
    
    logger.debug("This is a DEBUG message - Blue")
    logger.info("This is an INFO message - Green")
    logger.warning("This is a WARNING message - Yellow")
    logger.error("This is an ERROR message - Red")
    logger.critical("This is a CRITICAL message - Bright Red")
    
    print("\nTesting with different loggers:")
    print("-" * 30)
    
    app_logger = logging.getLogger('app')
    db_logger = logging.getLogger('database')
    api_logger = logging.getLogger('api')
    
    app_logger.info("Application started successfully")
    db_logger.warning("Connection pool is running low")
    api_logger.error("Failed to process request")
    
    print("\nDemo completed!")

if __name__ == "__main__":
    main() 