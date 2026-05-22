<?php
/*
Condicionais no PHP
if, elseif, else e switch
*/
$idade = 18;

if ($idade >= 18) {
    echo "Maior de idade\n";
} else {
    echo "Menor de idade\n";
}

$nota = 85;
if ($nota >= 90) {
    echo "Conceito A";
} elseif ($nota >= 80) {
    echo "Conceito B";
} else {
    echo "Conceito C";
}
