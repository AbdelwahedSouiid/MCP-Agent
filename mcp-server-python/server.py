#!/usr/bin/env python3
"""
Serveur MCP simple sans dépendances Windows problématiques
"""

import json
import sys
import asyncio
import logging
from typing import Dict, List, Any

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleMCPServer:
    def __init__(self, name: str):
        self.name = name
        self.tools = {}
        
    def tool(self, name: str = None):
        """Décorateur pour enregistrer les outils"""
        def decorator(func):
            tool_name = name or func.__name__
            self.tools[tool_name] = {
                'function': func,
                'description': func.__doc__ or '',
                'name': tool_name
            }
            return func
        return decorator
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une requête MCP"""
        try:
            method = request.get('method')
            request_id = request.get('id')
            
            if method == 'initialize':
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'protocolVersion': '2024-11-05',
                        'capabilities': {
                            'tools': {}
                        },
                        'serverInfo': {
                            'name': self.name,
                            'version': '1.0.0'
                        }
                    }
                }
            
            elif method == 'tools/list':
                tools_list = []
                for tool_name, tool_info in self.tools.items():
                    tools_list.append({
                        'name': tool_name,
                        'description': tool_info['description'],
                        'inputSchema': {
                            'type': 'object',
                            'properties': {},
                            'required': []
                        }
                    })
                
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'result': {
                        'tools': tools_list
                    }
                }
            
            elif method == 'tools/call':
                tool_name = request['params']['name']
                arguments = request['params'].get('arguments', {})
                
                if tool_name in self.tools:
                    try:
                        result = self.tools[tool_name]['function'](**arguments)
                        return {
                            'jsonrpc': '2.0',
                            'id': request_id,
                            'result': {
                                'content': [
                                    {
                                        'type': 'text',
                                        'text': json.dumps(result, ensure_ascii=False, indent=2)
                                    }
                                ]
                            }
                        }
                    except Exception as e:
                        return {
                            'jsonrpc': '2.0',
                            'id': request_id,
                            'error': {
                                'code': -32603,
                                'message': f'Erreur lors de l\'exécution de l\'outil: {str(e)}'
                            }
                        }
                else:
                    return {
                        'jsonrpc': '2.0',
                        'id': request_id,
                        'error': {
                            'code': -32601,
                            'message': f'Outil non trouvé: {tool_name}'
                        }
                    }
            
            else:
                return {
                    'jsonrpc': '2.0',
                    'id': request_id,
                    'error': {
                        'code': -32601,
                        'message': f'Méthode non supportée: {method}'
                    }
                }
        
        except Exception as e:
            logger.error(f"Erreur lors du traitement de la requête: {e}")
            return {
                'jsonrpc': '2.0',
                'id': request.get('id'),
                'error': {
                    'code': -32603,
                    'message': f'Erreur interne du serveur: {str(e)}'
                }
            }
    
    async def run(self):
        """Lance le serveur MCP en mode stdio"""
        logger.info(f"Démarrage du serveur MCP: {self.name}")
        
        try:
            while True:
                # Lire depuis stdin
                line = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                try:
                    # Parser la requête JSON
                    request = json.loads(line)
                    logger.info(f"Requête reçue: {request.get('method', 'unknown')}")
                    
                    # Traiter la requête
                    response = await self.handle_request(request)
                    
                    # Envoyer la réponse
                    print(json.dumps(response, ensure_ascii=False))
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    logger.error(f"Erreur de parsing JSON: {e}")
                    continue
                except Exception as e:
                    logger.error(f"Erreur lors du traitement: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Erreur fatale du serveur: {e}")
            raise

# Créer une instance du serveur
mcp = SimpleMCPServer("Python MCP Server")

@mcp.tool()
def get_user_info(name: str) -> dict:
    """
    Get Description About given User:
    - User: nom de l'utilisateur à rechercher
    """
    logger.info(f"Recherche d'informations pour l'utilisateur: {name}")
    
    # Données utilisateurs simulées
    users_data = {
        "abdel": {
            "username": "Abdel_Exploitant",
            "description": "Développeur principal du projet ADV-PFE",
            "role": "Lead Developer",
            "email": "abdel@orange.com"
        },
        "exploitant": {
            "username": "Exploitant_Utilisateur", 
            "description": "Explorer la plupart des fonctionnalités dans la plateforme",
            "role": "System Administrator",
            "email": "exploitant@orange.com"
        },
        "admin": {
            "username": "Admin_Système",
            "description": "Administrateur système avec tous les privilèges",
            "role": "System Admin",
            "email": "admin@orange.com"
        }
    }
    
    # Rechercher l'utilisateur (insensible à la casse)
    user_key = name.lower()
    if user_key in users_data:
        result = users_data[user_key]
        logger.info(f"Utilisateur trouvé: {result}")
        return result
    else:
        result = {
            "username": f"Utilisateur_{name}",
            "description": f"Utilisateur {name} non trouvé dans la base de données",
            "role": "Unknown",
            "email": f"{name}@orange.com"
        }
        logger.warning(f"Utilisateur non trouvé: {name}")
        return result

@mcp.tool()
def list_all_users() -> list:
    """
    Liste tous les utilisateurs disponibles
    """
    logger.info("Récupération de la liste des utilisateurs")
    
    users = [
        {
            "name": "abdel",
            "username": "Abdel_Exploitant",
            "role": "Lead Developer"
        },
        {
            "name": "exploitant", 
            "username": "Exploitant_Utilisateur",
            "role": "System Administrator"
        },
        {
            "name": "admin",
            "username": "Admin_Système", 
            "role": "System Admin"
        }
    ]
    
    logger.info(f"Retour de {len(users)} utilisateurs")
    return users

@mcp.tool()
def check_user_permissions(name: str) -> dict:
    """
    Vérifie les permissions d'un utilisateur
    - name: nom de l'utilisateur
    """
    logger.info(f"Vérification des permissions pour: {name}")
    
    permissions = {
        "abdel": ["read", "write", "deploy", "admin"],
        "exploitant": ["read", "write", "execute"],
        "admin": ["read", "write", "delete", "admin", "system"]
    }
    
    user_perms = permissions.get(name.lower(), ["read"])
    
    result = {
        "user": name,
        "permissions": user_perms,
        "admin_access": "admin" in user_perms,
        "can_deploy": "deploy" in user_perms
    }
    
    logger.info(f"Permissions pour {name}: {result}")
    return result

@mcp.tool()
def get_project_info() -> dict:
    """
    Retourne les informations du projet ADV-PFE
    """
    logger.info("Récupération des informations du projet")
    
    project_info = {
        "name": "ADV-PFE",
        "description": "Projet de fin d'études - Plateforme de microservices",
        "version": "1.0.0",
        "technologies": ["Spring Boot", "Java", "PostgreSQL", "Redis", "Docker"],
        "microservices": [
            "gateway-service",
            "auth-service", 
            "user-service",
            "notification-service"
        ],
        "status": "En développement"
    }
    
    logger.info("Informations du projet retournées")
    return project_info

if __name__ == "__main__":
    try:
        asyncio.run(mcp.run())
    except KeyboardInterrupt:
        logger.info("Arrêt du serveur MCP...")
    except Exception as e:
        logger.error(f"Erreur fatale: {e}")