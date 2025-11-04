package com.orange.adv.ihm.service;

import io.modelcontextprotocol.client.McpSyncClient;
import org.springframework.stereotype.Service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.List;

@Service
public class DiagnosticService {

    private static final Logger logger = LoggerFactory.getLogger(DiagnosticService.class);
    private final List<McpSyncClient> clients;


    public DiagnosticService(List<McpSyncClient> clients) {
        this.clients = clients;

    }

    /**
     * Logs all available MCP tools with detailed information
     */
    public void logAvailableTools() {

        logger.info("EnhancedAiAgent initialized successfully");
        if (clients == null || clients.isEmpty()) {
            logger.warn("No MCP clients configured!");
            return;
        }

        logger.info("Checking available MCP tools across {} clients...", clients.size());

        for (McpSyncClient client : clients) {
            try {
                logger.info("🔍 Connecting to MCP client: {}", client.getClass().getSimpleName());

                var toolsResponse = client.listTools();
                if (toolsResponse == null || toolsResponse.tools() == null) {
                    logger.warn("No tools available for this MCP client");
                    continue;
                }

                logger.info("🛠️ Found {} tools:", toolsResponse.tools().size());

                toolsResponse.tools().forEach(tool -> {
                    logger.info("----------------------------------------");
                    logger.info("Tool Name: {}", tool.name());
                    logger.info("Description: {}", tool.description());
                    logger.info("Input Schema: {}", tool.inputSchema());
                    logger.info("----------------------------------------");
                });

            } catch (Exception e) {
                logger.error("❌ Error while checking tools for MCP client", e);
            }
        }
    }

    /**
     * Returns a formatted string with all available tools information
     */
    public String getAvailableToolsReport() {
        StringBuilder report = new StringBuilder();

        if (clients == null || clients.isEmpty()) {
            return "No MCP clients configured!";
        }

        report.append(String.format("Available MCP Tools Report (%d clients)%n%n", clients.size()));

        for (McpSyncClient client : clients) {
            try {
                report.append(String.format("=== Client: %s ===%n", client.getClass().getSimpleName()));

                var toolsResponse = client.listTools();
                if (toolsResponse == null || toolsResponse.tools() == null) {
                    report.append("No tools available for this client\n\n");
                    continue;
                }

                report.append(String.format("Total Tools: %d%n%n", toolsResponse.tools().size()));

                toolsResponse.tools().forEach(tool -> {
                    report.append(String.format("🛠️ Tool: %s%n", tool.name()));
//                    report.append(String.format("📝 Description: %s%n", tool.description()));
//                    report.append(String.format("📋 Input Schema: %s%n%n", tool.inputSchema()));
                });

            } catch (Exception e) {
                report.append(String.format("❌ Error checking tools: %s%n", e.getMessage()));
            }
            report.append("\n");
        }

        return report.toString();
    }
}