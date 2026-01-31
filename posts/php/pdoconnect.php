<?php 
/*
 * Subir o servidor de desenvolvimento do PHP
 * php -S 0.0.0.0:8080
 * 
 * Tornando a pasta atual a raiz do servidor 
 * 
 * lembrando que o output do PHP se for HTML,
 * sera interpretado corretamente no navegador
 * 
 * basta acessar 0.0.0.0:8080/pdoconnect.php
 * 
 * Código para estudo muito inseguro.
 */

if (isset($_POST['nome'])) {
    $db = new PDO('sqlite:'.__DIR__.'/sample.sqlite3');
    $nome = $_POST['nome'];
    $telefone = $_POST['telefone'];
    $db->query("insert into clientes ('nome', 'telefone') values ('$nome', '$telefone')");
}
?>
<html>
  <body>
    <form method="post">
        <label for="nome">
          Nome Cliente:
        </label><br />
        <input id="nome" name="nome" type="text" autofocus><br />
        <label for="nome">
          Telefone:
        </label><br />
        <input id="telefone" name="telefone" type="text" ><br />
        <input type="submit" value="Enviar">
    </form>
  </body>
</html>