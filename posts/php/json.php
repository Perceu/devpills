<?php
/*
JSON no PHP
json_encode e json_decode
*/
$dados = [
    "nome" => "Maria",
    "idiomas" => ["PHP", "Python", "JavaScript"],
    "ativo" => true,
];

$json = json_encode($dados, JSON_PRETTY_PRINT);
echo $json . "\n";

$decoded = json_decode($json, true);
echo $decoded["nome"] . "\n";

foreach ($decoded["idiomas"] as $lang) {
    echo " - $lang\n";
}
