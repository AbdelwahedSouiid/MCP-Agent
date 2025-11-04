
package com.orange.adv.ihm.controller;


import com.orange.adv.ihm.service.McpLlmService;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.ResponseEntity;

@RestController
@RequestMapping("/api/mcp")
public class McpLlmController {

    private final McpLlmService mcpLlmService;

    public McpLlmController(McpLlmService mcpLlmService) {
        this.mcpLlmService = mcpLlmService;
    }

    @PostMapping("/ask")
    public ResponseEntity<String> ask(@RequestParam String question) {

        String response = mcpLlmService.askLlm(question);
        return ResponseEntity.ok(response);
    }

}
