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
 * basta acessar 0.0.0.0:8080/form_info.php
 */

$nome = '';
if (isset($_POST['nome'])) {
    $nome = $_POST['nome'];
}
?>
<html>
  <body>
    <form method="post">
        <label for="nome">
          Digite seu nome:
        </label>
        <input id="nome" name="nome" type="text" autofocus value="<?=$nome?>">
        <input type="submit" value="Enviar">
        <br />
        <?php if ($nome) { ?>
          Bem Vindo! <?=$nome?>
        <?php } ?>
    </form>
  </body>
</html>