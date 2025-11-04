package com.orange.adv.ihm.service;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.stereotype.Service;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Service
public class McpLlmService {

    private static final Logger logger = LoggerFactory.getLogger(McpLlmService.class);
    private final ChatClient chatClient;
    private final ToolCallbackProvider toolCallbackProvider;

    // Répertoire de base autorisé - TRÈS IMPORTANT
    private static final String ALLOWED_BASE_PATH = "C:/Users/abdel/OneDrive/Bureau/Projects/ADV-PFE/poc-microservices";

    private static final String SYSTEM_PROMPT = """
            Vous êtes un assistant IA spécialisé dans la gestion de fichiers et répertoires via le protocole MCP.
        
            🚫 INTERDICTIONS STRICTES :
            - Ne JAMAIS utiliser des chemins absolus qui sortent du répertoire autorisé
            - Ne JAMAIS créer de dossier quand l'utilisateur demande un FICHIER
            
            ✅ COMPORTEMENT OBLIGATOIRE :
            - Travaillez UNIQUEMENT dans ce répertoire et ses sous-dossiers : "C:/Users/abdel/OneDrive/Bureau/Projects/ADV-PFE/poc-microservices"
            - Distinguez clairement entre FICHIERS et DOSSIERS
            
            Suivre les etapes de client en memoire 
       
            """;

    public McpLlmService(
            ChatClient.Builder chatClientBuilder,
            ToolCallbackProvider toolCallbackProvider
    ) {
        this.toolCallbackProvider = toolCallbackProvider;
        this.chatClient = chatClientBuilder
                .defaultToolCallbacks(toolCallbackProvider)
                .defaultSystem(SYSTEM_PROMPT)
                .defaultAdvisors(MessageChatMemoryAdvisor.builder(
                        MessageWindowChatMemory.builder().maxMessages(10).build()).build())
                .build();

        logger.info("🔐 McpLlmService initialisé avec le répertoire autorisé : {}", ALLOWED_BASE_PATH);
    }

    public String askLlm(String question) {
        logger.info("📝 Question : {}", question);

        try {
            // Amélioration de la question pour forcer l'utilisation du bon répertoire
            String enhancedQuestion = enhanceQuestionForSecurity(question);

            var response = chatClient
                    .prompt()
                    .user(enhancedQuestion)
                    .call()
                    .content();

            logger.info("✅ Réponse générée ({} caractères)", response.length());

            // Vérification post-traitement
            if (containsSecurityViolation(response)) {
                logger.warn("⚠️ Violation de sécurité détectée dans la réponse");
                return handleSecurityViolation(question);
            }

            return response;

        } catch (Exception e) {
            logger.error("❌ Erreur : {}", e.getMessage());

            // Traitement spécial pour les erreurs d'accès
            if (e.getMessage().contains("Access denied") ||
                    e.getMessage().contains("path outside allowed directories")) {
                return handleAccessDeniedError(e.getMessage(), question);
            }
            return "❌ Erreur technique : " + e.getMessage();
        }
    }

    /**
     * Améliore la question pour forcer le respect des contraintes de sécurité
     */
    private String enhanceQuestionForSecurity(String question) {
        StringBuilder enhanced = new StringBuilder();
        enhanced.append(question);

        // Instructions spécifiques selon le type de demande
        if (question.toLowerCase().contains("crée") || question.toLowerCase().contains("créer")) {
            enhanced.append("\n\n🔐 RAPPEL SÉCURITÉ : ");

            // Détection plus précise fichier vs dossier
            if (containsFileExtension(question)) {
                enhanced.append("Il s'agit d'un FICHIER. Utilisez write_file() avec le chemin complet dans : ");
            } else if (question.toLowerCase().contains("dossier") || question.toLowerCase().contains("répertoire")) {
                enhanced.append("Il s'agit d'un DOSSIER. Utilisez create_directory() avec le chemin complet dans : ");
            } else {
                enhanced.append("Analysez s'il s'agit d'un fichier (avec extension) ou dossier. Utilisez l'outil approprié dans : ");
            }

            enhanced.append(ALLOWED_BASE_PATH);
        } else if (question.toLowerCase().contains("liste") || question.toLowerCase().contains("dossier")) {
            enhanced.append("\n\n🔐 RAPPEL SÉCURITÉ : Utilisez UNIQUEMENT le répertoire autorisé : ");
            enhanced.append(ALLOWED_BASE_PATH);
        }

        enhanced.append("\n\nRépondez en français naturel avec les résultats obtenus.");
        return enhanced.toString();
    }

    /**
     * Vérifie si la question contient une extension de fichier
     */
    private boolean containsFileExtension(String question) {
        String[] extensions = {".txt", ".json", ".java", ".xml", ".properties", ".yml", ".yaml",
                ".js", ".css", ".html", ".md", ".sql", ".log", ".csv", ".pdf"};

        String lowerQuestion = question.toLowerCase();
        for (String ext : extensions) {
            if (lowerQuestion.contains(ext)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Détecte les violations de sécurité dans la réponse
     */
    private boolean containsSecurityViolation(String response) {
        return response.contains("Access denied") ||
                response.contains("path outside allowed directories") ||
                response.contains("../") ||
                (response.contains("C:/Users/abdel/OneDrive/Bureau/Projects/ADV-PFE") &&
                        !response.contains("poc-microservices"));
    }

    /**
     * Gère les erreurs d'accès refusé
     */
    private String handleAccessDeniedError(String errorMessage, String originalQuestion) {
        logger.error("🚫 Erreur d'accès détectée : {}", errorMessage);

        StringBuilder response = new StringBuilder();
        response.append("🔐 **Restriction de sécurité appliquée**\n\n");
        response.append("L'accès a été refusé car l'opération tentait de sortir du répertoire autorisé.\n\n");
        response.append("**Répertoire autorisé :** `").append(ALLOWED_BASE_PATH).append("`\n\n");

        // Suggestion basée sur la question
        if (originalQuestion.toLowerCase().contains("crée") || originalQuestion.toLowerCase().contains("créer")) {
            if (containsFileExtension(originalQuestion)) {
                response.append("**Suggestion :** Pour créer un fichier, utilisez :\n");
                response.append("- \"Crée un fichier test.txt dans le projet\"\n");
            } else {
                response.append("**Suggestion :** Pour créer un dossier, utilisez :\n");
                response.append("- \"Crée un dossier backend dans le projet\"\n");
            }
        } else if (originalQuestion.toLowerCase().contains("liste")) {
            response.append("**Suggestion :** Pour lister les dossiers du projet, reformulez votre demande comme :\n");
            response.append("- \"Liste le contenu du répertoire de travail\"\n");
            response.append("- \"Montre-moi les fichiers dans le projet\"\n");
        }

        response.append("\nToutes les opérations sont limitées à ce répertoire pour des raisons de sécurité.");
        return response.toString();
    }

    /**
     * Gère les violations de sécurité
     */
    private String handleSecurityViolation(String originalQuestion) {
        return "🔐 **Opération bloquée pour sécurité**\n\n" +
                "L'opération demandée a tenté d'accéder à des répertoires non autorisés.\n" +
                "Toutes les opérations doivent rester dans : `" + ALLOWED_BASE_PATH + "`\n\n" +
                "Veuillez reformuler votre demande en restant dans les limites autorisées.";
    }
}