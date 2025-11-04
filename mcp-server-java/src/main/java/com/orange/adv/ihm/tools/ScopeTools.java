package com.orange.adv.ihm.tools;

import com.orange.adv.ihm.model.ScopeEntity;
import jakarta.annotation.PostConstruct;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class ScopeTools {

   private final List<ScopeEntity> scopes = new ArrayList<>();

    @PostConstruct
    public void initScopes() {
        // Scopes OAuth2 / OpenID Connect standards
        scopes.add(new ScopeEntity("1", "openid", "OpenID Connect", "Scope obligatoire pour l'authentification OpenID Connect"));
        scopes.add(new ScopeEntity("2", "profile", "Profil utilisateur", "Accès aux informations de profil de l'utilisateur"));
        scopes.add(new ScopeEntity("3", "email", "Email", "Accès à l'adresse email de l'utilisateur"));
        scopes.add(new ScopeEntity("4", "address", "Adresse", "Accès à l'adresse postale de l'utilisateur"));
        scopes.add(new ScopeEntity("5", "phone", "Téléphone", "Accès au numéro de téléphone de l'utilisateur"));

        // Scopes d'accès aux données
        scopes.add(new ScopeEntity("6", "read", "Lecture", "Accès en lecture seule aux ressources"));
        scopes.add(new ScopeEntity("7", "write", "Écriture", "Accès en écriture aux ressources"));
        scopes.add(new ScopeEntity("8", "delete", "Suppression", "Autorisation de suppression des ressources"));
        scopes.add(new ScopeEntity("9", "admin", "Administration", "Accès administrateur complet"));

        // Scopes spécifiques métier
        scopes.add(new ScopeEntity("10", "user:read", "Lecture utilisateurs", "Consultation des données utilisateurs"));
        scopes.add(new ScopeEntity("11", "user:write", "Modification utilisateurs", "Création et modification des utilisateurs"));
        scopes.add(new ScopeEntity("12", "user:delete", "Suppression utilisateurs", "Suppression des comptes utilisateurs"));

        // Scopes pour les ressources
        scopes.add(new ScopeEntity("13", "resource:read", "Lecture ressources", "Consultation des ressources"));
        scopes.add(new ScopeEntity("14", "resource:write", "Modification ressources", "Création et modification des ressources"));
        scopes.add(new ScopeEntity("15", "resource:delete", "Suppression ressources", "Suppression des ressources"));

        // Scopes pour les rapports et analytics
        scopes.add(new ScopeEntity("16", "reports:read", "Lecture rapports", "Consultation des rapports"));
        scopes.add(new ScopeEntity("17", "analytics:read", "Lecture analytics", "Accès aux données d'analyse"));

        // Scopes pour les fichiers
        scopes.add(new ScopeEntity("18", "files:read", "Lecture fichiers", "Téléchargement et consultation des fichiers"));
        scopes.add(new ScopeEntity("19", "files:write", "Écriture fichiers", "Upload et modification des fichiers"));
        scopes.add(new ScopeEntity("20", "files:delete", "Suppression fichiers", "Suppression des fichiers"));

        // Scopes pour les notifications
        scopes.add(new ScopeEntity("21", "notifications:read", "Lecture notifications", "Consultation des notifications"));
        scopes.add(new ScopeEntity("22", "notifications:write", "Envoi notifications", "Envoi de notifications"));

        // Scopes pour les paramètres système
        scopes.add(new ScopeEntity("23", "settings:read", "Lecture paramètres", "Consultation des paramètres système"));
        scopes.add(new ScopeEntity("24", "settings:write", "Modification paramètres", "Modification des paramètres système"));

        // Scopes pour les logs et audit
        scopes.add(new ScopeEntity("25", "logs:read", "Lecture logs", "Consultation des logs système"));
        scopes.add(new ScopeEntity("26", "audit:read", "Lecture audit", "Consultation des pistes d'audit"));

        // Scopes pour les API externes
        scopes.add(new ScopeEntity("27", "api:read", "Lecture API", "Accès en lecture aux API externes"));
        scopes.add(new ScopeEntity("28", "api:write", "Écriture API", "Accès en écriture aux API externes"));

        // Scopes pour les sessions
        scopes.add(new ScopeEntity("29", "session:manage", "Gestion sessions", "Gestion des sessions utilisateur"));

        // Scope offline access
        scopes.add(new ScopeEntity("30", "offline_access", "Accès hors ligne", "Permet l'obtention de refresh tokens"));
    }

    @Tool(description = "Récupère la liste complète des scopes disponibles")
    public List<ScopeEntity> listScope() {
        return scopes;
    }

    @Tool(description ="Recherche un scope par son code")
    public ScopeEntity findScopeByCode(String code) {
        return scopes.stream()
                .filter(scope -> scope.getCdScope().equals(code))
                .findFirst()
                .orElse(null);
    }

    @Tool(description ="Recherche des scopes par libellé (recherche partielle)")
    public List<ScopeEntity> findScopesByLabel(String label) {
        return scopes.stream()
                .filter(scope -> scope.getLbScope().toLowerCase().contains(label.toLowerCase()))
                .toList();
    }

    @Tool(description ="Supprime un scope par son code")
    public boolean removeScopeByCode(String code) {
        return scopes.removeIf(scope -> scope.getCdScope().equals(code));
    }

    @Tool(description ="Met à jour un scope existant")
    public boolean updateScope(String code, String newLabel, String newComment) {
        ScopeEntity scope = findScopeByCode(code);
        if (scope != null) {
            scope.setLbScope(newLabel);
            scope.setComment(newComment);
            return true;
        }
        return false;
    }

    @Tool(description ="Vérifie si un scope existe")
    public boolean scopeExists(String code) {
        return scopes.stream().anyMatch(scope -> scope.getCdScope().equals(code));
    }

    @Tool(description ="Ajoute un nouveau scope à la liste")
    public boolean addScope(String id, String cdScope, String lbScope, String comment) {
        // Vérifier si le scope existe déjà
        if (scopeExists(cdScope)) {
            return false; // Scope déjà existant
        }
        scopes.add(new ScopeEntity(id, cdScope, lbScope, comment));
        return true;
    }

    @Tool(description ="Récupère le nombre total de scopes")
    public int getScopeCount() {
        return scopes.size();
    }
}