package com.orange.adv.ihm.controller;

import com.orange.adv.ihm.service.DiagnosticService;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.context.ApplicationContext;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

@RestController
@RequestMapping("/diagnostic")
public class DiagnosticController {

    private final DiagnosticService diagnosticService;
    private final ApplicationContext applicationContext;

    public DiagnosticController(DiagnosticService diagnosticService,
                                ApplicationContext applicationContext) {
        this.diagnosticService = diagnosticService;
        this.applicationContext = applicationContext;
    }


    @GetMapping("/test-tools")
    public String testToolsEnhanced() {
        try {
            return diagnosticService.getAvailableToolsReport();
        } catch (Exception e) {
            return "Erreur lors du diagnostic des outils avec diagnosticService : " + e.getMessage();
        }
    }

    @GetMapping("/beans")
    public String listBeans() {
        StringBuilder result = new StringBuilder();
        result.append("=== DIAGNOSTIC DES BEANS SPRING ===\n\n");

        // Liste tous les ToolCallbackProvider
        Map<String, ToolCallbackProvider> toolProviders = applicationContext.getBeansOfType(ToolCallbackProvider.class);
        result.append("ToolCallbackProvider trouvés : ").append(toolProviders.size()).append("\n");

        for (Map.Entry<String, ToolCallbackProvider> entry : toolProviders.entrySet()) {
            result.append("- Bean name: ").append(entry.getKey())
                    .append(" | Class: ").append(entry.getValue().getClass().getName()).append("\n");
        }

        result.append("\n=== TOUS LES BEANS MCP ===\n");
        String[] beanNames = applicationContext.getBeanNamesForType(Object.class);
        for (String beanName : beanNames) {
            if (beanName.toLowerCase().contains("mcp") ||
                    beanName.toLowerCase().contains("tool") ||
                    beanName.toLowerCase().contains("callback")) {
                result.append("- ").append(beanName).append(" : ")
                        .append(applicationContext.getType(beanName)).append("\n");
            }
        }

        return result.toString();
    }
}