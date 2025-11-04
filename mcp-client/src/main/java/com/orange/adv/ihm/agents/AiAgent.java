package com.orange.adv.ihm.agents;


import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.stereotype.Service;

@Service
public class AiAgent {

    private static final String SYSTEM_PROMPT = """
        Tu es un assistant IA avec accès au système de fichiers via MCP (Model Context Protocol).
        """;

    private final ChatClient chatClient;

    public AiAgent(ChatClient.Builder client, ToolCallbackProvider toolCallbackProvider) {
        this.chatClient = client
                .defaultToolCallbacks(toolCallbackProvider)
                .defaultSystem(" Repondere selon les tools fournis ")

                .defaultAdvisors(MessageChatMemoryAdvisor.builder(MessageWindowChatMemory.builder().maxMessages(10).build()).build())
                .build();
    }

    public String askLLM(String userMessage) {
        try {
            return chatClient.prompt()
                    .system(SYSTEM_PROMPT)
                    .user(userMessage)
                    .call()
                    .content();
        } catch (Exception e) {
            return "Erreur lors de l'appel au LLM : " + e.getMessage();
        }
    }
}
