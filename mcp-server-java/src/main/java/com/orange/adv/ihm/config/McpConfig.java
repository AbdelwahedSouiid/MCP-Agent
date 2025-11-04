package com.orange.adv.ihm.config;


import com.orange.adv.ihm.tools.ScopeTools;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.beans.factory.annotation.Configurable;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class McpConfig {


    private final ScopeTools scopeTools;

    public McpConfig(ScopeTools scopeTools) {
        this.scopeTools = scopeTools;
    }

    @Bean
    public MethodToolCallbackProvider getMethodeToolBack(){
        return MethodToolCallbackProvider.builder()
                .toolObjects(scopeTools)
                .build();
    }
}

