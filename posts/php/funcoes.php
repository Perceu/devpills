<?php
/*
Funções no PHP
Parâmetros, retorno e type hint
*/
function somar(int $a, int $b): int {
    return $a + $b;
}

function saudacao(string $nome): string {
    return "Olá, $nome!";
}

echo somar(10, 5) . "\n";
echo saudacao("PHP") . "\n";

// Parâmetro opcional
function incrementar($num, $passo = 1) {
    return $num + $passo;
}

echo incrementar(5) . "\n";
echo incrementar(5, 3);
