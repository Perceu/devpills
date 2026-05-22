<?php
/*
Tratamento de erros com try/catch
Capturando exceções no PHP
*/
function dividir($a, $b) {
    if ($b == 0) {
        throw new InvalidArgumentException(
            "Divisão por zero não permitida"
        );
    }
    return $a / $b;
}

try {
    echo dividir(10, 2) . "\n";
    echo dividir(10, 0);
} catch (InvalidArgumentException $e) {
    echo "Erro: " . $e->getMessage();
}
