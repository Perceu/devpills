<?php
/*
Recebendo dados de formulário com PHP
php -S 0.0.0.0:8080
acesse 0.0.0.0:8080/form_info.php
*/
$nome = '';
if (isset($_POST['nome'])) {
    $nome = $_POST['nome'];
}
?>
<html>
<body>
<form method="post">
    <label>Digite seu nome:</label>
    <input name="nome" type="text" value="<?=$nome?>">
    <input type="submit" value="Enviar">
    <?php if ($nome) { echo "Bem Vindo! $nome"; } ?>
</form>
</body>
</html>