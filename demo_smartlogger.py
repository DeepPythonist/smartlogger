#!/usr/bin/env python3
"""
SmartLogger Demo - نمایش قابلیت‌های رنگی سیستم لاگ
"""

import time
import logging

# فعالسازی SmartLogger
import smartlogger.auto

# تنظیم logging برای نمایش تمام سطوح
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ایجاد logger های مختلف
main_logger = logging.getLogger('SmartLogger.Demo')
app_logger = logging.getLogger('App.Service')
db_logger = logging.getLogger('Database.Connection')
auth_logger = logging.getLogger('Auth.Security')

def demo_basic_logging():
    """نمایش لاگ‌های پایه با رنگ‌های مختلف"""
    print("🎨 === Demo: Basic Colored Logging ===")
    
    main_logger.debug("Debug: Debugging application startup")
    time.sleep(0.5)
    
    main_logger.info("Info: Application started successfully")
    time.sleep(0.5)
    
    main_logger.warning("Warning: High memory usage detected")
    time.sleep(0.5)
    
    main_logger.error("Error: Failed to connect to external API")
    time.sleep(0.5)
    
    main_logger.critical("Critical: System running out of disk space!")
    time.sleep(1)

def demo_application_scenario():
    """سناریو واقعی اپلیکیشن"""
    print("\n📱 === Demo: Real Application Scenario ===")
    
    app_logger.info("Starting web server on port 8080")
    time.sleep(0.3)
    
    auth_logger.info("User 'admin' logged in successfully")
    time.sleep(0.3)
    
    db_logger.debug("Executing query: SELECT * FROM users")
    time.sleep(0.3)
    
    app_logger.warning("API rate limit exceeded for IP 192.168.1.100")
    time.sleep(0.3)
    
    auth_logger.error("Failed login attempt for user 'hacker'")
    time.sleep(0.3)
    
    db_logger.critical("Database connection pool exhausted!")
    time.sleep(0.3)
    
    app_logger.info("Server shutdown initiated")
    time.sleep(1)

def demo_custom_colors():
    """نمایش رنگ‌های سفارشی"""
    print("\n🌈 === Demo: Custom Color Scheme ===")
    
    # تغییر به رنگ‌های سفارشی
    from smartlogger.config.colors import ANSIColors
    import smartlogger
    
    smartlogger.configure_colors({
        'DEBUG': ANSIColors.CYAN,
        'INFO': ANSIColors.BRIGHT_GREEN,
        'WARNING': ANSIColors.MAGENTA,
        'ERROR': ANSIColors.BRIGHT_RED,
        'CRITICAL': ANSIColors.BOLD + ANSIColors.YELLOW + ANSIColors.BG_RED
    })
    
    custom_logger = logging.getLogger('Custom.Colors')
    
    custom_logger.debug("Debug with CYAN color")
    time.sleep(0.3)
    
    custom_logger.info("Info with BRIGHT GREEN color")
    time.sleep(0.3)
    
    custom_logger.warning("Warning with MAGENTA color")
    time.sleep(0.3)
    
    custom_logger.error("Error with BRIGHT RED color")
    time.sleep(0.3)
    
    custom_logger.critical("Critical with BOLD YELLOW on RED background!")
    time.sleep(1)

def demo_multiple_loggers():
    """نمایش logger های متعدد با context مختلف"""
    print("\n🔧 === Demo: Multiple Logger Context ===")
    
    loggers = [
        ('Frontend.React', 'Component mounted successfully'),
        ('Backend.API', 'Processing user request'),
        ('Cache.Redis', 'Cache miss for key: user_123'),
        ('Queue.Worker', 'Processing background job'),
        ('Monitoring.Metrics', 'CPU usage: 85%'),
        ('Security.WAF', 'Blocked suspicious request')
    ]
    
    for logger_name, message in loggers:
        logger = logging.getLogger(logger_name)
        
        if 'Error' in message or 'Failed' in message:
            logger.error(message)
        elif 'Warning' in message or 'suspicious' in message:
            logger.warning(message)
        elif 'CPU usage: 85%' in message:
            logger.warning(message)
        else:
            logger.info(message)
        
        time.sleep(0.4)

def demo_error_scenarios():
    """نمایش سناریوهای خطا"""
    print("\n🚨 === Demo: Error Scenarios ===")
    
    error_logger = logging.getLogger('ErrorDemo')
    
    scenarios = [
        ("Connection timeout to database", "error"),
        ("Invalid API key provided", "error"),
        ("Memory usage above 90%", "warning"),
        ("Disk space below 10%", "critical"),
        ("SSL certificate expires in 7 days", "warning"),
        ("Authentication service unavailable", "critical"),
        ("Backup process completed", "info"),
        ("System health check passed", "info")
    ]
    
    for message, level in scenarios:
        getattr(error_logger, level)(f"{level.upper()}: {message}")
        time.sleep(0.5)

def main():
    """اجرای تمام demo ها"""
    print("🎯 SmartLogger Demonstration")
    print("=" * 50)
    print("نمایش قابلیت‌های رنگی سیستم لاگ پایتون")
    print("=" * 50)
    
    # اجرای تمام demo ها
    demo_basic_logging()
    demo_application_scenario()
    demo_custom_colors()
    demo_multiple_loggers()
    demo_error_scenarios()
    
    print("\n✅ === Demo Completed ===")
    print("تمام قابلیت‌های SmartLogger نمایش داده شد!")
    print("رنگ‌ها بر اساس سطح لاگ تنظیم شده‌اند:")
    print("🔵 DEBUG (آبی)")
    print("🟢 INFO (سبز)")  
    print("🟡 WARNING (زرد)")
    print("🔴 ERROR (قرمز)")
    print("🟥 CRITICAL (قرمز Bold)")

if __name__ == "__main__":
    main() 