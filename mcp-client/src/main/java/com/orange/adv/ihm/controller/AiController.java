

package com.orange.adv.ihm.controller;

import com.orange.adv.ihm.agents.AiAgent;

import org.springframework.web.bind.annotation.GetMapping;

import org.springframework.web.bind.annotation.RestController;

@RestController
public class AiController {

    private AiAgent aiAgent;

    public AiController(AiAgent aiAgent) {
        this.aiAgent = aiAgent;
    }

    @GetMapping("/chat")
    public String chat(String query){
        return aiAgent.askLLM(query);
    }


}
