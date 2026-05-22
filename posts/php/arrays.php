<?php
/*
Arrays no PHP
Indexados, associativos e multidimensionais
*/
$cores = ["Vermelho", "Verde", "Azul"];
echo $cores[0] . "\n";

$usuario = [
    "nome" => "João",
    "email" => "joao@email.com",
];
echo $usuario["nome"] . "\n";

$turma = [
    ["nome" => "Ana", "nota" => 9],
    ["nome" => "Beto", "nota" => 8],
];

foreach ($turma as $aluno) {
    echo "{$aluno['nome']}: {$aluno['nota']}\n";
}
