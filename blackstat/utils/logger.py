from loguru import logger
import sys
from pathlib import Path

def setup_logger(name: str = "price_agent"):
    """
    Configures loguru logger.
    Note: Loguru uses a global logger, so 'name' is less relevant for the instance 
    but we keep the signature for compatibility.
    """
    # Remove default handler to avoid duplicate logs if re-run
    logger.remove()
    
    # Add console handler
    logger.add(sys.stderr, level="INFO", colorize=True, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>")
    
    # Create logs directory
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "price_agent.log"
    
    # Add file handler with rotation and colors enabled (as requested)
    logger.add(
        log_file, 
        rotation="10 MB", 
        level="DEBUG", 
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
    )
    
    return logger
