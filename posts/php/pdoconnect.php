<?php
/*
PDO + SQLite no PHP
php -S 0.0.0.0:8080
acesse 0.0.0.0:8080/pdoconnect.php
Requires sample.sqlite3 na mesma pasta
Código para estudo, muito inseguro (SQL injection)
*/
if (isset($_POST['nome'])) {
    $db = new PDO('sqlite:'.__DIR__.'/sample.sqlite3');
    $nome = $_POST['nome'];
    $telefone = $_POST['telefone'];
    $db->query("insert into clientes values ('$nome', '$telefone')");
}
?>
<html>
<body>
<form method="post">
    <label>Nome:</label><input name="nome" type="text"><br>
    <label>Telefone:</label><input name="telefone" type="text"><br>
    <input type="submit" value="Salvar">
</form>
</body>
</html>