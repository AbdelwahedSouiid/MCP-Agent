import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
import glob

# Création du dossier de logs s'il n'existe pas
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

class LoggerConfig:
    @staticmethod
    def setup_logger(name, log_file, level=logging.INFO):
        """
        Configure un logger qui écri    t dans un fichier spécifique
        
        Args:
            name: Nom du logger
            log_file: Nom du fichier de log
            level: Niveau de logging
        """
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d (%(funcName)s) - %(message)s'
        )
        
        log_path = log_dir / log_file
        
        # Handler fichier avec rotation
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=5*1024*1024,
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # Handler console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        if not logger.handlers:
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
        
        return logger
    @staticmethod
    def clear_logs():
        """
        Supprime le contenu de tous les fichiers de logs tout en conservant les fichiers.
        Utile pour les tests ou le débogage.
        """
        try:
            log_files = glob.glob(str(log_dir / '*.log'))
            
            for log_file in log_files:
                try:
                    with open(log_file, 'w', encoding='utf-8') as f:
                        f.truncate(0)
                    app_logger.info(f"Contenu du fichier de log vidé: {os.path.basename(log_file)}")
                except Exception as e:
                    error_logger.error(f"Erreur lors du vidage de {log_file}: {str(e)}")
                    
            return True
        except Exception as e:
            error_logger.critical(f"Erreur critique dans clear_logs: {str(e)}")
            return False

# Initialisation des loggers
app_logger = LoggerConfig.setup_logger('app', 'app.log')
error_logger = LoggerConfig.setup_logger('errors', 'errors.log', level=logging.ERROR)
voice_logger = LoggerConfig.setup_logger('voice', 'voice.log')
response_logger = LoggerConfig.setup_logger('response', 'response.log')
search_logger = LoggerConfig.setup_logger('search', 'search.log')
classifier_logger = LoggerConfig.setup_logger('classifier', 'classifier.log')
mongo_logger = LoggerConfig.setup_logger('mongo', 'mongo.log')
models_logger = LoggerConfig.setup_logger('models', 'models.log')
translate_logger = LoggerConfig.setup_logger('translate', 'translate.log')
redis_logger = LoggerConfig.setup_logger('redis', 'redis.log')
warning_logger = LoggerConfig.setup_logger('warnings', 'warnings.log')