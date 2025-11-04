package com.orange.adv.ihm.model;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class UserEntity {

    private String cuid;
    private String firstName;
    private ProfilEntity profil;
}
