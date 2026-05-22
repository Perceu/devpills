<?php
/*
Classes e objetos no PHP
Propriedades, métodos e construtor
*/
class Usuario {
    public function __construct(
        public string $nome,
        public string $email,
    ) {}

    public function saudacao(): string {
        return "Olá, eu sou {$this->nome}";
    }
}

$user = new Usuario("João", "joao@email.com");
echo $user->saudacao() . "\n";
echo "Email: {$user->email}";
